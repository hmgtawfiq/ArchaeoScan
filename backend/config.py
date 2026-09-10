import os
from dotenv import load_dotenv

load_dotenv()

CDSE_CLIENT_ID = os.getenv("CDSE_CLIENT_ID", "")
CDSE_CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET", "")

CDSE_TOKEN_URL = os.getenv(
    "CDSE_TOKEN_URL",
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
)

CDSE_PROCESS_URL = os.getenv(
    "CDSE_PROCESS_URL",
    "https://sh.dataspace.copernicus.eu/process/v1",
)

CDSE_CATALOG_URL = os.getenv(
    "CDSE_CATALOG_URL",
    "https://sh.dataspace.copernicus.eu/catalog/v1/search",
)
