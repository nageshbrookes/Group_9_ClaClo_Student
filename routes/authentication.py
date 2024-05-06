
from config.database import users
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="authenticate")

class createuserReq(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    status: str


@router.post("/user", tags=['Authentication'], status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: createuserReq):
    createUserModel = {
        'username' : create_user_req.username,
        'hasedpassword' : bcrypt_context.hash(create_user_req.password)
    }
    users.insert_one(dict(createUserModel))
    return 'User is successfully created'


@router.post("/authenticate", tags=['Authentication'])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # token expires after ACCESS_TOKEN_EXPIRE_MINUTES minites
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        user, expires_delta=access_token_expires
    )
    print(access_token)
    return Token(access_token=access_token, token_type="bearer", status= 'Authentication is Success')


# fetch the details and authenticate the user returns userName
def authenticate_user(username: str, password: str):
    user = users.find_one({"username": username})

    passwordHashed = user.get('hasedpassword') 
    userName = user.get('username') 

    if not user:
        return False
    if not bcrypt_context.verify(password, passwordHashed):
        return False
    return userName


# Acreating access token based on time and username
def create_access_token(username: str, expires_delta):
    encode = {'sub': username}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception     
    except JWTError:
        raise credentials_exception
    return username