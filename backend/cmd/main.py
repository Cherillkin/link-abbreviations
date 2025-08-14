from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.config.config import settings
from backend.repositories.auth import AuthRepository
from backend.repositories.shortLinks import ShortLinkRepository
from backend.repositories.user import UserRepository
from backend.routing.auth import router as router_auth, get_auth_service
from backend.routing.oauth import router as router_oauth
from backend.routing.shortLinks import (
    router as router_shortlinks,
    get_short_link_service,
)
from backend.routing.user import router as router_user, get_user_service
from backend.services.auth import AuthService
from backend.services.shortLinks import ShortLinkService
from backend.services.user import UserService

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

app.dependency_overrides[get_auth_service] = lambda: auth_service

shortLinks_repository = ShortLinkRepository()
shorLinks_service = ShortLinkService(shortLinks_repository)

app.dependency_overrides[get_short_link_service()] = lambda: shorLinks_service

user_repository = UserRepository()
user_service = UserService(user_repository)

app.dependency_overrides[get_user_service] = lambda: user_service

app.include_router(router_auth)
app.include_router(router_shortlinks)
app.include_router(router_user)
app.include_router(router_oauth)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False
)
