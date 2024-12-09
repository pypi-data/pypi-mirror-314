from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from sia_storage.exception_handler import SiaAzureException
import logging


class AzureBlobStorage:
    """
    Acts as a wrapper class to provide azure blob storage specific methods like file upload,
    download file, list the blobs and delete blob.
    """

    CONNECTION_FORMAT = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net"

    def __init__(self, account_name: str, account_key: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            AzureBlobStorage.CONNECTION_FORMAT.format(account_name, account_key)
        )
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self.logger = logging.getLogger(__name__)

    def upload_file(self, file_path: str, blob_name: str):
        """
        Uploads a local file into Azure Blob Storage.

        param file_path (str): Local path of the file to be uploaded.
        param blob_name (str): Name of the blob in the storage container.
        return (str): Name of the blob into which file will be uploaded.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            self.logger.info(f"File '{file_path}' uploaded to blob '{blob_name}'")
            return blob_name
        except Exception as e:
            raise SiaAzureException(e, f'Error uploading file: {file_path}')

    def download_file(self, blob_name: str, download_path: str):
        """
        Downloads a blob from Azure Blob Storage into the local.

        param blob_name (str): Name of the blob in the storage container.
        param download_path (str): Download the file into the local path.
        return (str): Downloaded file path.
        raises: SiaAzureException in case any runtime exception is caught
        and also if blob is not found in the storage container.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            self.logger.info(f"Blob '{blob_name}' downloaded to '{download_path}'")
            return download_path
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Blob '{blob_name}' not found")
        except Exception as e:
            raise SiaAzureException(e, f"Error downloading blob: {blob_name}")

    def list_blobs(self):
        """
        Lists all the blobs from the azure blob storage.

        return (list): List of blob names.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:
            blobs = self.container_client.list_blobs()
            self.logger.info("Blobs in container:")
            for blob in blobs:
                self.logger.info(f"- {blob.name}")
            return [blob.name for blob in blobs]
        except Exception as e:
            raise SiaAzureException(e, f"Error listing blobs.")

    def delete_blob(self, blob_name: str):
        """
        Deletes a blob from Azure Blob Storage.

        param blob_name (str): Name of the blob to delete.
        return (str): Name of the deleted blob.
        raises: SiaAzureException in case any runtime exception is caught
        and also if the blob is not found in the storage container.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            self.logger.info(f"Blob '{blob_name}' deleted successfully")
            return blob_name
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Blob '{blob_name}' not found")
        except Exception as e:
            raise SiaAzureException(e, f"Error deleting blob: {blob_name}")


class AzureDataLake:
    """
    Acts as a wrapper class to provide azure data lake storage specific methods like create folder,
    create file, download file, list files and delete file.
    """

    def __init__(self, account_name: str, container_name: str, credential=None):
        self.account_url = f"https://{account_name}.dfs.core.windows.net"
        self.datalake_service_client = DataLakeServiceClient(account_url=self.account_url, credential=credential)
        self.file_system_client = self.datalake_service_client.get_file_system_client(container_name)
        self.logger = logging.getLogger(__name__)

    def create_folder(self, folder_path):
        """
        Create a folder into the datalake storage if not created.

        param folder_path (str): Name of the folder path to be created
        return (str): Created folder path.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        folder_client = self.file_system_client.get_directory_client(folder_path)
        try:
            folder_client.get_directory_properties()
            self.logger.info(f"Folder '{folder_path}' exists")
            return folder_path
        except Exception as e:
            self.logger.error(f"Folder '{folder_path}' does not exist. Creating it")
            folder_client.create_directory()
        return folder_client

    def upload_file(self, local_path: str, remote_path: str):
        """
        Uploads a file to Azure Data Lake.

        param local_path (str): Local path of the file to be uploaded.
        param remote_path (str): Path inside the Data Lake file system.
        return (str): Path of the data lake file system into which file is uploaded.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:
            file_client = self.file_system_client.get_directory_client(remote_path)
            file_client.create_file(local_path, overwrite=True)
            self.logger.info(f"File '{local_path}' created into Data Lake path '{remote_path}'.")
            return remote_path
        except Exception as e:
            raise SiaAzureException(e, f"Error creating file into Data Lake: {local_path}")

    def download_file(self, remote_path: str, local_path: str):
        """
        Downloads a file from Azure Data Lake.

        param remote_path (str): Path in the Data Lake file system.
        param local_path (str): Local path to save the downloaded file.
        return (str): Downloaded local file path.
        raises: SiaAzureException in case any runtime exception is caught
        and also if the path is not present inside the data lake file system.
        """
        try:
            file_client = self.file_system_client.get_file_client(remote_path)
            with open(local_path, "wb") as file:
                file.write(file_client.download_file().readall())
            self.logger.info(f"Data Lake file '{remote_path}' downloaded to '{local_path}'")
            return local_path
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Data Lake file '{remote_path}' not found")
        except Exception as e:
            raise SiaAzureException(e, f"Error downloading from Data Lake: {remote_path}")

    def list_files(self, directory: str = ""):
        """
        Lists files and directories in a specified Data Lake directory.

        param directory (str): Path of the directory to list. Defaults to root.
        return (list): List of data lake directory path files and directory names.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:

            paths = self.file_system_client.get_paths(path=directory)
            self.logger.info("Files and directories in Data Lake:")
            for path in paths:
                self.logger.info(f"- {path.name}")
            return [path.name for path in paths]
        except Exception as e:
            raise SiaAzureException(e, f"Error listing Data Lake files from {directory}")

    def delete_file(self, file_path: str):
        """
        Deletes a file from Azure Data Lake.

        param file_path (str): Path of the file to delete in the Data Lake.
        return (str): Deleted file path inside the data lake file system.
        raises: SiaAzureException in case any runtime exception is caught
        and also if the file path is not present inside the data lake file system.
        """
        try:
            folder_client = self.file_system_client.get_directory_client(file_path)
            folder_client.delete_directory()
            self.logger.info(f"Data Lake file '{file_path}' deleted successfully")
            return file_path
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Data Lake file '{file_path}' not found")
        except Exception as e:
            raise SiaAzureException(e, f"Error deleting Data Lake file: {file_path}")


class AzureTable:
    """
    Acts as a wrapper class to provide azure blob table specific methods like insert entity,
    query entity, update entity, list all entities and delete entity.
    """

    CONNECTION_FORMAT = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net"

    def __init__(self, account_name: str, account_key: str, table_name: str):
        self.table_service_client = TableServiceClient.from_connection_string(
            AzureTable.CONNECTION_FORMAT.format(account_name, account_key)
        )
        self.table_client = self.table_service_client.get_table_client(table_name=table_name)
        self.logger = logging.getLogger(__name__)

    def insert_entity(self, entity: dict):
        """
        Inserts an entity into the Azure Table Storage.

        param entity (dict): Entity data to insert. Must contain 'PartitionKey' and 'RowKey'.
        raises: SiaAzureException in case any runtime exception is caught
        and also if an entity is already exists.
        """
        try:
            self.table_client.create_entity(entity=entity)
            self.logger.info(f"Entity inserted: {entity}")
        except ResourceExistsError as e:
            raise SiaAzureException(e, f"Entity already exists: {entity}")
        except Exception as e:
            raise SiaAzureException(e, f"Error inserting entity: {entity}")

    def query_entities(self, filter_expression: str = None):
        """
        Queries entities from the Azure Table Storage.

        param filter_expression (str): OData filter expression. Defaults to None (fetch all).
        return ItemPaged[TableEntity]: Filtered list of table entities.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:
            entities = self.table_client.query_entities(filter=filter_expression)
            return entities
        except Exception as e:
            raise SiaAzureException(e, f"Error querying entities: {filter_expression}")

    def update_entity(self, entity: dict, mode: str = "merge"):
        """
        Updates an entity in the Azure Table Storage.

        param entity (dict): Entity data to update. Must contain 'PartitionKey' and 'RowKey'.
        param mode (str): Update mode ('merge' or 'replace'). Defaults to 'merge'.
        raises: SiaAzureException in case any runtime exception is caught
        and also if an entity is not found.
        """
        try:
            self.table_client.update_entity(entity=entity, mode=mode)
            self.logger.info(f"Entity updated: {entity}")
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Entity not found: {entity}")
        except Exception as e:
            raise SiaAzureException(e, f"Error updating entity: {entity}")

    def delete_entity(self, partition_key: str, row_key: str):
        """
        Deletes an entity from the Azure Table Storage.

        param partition_key (str): PartitionKey of the entity.
        param row_key (str): RowKey of the entity.
        raises: SiaAzureException in case any runtime exception is caught
        and also if an entity is not found.
        """
        try:
            self.table_client.delete_entity(partition_key=partition_key, row_key=row_key)
            self.logger.info(f"Entity deleted: PartitionKey={partition_key}, RowKey={row_key}")
        except ResourceNotFoundError as e:
            raise SiaAzureException(e, f"Entity not found: PartitionKey={partition_key}, RowKey={row_key}")
        except Exception as e:
            raise SiaAzureException(e, f"Error deleting entity: PartitionKey={partition_key}, RowKey={row_key}")

    def list_all_entities(self):
        """
        Lists all entities in the table.

        return ItemPaged[TableEntity]: list of table entities.
        raises: SiaAzureException in case any runtime exception is caught.
        """
        try:
            entities = self.table_client.list_entities()
            self.logger.info(f"All entities returned")
            return entities
        except Exception as e:
            raise SiaAzureException(e, f"Error listing entities")
