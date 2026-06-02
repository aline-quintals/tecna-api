from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
import subprocess
from app.database import engine
from app.auth import verify_token
from app.services import save_log
from app.scripts_api import router as scripts_router
from app.logs_api import router as logs_router

# =========================
# APP
# =========================
app = FastAPI(
    title="TECNA API",
    version="1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)
app = FastAPI(
    title="TECNA API",
    version="1.0"
)

app.include_router(scripts_router)
app.include_router(logs_router)


# =========================
# MODELO
# =========================
class ExecuteRequest(BaseModel):
    script_id: int


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "project": "TECNA",
            "status": "online",
            "database": "conectado"
        }

    except Exception as e:
        return {
            "project": "TECNA",
            "status": "erro",
            "message": str(e)
        }


# =========================
# EXECUÇÃO DE SCRIPT
# =========================
@app.post("/execute")
def execute_script(
    payload: ExecuteRequest,
    user=Depends(verify_token)   # <-- AGORA ISSO É O USUÁRIO
):

    script_id = payload.script_id

    # =========================
    # 1. BUSCAR SCRIPT ATIVO
    # =========================
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT caminho 
                FROM scripts 
                WHERE id = :id AND ativo = 1
            """),
            {"id": script_id}
        ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Script não encontrado ou inativo"
        )

    script_path = result[0]


    # =========================
    # 2. EXECUTAR SCRIPT
    # =========================
    try:
        exec_result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True
        )

        status = "success"
        stdout = exec_result.stdout
        stderr = exec_result.stderr

    except Exception as e:
        status = "error"
        stdout = ""
        stderr = str(e)


    # =========================
    # 3. PEGAR USUÁRIO (CORRETO AGORA)
    # =========================
    usuario_id = user["id"]
    usuario_nome = user["nome"]


    # =========================
    # 4. SALVAR LOG
    # =========================
    print("========== DEBUG ==========")
    print("USUARIO:", usuario_id)
    print("SCRIPT:", script_id)
    print("STATUS:", status)
    print("===========================")

    save_log(
        usuario_id=usuario_id,
        script_id=script_id,
        status=status,
        stdout=stdout,
        stderr=stderr
    )

    # =========================
    # 5. RESPONSE
    # =========================
    return {
        "status": status,
        "script_id": script_id,
        "usuario_id": usuario_id,
        "usuario_nome": usuario_nome,
        "stdout": stdout,
        "stderr": stderr
    }