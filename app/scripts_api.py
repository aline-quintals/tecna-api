from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from app.database import engine
from app.auth import verify_token

router = APIRouter(prefix="/scripts", tags=["Scripts"])


# =========================
# MODELO
# =========================
class ScriptCreate(BaseModel):
    nome: str
    descricao: str
    caminho: str


class ScriptUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    caminho: str | None = None
    ativo: bool | None = None


# =========================
# LISTAR SCRIPTS
# =========================
@router.get("/")
def list_scripts(auth: bool = Depends(verify_token)):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM scripts")
        ).fetchall()

    return {"scripts": [dict(row._mapping) for row in result]}


# =========================
# BUSCAR POR ID
# =========================
@router.get("/{script_id}")
def get_script(script_id: int, auth: bool = Depends(verify_token)):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM scripts WHERE id = :id"),
            {"id": script_id}
        ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Script não encontrado")

    return dict(result._mapping)


# =========================
# CRIAR SCRIPT
# =========================
@router.post("/")
def create_script(data: ScriptCreate, auth: bool = Depends(verify_token)):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO scripts (nome, descricao, caminho, ativo)
                VALUES (:nome, :descricao, :caminho, TRUE)
            """),
            data.dict()
        )

    return {"status": "created", "message": "Script criado com sucesso"}


# =========================
# ATUALIZAR SCRIPT
# =========================
@router.put("/{script_id}")
def update_script(script_id: int, data: ScriptUpdate, auth: bool = Depends(verify_token)):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE scripts
                SET 
                    nome = COALESCE(:nome, nome),
                    descricao = COALESCE(:descricao, descricao),
                    caminho = COALESCE(:caminho, caminho),
                    ativo = COALESCE(:ativo, ativo)
                WHERE id = :id
            """),
            {"id": script_id, **data.dict()}
        )

    return {"status": "updated", "script_id": script_id}


# =========================
# DESATIVAR SCRIPT (SOFT DELETE)
# =========================
@router.delete("/{script_id}")
def deactivate_script(script_id: int, auth: bool = Depends(verify_token)):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE scripts
                SET ativo = FALSE
                WHERE id = :id
            """),
            {"id": script_id}
        )

    return {"status": "deactivated", "script_id": script_id}