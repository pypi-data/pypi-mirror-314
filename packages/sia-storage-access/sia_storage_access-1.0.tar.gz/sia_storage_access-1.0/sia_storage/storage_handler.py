from sia_storage.azure_storage import *
from sia_storage.exception_handler import SiaAzureException


class StorageHandler:
    """
    Class acts as a handler to instantiate cloud specific storage class based on the
    requested cloud type and along with necessary credentials.
    Cloud type can be of the following values:
    - For Azure Cloud, pass cloud type as azure.
    """

    def __init__(self, cloud_type: str, credentials: dict):
        self.cloud_type = cloud_type
        self.credentials = credentials

    def get_storage(self):
        """
        Method to instantiate cloud specific storage on the cloud type, and it passes
        the necessary cloud specific credentials for the class.

        return: Instance of Cloud specific storage class
        raises: SiaAzureException in case of wrong cloud type
        """
        if self.cloud_type == 'azure':
            return _AzureStorageHandler.initialize_storage(**self.credentials)
        raise SiaAzureException(
            "Cloud Type is not supported",
            'Please pass the supported cloud type (Azure)'
        )


class _AzureStorageHandler:
    """
    Acts as a Handler to instantiate azure specific cloud storage class. Supports the
    following azure storage:
    Blob Storage
    Datalake Storage
    Blob Table Storage
    Pass any one of parameter configs to instantiate azure specific cloud storage and not
    all the parameters.

    param blob_config (dictionary): To instantiate blob storage, pass parameter blob config dictionary which
    should contain account name, account key and container name.
    param datalake_config (dictionary): To instantiate datalake storage, pass parameter datalake config dictionary
    which should contain account name, container name and credential.
    param table_config (dictionary): To instantiate blob table storage, pass parameter table config dictionary
    which should contain account name, account key and table name.
    return: Instance of the azure specific storage based on the parameter value.
    raises: SiaAzureException in case of no config or wrong config parameter is set and caught any runtime
    specific exception.
    """
    @staticmethod
    def initialize_storage(blob_config=None, datalake_config=None, table_config=None):
        try:
            if blob_config:
                return AzureBlobStorage(**blob_config)
            if datalake_config:
                return AzureDataLake(**datalake_config)
            if table_config:
                return AzureTable(**table_config)
            raise SiaAzureException(
                "Azure supported storage config is not set",
                'It supports only blob, datalake and table storage'
            )
        except Exception as e:
            raise SiaAzureException(e, 'Error initializing AzureHandler')
