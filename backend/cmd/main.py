from fastapi import FastAPI

from backend.repositories.auth import AuthRepository
from backend.routing.auth import router as router_auth, get_auth_service
from backend.services.auth import AuthService
from backend.databases.postgres import Base, engine

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")

#Авторизация
auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

app.dependency_overrides[get_auth_service] = lambda: auth_service

app.include_router(router_auth)

Base.metadata.create_all(bind=engine)