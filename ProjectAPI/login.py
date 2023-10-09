from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

algoritmo = "HS256"
access_token_time = 1
secret = "f071ac63ffdfb206ddf4890afac9b72ef5e21509d1a79b33c643f0ee492bd36e"
app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt =CryptContext(schemes=["bcrypt"])

class user(BaseModel):
    username: str
    email: str
    disabled: bool
class usersdb(user):
    password: str


userdb ={
    "admin":{
        "username": "admin",
        "email": "admin@gmail.com",
        "disabled": False,
        "password": "$2a$12$mZ6mQc3GNCJBa5e2Wo0DMOkkrCtREQPakAunduUwA7xQNAPCZcXv."
    },
    "admin2":{
        "username": "admin2",
        "email": "admin2@gmail.com",
        "disabled": True,
        "password": "$2a$12$mZ6mQc3GNCJBa5e2Wo0DMOkkrCtREQPakAunduUwA7xQNAPCZcXv."
    }
}

def searchuser_db(username: str):
    if username in userdb:
        return usersdb(**userdb[username])
def searchuser(username: str):
    if username in userdb:
        return user(**userdb[username])
    
async def auth(token: str = Depends(oauth2)):
    try:
        usere = jwt.decode(token, secret, algorithms=[algoritmo]).get("sub")
        if usere is None:
            return {"error": "user not found"}
    
    except JWTError:
        return {"error": "user not found"}
    
    return searchuser(usere)


async def currentuser(user: user = Depends(auth)):
    if user.disabled:
        return {"error": "inactive"}
    return user
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userdb1 = userdb.get(form.username)
    if not userdb1:
        return {"error": "user not found"}
    user = searchuser_db(form.username)
    if not crypt.verify(form.password, user.password):
        return {"Error": "contraseña incorrecta"}
    accesstoken = {"sub":user.username, "exp": datetime.utcnow() + timedelta(minutes=access_token_time)}
    return {"access_token": jwt.encode(accesstoken,secret, algorithm=algoritmo),  "token_type": "bearer"}

@app.get("/user/me")
async def me(user: user = Depends(currentuser)):
    return user