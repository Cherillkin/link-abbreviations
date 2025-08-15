from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import List, Union

from backend.databases.postgres import get_db
from backend.models import ShortLink
from backend.repositories.shortLinks import ShortLinkRepository
from backend.schemas.shortLink import (
    ShortLinkInfo,
    ShortLinkCreate,
    ShortLinkInfoWithClick,
)
from backend.services.shortLinks import ShortLinkService
from backend.tasks.shortlinks import generate_qr_code_task
from backend.utils.auth import get_current_user
from backend.models.auth import User
from backend.utils.shortlink import generate_qr_code

router = APIRouter(prefix="/short-links", tags=["ShortLinks"])


def get_short_link_service() -> ShortLinkService:
    return ShortLinkService(ShortLinkRepository())


@router.post(
    "/",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    response_model=ShortLinkInfo,
    description="Создание ссылки",
)
async def create_short_link(
    data: ShortLinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: ShortLinkService = Depends(get_short_link_service),
) -> ShortLinkInfo:
    link = service.create(db, current_user, data)
    return ShortLinkInfo(
        short_code=link.short_code,
        original_url=link.original_url,
        created_at=link.created_at,
        expires_at=link.expires_at,
        click_count=0,
    )


@router.get(
    "/{code}",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    response_model=ShortLinkInfoWithClick,
    description="Просмотр информации о ссылке",
)
def get_link_info(
    code: str,
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> ShortLinkInfoWithClick:
    return service.get_info(db, code)


@router.get(
    "/",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    response_model=List[ShortLinkInfo],
    description="Получение всех коротких кодов",
)
def get_links_code(
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> List[ShortLinkInfo]:
    return service.get_all_links_code(db)


@router.get(
    "/r/{code}",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    description="Перенаправление пользователя по новой ссылке",
)
def redirect_to_original(
    code: str,
    request: Request,
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> RedirectResponse:
    url = service.redirect(db, code, request)
    return RedirectResponse(url=url)


@router.get(
    "/stats/top-links",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    description="Статистика ссылок",
)
def get_top_links_stats(
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> List:
    return service.get_top_links_stats(db)


@router.post(
    "/verify-password",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    description="Проверка пароля",
)
def verify_password(
    code: str,
    password: str,
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> dict:
    link: Union[dict, ShortLink] = service.verify_password_short_link(
        db, code, password
    )

    if isinstance(link, dict):
        return link

    # иначе это ShortLink
    status = "not_protected" if not link.is_protected else "ok"
    return {"status": status, "redirect_url": link.original_url}


@router.post(
    "/{code}/qr",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
    description="Создание QR-кода",
)
def generate_qr_for_link(
    code: str,
    request: Request,
    db: Session = Depends(get_db),
    service: ShortLinkService = Depends(get_short_link_service),
) -> dict:
    link = service.get_info(db, code)

    short_url = f"{request.base_url}short-links/r/{link.short_code}"
    qr_base64 = generate_qr_code(short_url)

    return {"qr_code": f"data:image/png;base64,{qr_base64}"}
