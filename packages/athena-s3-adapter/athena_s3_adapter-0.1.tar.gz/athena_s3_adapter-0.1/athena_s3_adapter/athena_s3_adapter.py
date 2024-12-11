# -*- coding: utf-8 -*-

# バージョン  | 更新日      | 更新者 | 更新内容 |
# -----------|------------|--------|----------|
#   v1.0     | 2024/09/xx | 村田   | create_athena_api新規作成 |
#   v1.1     | 2024/10/08 | 村田   | read_sql関数追加 |
#   v1.2     | 2024/10/19 | 村田   | list_table関数追加 |


import pandas as pd
import boto3
import time
import io
import re

# Athenaテーブルの存在チェック
def _exist_table(athena_client, catalog, database, table):
    try:
        response = athena_client.get_table_metadata(
            CatalogName=catalog,
            DatabaseName=database,
            TableName=table,
        )
        assert(response['TableMetadata']['Name'] == table)
        return True
    except:
        return False
    
# Athenaテーブルの実体データパス(S3)を取得する
def _get_s3_location(athena_client, catalog, database, table):
    response = athena_client.get_table_metadata(
        CatalogName=catalog,
        DatabaseName=database,
        TableName=table,
    )
    return response['TableMetadata']['Parameters']['location']

# S3ロケーションパスをbucketとobjectに分解する
def _parse_location(location):
    matched = re.match(r's3://(.*?)/(.*)', location)
    bucket = matched.group(1)
    obj_path = matched.group(2)
    return bucket, obj_path

# AthenaでSQLを実行し、テーブルを作成したり、抽出結果をdfで取得する
def _exec_sql(s3_client, athena_client, workgroup, catalog, database, sql):
    # Athenaでクエリを開始する
    query_execution = athena_client.start_query_execution(
        QueryString=sql,
        WorkGroup=workgroup,
        QueryExecutionContext={
            'Database': database,
            'Catalog': catalog,
        },
    )

    # クエリの完了を1秒ポーリングして待つ
    query_execution_id = query_execution['QueryExecutionId']
    retry_count = 0
    while True:
        query_execution = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']
        query_execution_status = query_execution['Status']['State']
        if query_execution_status == 'SUCCEEDED':
            break
        if query_execution_status == 'FAILED':
            raise Exception("get_query_execution: FAILED")
        else:
            time.sleep(1)
            retry_count += 1
            if retry_count == 60 * 110: # 110分
                raise Exception("query TIMEOUT")
    
    # クエリ実行結果から結果保存先のバケット、オブジェクト（ファイル）を取得する
    bucket, obj_path = _parse_location(query_execution['ResultConfiguration']['OutputLocation'])

    df_result = None
    if query_execution['StatementType'] == 'DML': # SELECTによるデータ取得クエリ
        # クエリの結果はS3に保存されているので読み取ってdfに変換する
        get_object_result = s3_client.get_object(Bucket=bucket, Key=obj_path)
        assert(get_object_result['ResponseMetadata']['HTTPStatusCode'] == 200)
        body = get_object_result['Body'].read().decode('utf-8')
        df_result = pd.read_csv(io.StringIO(body))

    # 作成されたS3のファイルは不要なので削除する
    s3_client.delete_object(Bucket=bucket, Key=obj_path)
    s3_client.delete_object(Bucket=bucket, Key=f'{obj_path}.metadata')
    if 'DataManifestLocation' in query_execution['Statistics']:
        bucket, obj_path = _parse_location(query_execution['Statistics']['DataManifestLocation'])
        s3_client.delete_object(Bucket=bucket, Key=obj_path)

    # dfを返す
    return df_result

# S3のフォルダ(prefix)からparquetデータを読み込む
def _read_paruqet_s3_folder(s3_client, bucket, folder):
    contents_count = 0
    next_token = ''

    result_df_list = []
    while True:
        if next_token == '':
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder, ContinuationToken=next_token)

        if 'Contents' in response:
            contents = response['Contents']
            contents_count = contents_count + len(contents)
            for content in contents:
                get_object_result = s3_client.get_object(Bucket=bucket, Key=content['Key'])
                assert(get_object_result['ResponseMetadata']['HTTPStatusCode'] == 200)
                body = get_object_result['Body'].read()
                df_tmp = pd.read_parquet(io.BytesIO(body))
                result_df_list.append(df_tmp)

        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
        else:
            break

    df_result = pd.concat(result_df_list, ignore_index=True)
    return df_result

# Athenaテーブルの読み込み
def _read_table(s3_client, athena_client, catalog, database, table):
    # テーブルの実態データ(S3)を取得
    s3_location = _get_s3_location(athena_client, catalog, database, table)
    bucket, obj_path = _parse_location(s3_location)
    # テーブルの読み込み
    df = _read_paruqet_s3_folder(s3_client, bucket, obj_path)
    return df

# S3のフォルダ(prefix)を削除する
def _delete_s3_folder(s3_client, bucket, folder):
    contents_count = 0
    next_token = ''

    while True:
        if next_token == '':
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder, ContinuationToken=next_token)

        if 'Contents' in response:
            contents = response['Contents']
            if len(contents) > 0:
                delete_objects_result = s3_client.delete_objects(Bucket=bucket, Delete={'Objects': [{'Key': c['Key']} for c in contents]})
                assert(delete_objects_result['ResponseMetadata']['HTTPStatusCode'] == 200)
                contents_count += len(delete_objects_result['Deleted'])

        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
        else:
            break

    return contents_count

# AthenaテーブルとS3データの削除
def _delete_table(s3_client, athena_client, workgroup, catalog, database, table):
    # テーブルの実態データ(S3)を取得
    s3_location = _get_s3_location(athena_client, catalog, database, table)
    if s3_location is not None:
        bucket, obj_path = _parse_location(s3_location)
    # テーブルの削除
    _exec_sql(s3_client, athena_client, workgroup, 'AwsDataCatalog', 'tss_share_db', f'DROP TABLE `{table}`')
    if s3_location is not None:
        # S3の削除
        _delete_s3_folder(s3_client, bucket, obj_path)
    return

# Athenaテーブルのリスト
def _list_table(athena_client, workgroup, catalog, database, regexp):
    next_token = ''
    tables = []
    while True:
        response = athena_client.list_table_metadata(**{
            'WorkGroup': workgroup,
            'CatalogName': catalog,
            'DatabaseName': database,
            **({'Expression': regexp} if regexp is not None else {}),
            **({'NextToken': next_token} if next_token != '' else {}),
        })

        assert(response['ResponseMetadata']['HTTPStatusCode'] == 200)
        
        if 'TableMetadataList' in response:
            tables += response['TableMetadataList']

        if 'NextToken' in response:
            next_token = response['NextToken']
        else:
            break

    return tables

# S3オブジェクトのサイズ
def _get_s3_size(s3_client, bucket, obj_path):
    total_size = 0
    next_token = ''

    while True:
        if next_token == '':
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=obj_path)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=obj_path, ContinuationToken=next_token)
        
        assert(response['ResponseMetadata']['HTTPStatusCode'] == 200)

        if 'Contents' in response:
            total_size += sum([int(c['Size']) for c in response['Contents']])

        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
        else:
            break

    return total_size

# Athenaテーブルのリスト
def _get_table_size(s3_client, athena_client, catalog, database, table):
    # テーブルの実態データ(S3)を取得
    s3_location = _get_s3_location(athena_client, catalog, database, table)
    if s3_location is None:
        return 0
    bucket, obj_path = _parse_location(s3_location)
    # テーブルのサイズを計算
    return _get_s3_size(s3_client, bucket, obj_path)

class _athena_api:
    """Athenaクラス"""

    def __init__(self, my_workgroup, context, auth):
        session = boto3.session.Session()
        if auth is not None and 'aws_access_key_id' in auth and 'aws_secret_access_key' in auth:
            aws_access_key_id = auth['aws_access_key_id']
            aws_secret_access_key = auth['aws_secret_access_key']
            athena_client = session.client('athena', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            s3_client     = session.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        else:
            athena_client = session.client('athena')
            s3_client     = session.client('s3')

        self._session = session
        self._athena_client = athena_client
        self._s3_client = s3_client
        self._my_workgroup = my_workgroup
        self._catalog = context['catalog'] if context is not None and 'catalog' in context else None
        self._database = context['database'] if context is not None and 'database' in context else None
        
    def exec_sql(self, sql: str, catalog=None, database=None):
        """
        SQL実行処理

        Parameters
        ----------
        sql: str
            SQL文字列
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する

        Returns
        -------
        df: DataFrame | None
            検索結果
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        return _exec_sql(self._s3_client, self._athena_client, self._my_workgroup, catalog, database, sql)
    
    def exist_table(self, table: str, catalog=None, database=None):
        """
        テーブル存在チェック

        Parameters
        ----------
        table: str
            Athenaテーブル名
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する

        Returns
        -------
        exist: Boolean
            存在有無
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        return _exist_table(self._athena_client, catalog, database, table)
    
    def read_table(self, table: str, catalog=None, database=None):
        """
        テーブル読み込み

        Parameters
        ----------
        table: str
            Athenaテーブル名
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する

        Returns
        -------
        df: DataFrame
            読み込んだテーブルデータ
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        return _read_table(self._s3_client, self._athena_client, catalog, database, table)

    def delete_table(self, table: str, catalog=None, database=None):
        """
        テーブル削除

        Parameters
        ----------
        table: str
            Athenaテーブル名
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        _delete_table(self._s3_client, self._athena_client, self._my_workgroup, catalog, database, table)
        
    def list_table(self, regexp=None, catalog=None, database=None):
        """
        テーブル一覧取得

        Parameters
        ----------
        reqexp: str | None
            テーブル名のフィルタ正規表現
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        return _list_table(self._athena_client, self._my_workgroup, catalog, database, regexp)
    
    def get_table_size(self, table: str, catalog=None, database=None):
        """
        テーブルのデータサイズ取得

        Parameters
        ----------
        table: str
            Athenaテーブル名
        catalog: str | None
            Athenaカタログ名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する
        database: str | None
            Athenaデータベース名 (SQL実行時のコンテキスト)
            Noneの場合はコンストラクト時のデフォルトコンテキストを使用する

        Returns
        -------
        size: int
            テーブルサイズ
        """
        catalog = catalog if catalog is not None else self._catalog
        database = database if database is not None else self._database
        return _get_table_size(self._s3_client, self._athena_client, catalog, database, table)


def create_athena_api(my_workgroup: str, *, context=None, auth=None):
    """
    Athenaインスタンスのファクトリー関数

    Parameters
    ----------
    my_workgroup: str
        Athena workgroup
    context: dict | None
        dict['catalog']: デフォルトのAthena Catalog
        dict['database']: デフォルトのAthena Database
    auth: dict | None
        dict['aws_access_key_id']: AWSアクセスキー。未指定の場合は.awsから読み出す
        dict['aws_secret_access_key']: AWSシークレット。未指定の場合は.awsから読み出す

    Returns
    -------
    athena : Athena APIインスタンス
        
    Examples
    --------
    >>> from athena_lib import create_athena_api
    >>> athena = create_athena_api(my_workgroup, context={'catalog': catalog, 'database': database})
    >>> df = athena.exec_sql(sql)
    >>> df
    """
    return _athena_api(my_workgroup, context, auth)


def read_sql(template_sql_file: str, replace_params) -> str:
    """
    SQLテンプレートを読み込み、テンプレート部分を実際の値で置き換える

    Parameters
    ----------
    template_sql_file: str
        可変部分が$XXXで書かれたSQLのファイルパス
    replace_params: dict
        可変部分を置き換えるパラメータ

    Returns
    -------
    sql: SQL文字列
    """
    with open(template_sql_file, encoding='utf_8') as f:
        sql = f.read()

    for key, val in replace_params.items():
        sql = sql.replace(f'${key}', val)

    return sql
