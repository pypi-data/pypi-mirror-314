# SIA Storage Access Layer

### To install the sia storage access package in another project
Run the following pip command to install it:\
`pip install sia-storage-access`

### To Initialize the Azure Blob Storage, use the following code
```
from sia_storage.storage_handler import StorageHandler
blob_credentials = {'blob_config':{'account_name': '', 'account_key':'', 'container_name':'testing'}}
storage_handler = StorageHandler('azure', blob_credentials)
blob_storage = storage_handler.get_storage()
```
### To Initialize the Azure Datalake Storage, use the following code
```
from sia_storage.storage_handler import StorageHandler
data_lake_credentials = {'datalake_config':{'account_name': '', 'container_name':'testing', 'credential':None}}
storage_handler = StorageHandler('azure', data_lake_credentials)
data_lake_storage = storage_handler.get_storage()
```
### To Initialize the Azure table Storage, use the following code
```
from sia_storage.storage_handler import StorageHandler
table_credentials = {'table_config':{'account_name': '', 'account_key':'', 'table_name':'testing'}}
storage_handler = StorageHandler('azure', table_credentials)
table_storage = storage_handler.get_storage()
```
