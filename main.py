from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# python -m uvicorn main:app --reload
app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)



app.mount("/static", StaticFiles(directory="static"), name="static") # Para exponer recursos estáticos. Ruta url, Ruta local archivo 

@app.get("/")
async def root():
    return "¡Hola FastApi!"

@app.get("/url")
async def url():
    return { "url":"https://cursos.com" }

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc