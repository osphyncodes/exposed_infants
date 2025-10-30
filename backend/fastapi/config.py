# fastapi/config.py
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

class Settings(BaseModel):
    authjwt_secret_key: str = "supersecretkey"
    authjwt_access_token_expires: int = 900      # 15 minutes
    authjwt_refresh_token_expires: int = 604800  # 7 days

@AuthJWT.load_config
def get_config():
    return Settings()
