from ydata.sdk.connectors._models.credentials.credentials import Credentials

class AzureBlobCredentials(Credentials):
    access_key_id: str
    account_key: str
