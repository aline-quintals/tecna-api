from fastapi import Depends, Header, HTTPException, FastAPI
from sqlalchemy import text
from app.database import engine
import subprocess

# =========================
# CRIA A API PRINCIPAL
# =========================
app = FastAPI(
    title="TECNA API",
    version="1.0"
)

# Caminho do script que será executado
SCRIPT_PATH = "scripts/teste.sh"


# =========================
# ROTA DE TESTE / SAÚDE DA API
# =========================
@app.get("/")
def home():
    try:
        # Testa conexão com o banco (SELECT 1)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "project": "TECNA",
            "database": "conectado",
            "status": "online"
        }

    except Exception as e:
        return {
            "project": "TECNA",
            "database": "erro",
            "message": str(e)
        }


# =========================
# VERIFICAÇÃO DO TOKEN (X-Isy-Token)
# =========================
def verify_token(x_isy_token: str = Header(...)):
    """
    Valida o token enviado no HEADER contra o banco de dados
    """

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT token FROM usuarios WHERE id = 1")
        ).fetchone()

    if not result or result[0] != x_isy_token:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")

    return True


# =========================
# ROTA PRINCIPAL
# EXECUTA SCRIPT SHELL
# =========================
@app.post("/execute")
def execute_script(auth: bool = Depends(verify_token)):

    # -------------------------
    # 1. EXECUÇÃO DO SCRIPT
    # -------------------------
    try:
        result = subprocess.run(
            ["bash", SCRIPT_PATH],
            capture_output=True,
            text=True
        )

        status = "success"
        stdout = result.stdout
        stderr = result.stderr

    except Exception as e:
        status = "error"
        stdout = ""
        stderr = str(e)

    # -------------------------
    # 2. DEBUG (terminal)
    # -------------------------
    print("DEBUG STATUS:", status)
    print("DEBUG STDOUT:", stdout)
    print("DEBUG STDERR:", stderr)

    # -------------------------
    # 3. SALVAR LOG NO BANCO
    # -------------------------
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO logs_execucao 
                    (usuario_id, script_id, status, stdout, stderr)
                    VALUES (:usuario_id, :script_id, :status, :stdout, :stderr)
                """),
                {
                    "usuario_id": 1,
                    "script_id": 1,
                    "status": status,
                    "stdout": stdout,
                    "stderr": stderr
                }
            )

        print("DEBUG: INSERT OK")

    except Exception as db_error:
        print("DEBUG DB ERROR:", db_error)

    # -------------------------
    # 4. RESPOSTA DA API
    # -------------------------
    return {
        "status": status,
        "stdout": stdout,
        "stderr": stderr
    }

