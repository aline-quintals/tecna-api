from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import engine
from app.auth import verify_token

router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


# =========================
# LISTAR LOGS
# =========================
@router.get("/")
def list_logs(auth=Depends(verify_token)):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM logs_execucao
                ORDER BY data_execucao DESC
            """)
        ).fetchall()

    return {
        "logs": [dict(row._mapping) for row in result]
    }