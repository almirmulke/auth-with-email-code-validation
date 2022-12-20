from fastapi import FastAPI

from routes.authentication import auth_router, protected_auth_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(protected_auth_router)
