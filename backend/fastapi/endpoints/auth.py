from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from django.contrib.auth.models import User
from schemas import LoginSchema, TokenResponse
from django.contrib.auth import authenticate
from config import Settings

router = APIRouter(prefix="", tags=["auth"])

# Existing login endpoint
@router.post("/token/", response_model=TokenResponse)
def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    user_obj = authenticate(username=user.username, password=user.password)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = Authorize.create_access_token(subject=user_obj.username)
    refresh = Authorize.create_refresh_token(subject=user_obj.username)
    
    print(access, refresh)
    return {"access_token": access, "refresh_token": refresh, 'success': True}

# Existing refresh endpoint
@router.post("/token/refresh/", response_model=TokenResponse)
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    username = Authorize.get_jwt_subject()
    new_access = Authorize.create_access_token(subject=username)
    new_refresh = Authorize.create_refresh_token(subject=username)
    return {"access_token": new_access, "refresh_token": new_refresh}

# 🔹 Protected endpoint

@router.get("/me/")
def get_profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"username": current_user}


@router.get("/profile/")
def me(Authorize: AuthJWT = Depends()):
    # Require a valid access token
    Authorize.jwt_required()

    username = Authorize.get_jwt_subject()
    try:
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user_obj.id,
        "username": user_obj.username,
        "email": user_obj.email,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
    }
