from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.repositories.auth import AuthRepository
from backend.repositories.shortLinks import ShortLinkRepository
from backend.routing.auth import router as router_auth, get_auth_service
from backend.routing.shortLinks import router as router_shortlinks, get_link_info
from backend.services.auth import AuthService
from backend.services.shortLinks import ShortLinkService

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")

#Авторизация
auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

app.dependency_overrides[get_auth_service] = lambda: auth_service

shortLinks_repository = ShortLinkRepository()
shorLinks_service = ShortLinkService(shortLinks_repository)

app.dependency_overrides[get_link_info] = lambda: shorLinks_service

app.include_router(router_auth)
app.include_router(router_shortlinks)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
