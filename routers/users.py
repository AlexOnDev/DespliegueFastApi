from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

# Entidad user
class User(BaseModel): # Al heredar de basemodel tiene capacidad de crear una entidad gracias al BaseModel
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Alejandro", surname="de Pablo", url="http://wikipedia.com",age=22),
         User(id=2,name="Pepe", surname="Perez", url="http://wiki.com",age=22),
         User(id=3,name="Haakon", surname="Dahlberg", url="http://haakon.com",age=20)]

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Alejandro", "apellido":"de Pablo", "url":"http://wikipedia.com", "age":22},
            {"name":"Pepe", "apellido":"Perez", "url":"http://wiki.com", "age":22},
            {"name":"Haakon", "apellido":"Dahlberg", "url":"http://haakon.com", "age":20}]

@router.get("/users")
async def users():
    # return User(name = "Alejandro", surname="de Pablo", url="http://wikipedia.com", age=22)
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int): # FastApi trabaja tipando los datos
    return search_user(id)
    
# Query
@router.get("/user/") # http://127.0.0.1:8000/userquery/?id=1 (query)
async def user(id: int): # FastApi trabaja tipando los datos
    return search_user(id)

# Post  
@router.post("/user/", response_model=User, status_code=201) # Response_model = Respuesta por defecto para documentacion /docs || Codigo de respuesta por defecto status_code
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe") # Si return devuelve un json, si raise usa el status_code
        # return {"error":"El usuario ya existe"}
    
    users_list.append(user)
    return user

# Put     
@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list): # Enumerando para obtener posicion y asi poder modificarlo
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
         return {"error":"No se ha actualizado el usuario"}
    
    return user

# Delete
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list): 
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
         return {"error":"No se ha eliminado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id ==id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}

