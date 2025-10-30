from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

class Settings(BaseModel):
    authjwt_secret_key: str = "YOUR_SECRET_KEY_HERE"  # replace with a strong random string

# This tells fastapi-jwt-auth where to read the settings


@AuthJWT.load_config
def get_config():
    return Settings()
