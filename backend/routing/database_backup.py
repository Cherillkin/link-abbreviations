from backend.utils.database_backup import database_backup
from backend.config.config import settings
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Backup"])

@router.post("/backup")
def create_backup() -> Dict[str, Any]:
    return database_backup(
        db_name=settings.postgres_db,
        user=settings.postgres_user,
        output_dir="backend/backups",
        host=settings.postgres_host,
        port=settings.postgres_port
    )
