from authlib.integrations.starlette_client import OAuth
from backend.config.config import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="yandex",
    client_id=settings.yandex_client_id,
    client_secret=settings.yandex_client_secret,
    access_token_url="https://oauth.yandex.com/token",
    authorize_url="https://oauth.yandex.com/authorize",
    api_base_url="https://login.yandex.ru/info",
    client_kwargs={"scope": "login:email"},
)
