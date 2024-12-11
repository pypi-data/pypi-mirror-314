from ydata.sdk.connectors._models.credentials.credentials import Credentials

class AWSS3Credentials(Credentials):
    access_key_id: str
    secret_access_key: str
    region: str
