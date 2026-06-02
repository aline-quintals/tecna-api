from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from app.database import engine

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(request: Request):

    with engine.connect() as conn:

        total_scripts = conn.execute(
            text("SELECT COUNT(*) FROM scripts")
        ).scalar()

        total_logs = conn.execute(
            text("SELECT COUNT(*) FROM logs_execucao")
        ).scalar()

        logs = conn.execute(
             text("""
               SELECT
               l.id,
               u.nome AS usuario,
               s.nome AS script,
               l.status,
               l.data_execucao
               FROM logs_execucao l
               JOIN usuarios u
               ON l.usuario_id = u.id
               JOIN scripts s
               ON l.script_id = s.id
               ORDER BY l.data_execucao DESC
               LIMIT 10
           """)
        ).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_scripts": total_scripts,
            "total_logs": total_logs,
            "logs": logs
        }
    )