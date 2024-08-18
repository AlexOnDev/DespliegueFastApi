from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "alexondev":{ # Clave valor
          "username": "alexondev",
          "full_name": "Alejandro de Pablo",
          "email": "alejandromelagarrasconlamano@jaja.com",
          "disabled": False,
          "password": "123456"
    },
      "alexondev2":{
          "username": "alexondev2",
          "full_name": "Alejandro de Pablo 2",
          "email": "2alejandromelagarrasconlamano2@jaja.com",
          "disabled": True,
          "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db: # Clave = username
        return UserDB(**users_db[username]) #Indicar que pueden ir varios por el constructor de BaseModel
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = "Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): # Recibe datos pero no dependen de nadie?
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)): # Devolvemos el que no tiene contraseña xd
    return user