from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .schemas import UserModel, UserSignupModel, UserLoginModel, LoginResponseModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_access_token, create_access_token, verify_password
from .dependencies import RefreshTokenBearer
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()

REFRESH_TOKEN_EXPIRY=7
@auth_router.post("/signup", response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignupModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login', response_model=LoginResponseModel,status_code=status.HTTP_200_OK)
async def login(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    user = await user_service.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    password_valid = verify_password(password, user.password_hash)
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid)
        },
        expiry=None
    )
    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid),
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
    )
    
    response = JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        #"refresh_token": refresh_token,
        "user": {
            "email": user.email,
            "user_uid": str(user.uid)
        }
    })

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True, # Prevents malicious JavaScript from reading the token
        secure=True, # Ensures cookie is only sent over encrypted HTTPS
        samesite="lax", # Balanced CSRF protection (use "strict" if on identical domain)
        path="/api/v1/auth/refresh", # Restricts browser from sending it to other API paths
        max_age=60 * 60 * 24 * REFRESH_TOKEN_EXPIRY    # Tells browser to keep cookie for 7 days (in seconds)
    )

    return response

@auth_router.post('/refresh', response_model=UserModel,status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Depends(refresh_token_bearer)):
    refresh_token_data = decode_access_token(refresh_token)
    return refresh_token_data