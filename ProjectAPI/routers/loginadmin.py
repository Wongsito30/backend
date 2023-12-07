from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

page_models.Base.metadata.create_all(bind=engine)
app = APIRouter()
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def get_adminlog():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class adminini(BaseModel):
    admin: str
    estado: int

    class Config:
       from_attributes = True
class adminps(adminini):
    contrasena: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return adminps(**user_dict)


def authenticate_admin(admin: str, password: str, db:session=Depends(get_adminlog)):
    admin = db.query(page_models.Admin).filter(page_models.Admin.admin == admin).first()
    if not admin:
        return False
    if not verify_password(password, admin.contrasena):
        return False
    return admin


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)], db:session=Depends(get_adminlog)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin: str = payload.get("sub")
        if admin is None:
            raise credentials_exception
        token_data = TokenData(username=admin)
    except JWTError:
        raise credentials_exception
    admin = db.query(page_models.Admin).filter(page_models.Admin.admin == admin).first()
    if admin is None:
        raise credentials_exception
    return admin


async def get_current_active_admin(
    current_user: Annotated[adminini, Depends(get_current_admin)]
):
    if current_user == 1 :
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/tokenadmin", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:session=Depends(get_adminlog)
):
    admin = authenticate_admin(form_data.username, form_data.password, db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/admin/me/", response_model=adminini)
async def read_admin_me(
    current_admin: Annotated[adminini, Depends(get_current_active_admin)]
):
    return current_admin


@app.get("/admin/me/items/")
async def read_own_items(
    current_admin: Annotated[adminini, Depends(get_current_active_admin)]
):
    return [{"item_id": "Foo", "owner": current_admin.admin}]