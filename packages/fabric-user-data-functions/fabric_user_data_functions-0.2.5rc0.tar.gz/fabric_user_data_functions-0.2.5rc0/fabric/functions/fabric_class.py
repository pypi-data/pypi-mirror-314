import struct
import typing
from urllib.parse import urlparse

# flake8: noqa: I005
import pyodbc
from azure.storage.filedatalake import DataLakeDirectoryClient

from fabric.functions.internal.custom_token_credential import CustomTokenCredential
from fabric.functions.internal.fabric_item import FabricItem
from fabric.functions.udf_exception import UserDataFunctionInternalError

class FabricSqlConnection(FabricItem):

    APPSETTINGS_PATH = "sqlendpoint"
    INITIAL_CATALOG = "Initial Catalog"

    def _get_split_connection_string(self) -> typing.Dict[str, str]:

        connString = self.endpoints[self.APPSETTINGS_PATH]["ConnectionString"]

        # Lakehouse connection string contains Data Source instead of Server
        connString = connString.replace("Data Source", "Server")

        if "=" not in connString:
            return { "Server": connString }
        
        if "Server" not in connString:
            raise UserDataFunctionInternalError("Server value is not set in connection")

        split_by_semicolon = connString.split(";")
        return {x.split("=")[0].strip(): x.split("=")[1].strip() for x in split_by_semicolon}

    def connect(self) -> pyodbc.Connection:
        if self.APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.APPSETTINGS_PATH} is not set")
        
        dict_conn_string = self._get_split_connection_string()
        connString = dict_conn_string["Server"]

        # https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Connect-to-Azure-SQL-Database
        
        token = self.endpoints[self.APPSETTINGS_PATH]["AccessToken"].encode('UTF-8')
        exptoken = b""
        for i in token:
            exptoken+=bytes({i})
            exptoken+=bytes(1)
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

        driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
        latest_driver = driver_names[-1] if driver_names else None

        if latest_driver is None:
            raise UserDataFunctionInternalError("No ODBC Driver found for SQL Server. Please download the latest for your OS.")

        conn_string = f'DRIVER={{{latest_driver}}};Server={connString};Encrypt=yes;'
        if self.INITIAL_CATALOG in dict_conn_string:
            conn_string += f"Database={dict_conn_string[self.INITIAL_CATALOG]}"

        return pyodbc.connect(conn_string, attrs_before = {1256:tokenstruct}, timeout=60)
    
class FabricLakehouseFilesClient(FabricItem):
    APPSETTINGS_PATH = "fileendpoint"
    
    def connect(self) -> DataLakeDirectoryClient:
        if self.APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.APPSETTINGS_PATH} is not set")
        
        raw_path = self.endpoints[self.APPSETTINGS_PATH]['ConnectionString']
        parsed_path = urlparse(raw_path)
        
        accessToken = self.endpoints[self.APPSETTINGS_PATH]['AccessToken']

        # The account URL is the scheme and netloc parts of the parsed path
        account_url = f"{parsed_path.scheme}://{parsed_path.netloc}"

        # The file system name and directory name are in the path part of the parsed path
        # We remove the leading slash and then split the rest into the file system name and directory name
        file_system_name, _, directory_name = parsed_path.path.lstrip('/').partition('/')

        directory_client = DataLakeDirectoryClient(account_url, file_system_name, directory_name, CustomTokenCredential(accessToken))
        return directory_client
    
class FabricLakehouseClient(FabricItem):

    def connectToSql(self) -> pyodbc.Connection:
        return FabricSqlConnection(self.alias_name, self.endpoints).connect()  

    def connectToFiles(self) -> DataLakeDirectoryClient:
        return FabricLakehouseFilesClient(self.alias_name, self.endpoints).connect()

class UserDataFunctionContext:
    def __init__(self, invocationId: str, executingUser: typing.Dict[str, typing.Dict[str, str]]):
        self.__invocation_id = invocationId
        self.__executing_user = executingUser

    @property
    def invocation_id(self) -> str:
        return self.__invocation_id
    
    @property
    def executing_user(self) -> typing.Dict[str, typing.Dict[str, str]]:
        return self.__executing_user
