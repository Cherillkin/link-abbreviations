from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from backend.databases.postgres import get_db
from backend.repositories.shortLinks import ShortLinkRepository
from backend.schemas.shortLink import ShortLinkInfo, ShortLinkCreate
from backend.services.shortLinks import ShortLinkService
from backend.tasks.shortlinks import generate_qr_code_task
from backend.utils.auth import get_current_user
from backend.models.auth import User
from backend.utils.shortlink import generate_qr_code

router = APIRouter(prefix="/short-links", tags=["ShortLinks"])

def get_short_link_service() -> ShortLinkService:
    return ShortLinkService(ShortLinkRepository())

@router.post("/", responses={400: {"description": "Bad Request"}},
             response_model=ShortLinkInfo, description="Создание ссылки")
async def create_short_link(data: ShortLinkCreate, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user), service: ShortLinkService = Depends(get_short_link_service)):
     link = service.create(db, current_user, data)
     return ShortLinkInfo(
         short_code=link.short_code,
         original_url=link.original_url,
         created_at=link.created_at,
         expires_at=link.expires_at,
         click_count=0
     )

@router.get("/{code}", responses={400: {"description": "Bad Request"}},
            response_model=ShortLinkInfo, description="Просмотр информации о ссылке")
def get_link_info(code: str, db: Session = Depends(get_db), service: ShortLinkService = Depends(get_short_link_service)):
    return service.get_info(db, code)

@router.get("/r/{code}", responses={400: {"description": "Bad Request"}}, description="Перенаправление пользователя по новой ссылке")
def redirect_to_original(code: str, request: Request, db: Session = Depends(get_db), service: ShortLinkService = Depends(get_short_link_service)):
    url = service.redirect(db, code, request)
    return RedirectResponse(url=url)

@router.post("/verify-password", responses={400: {"description": "Bad Request"}}, description="Проверка пароля")
def verify_password(code: str, password: str, db: Session = Depends(get_db), service: ShortLinkService = Depends(get_short_link_service)):
    link = service.verify_password_short_link(db, code, password)

    status = "not_protected" if not link.is_protected else "ok"

    return {"status": status, "redirect_url": link.original_url}

@router.post("/{code}/qr", responses={400: {"description": "Bad Request"}}, description="Создания QR-кода")
def generate_qr_for_link(code: str, request: Request, db: Session = Depends(get_db),
                         service: ShortLinkService = Depends(get_short_link_service)):
    link = service.get_info(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    short_url = f"{request.base_url}short-links/r/{link.short_code}"
    task = generate_qr_code_task.delay(short_url)

    return {
        "task_id": task.id,
        "status": "processing"
    }

