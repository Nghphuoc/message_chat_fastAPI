from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette import status
from depends.dependecy import user_service
from model.schema import LoginRequest, TokenData, UserRequest, UserResponse
from service.UserService import UserService
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os
load_dotenv()


router= APIRouter(prefix="/api/auth", tags=["Auth"])
# encoder = CryptContext(schemes=["bcrypt"], deprecated="auto") lap personal
encoder = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


#Check Token and get user, role
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Invalid authentication credentials",
                                          headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role : str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
        return token_data
    except JWTError:
        raise credentials_exception


# Check Admin
def is_admin(user: TokenData = Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này."
        )
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
def auth(login: LoginRequest, service: UserService = Depends(user_service)):
    user = service.get_user_by_email(login.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not encoder.verify(login.password, user.password):
        raise HTTPException(status_code=500, detail="Incorrect password")
    access_token = generate_token(data={"sub": user.username, "role": user.role.role_name.value})
    return {"access_token": access_token, "infor_user": user, "token_type": "bearer"}


@router.post("/register",status_code=status.HTTP_201_CREATED, response_model= UserResponse)
async def create_user_control(user: UserRequest ,service: UserService = Depends(user_service)):
    try:
        user_data = service.add_user(user)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})


@router.put("/forgot_password", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def for_got_password(email: str, password: str, new_password: str, service: UserService = Depends(user_service)):
    try:
        service.for_got_password(email, password, new_password)
        return {"message": "update password successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})