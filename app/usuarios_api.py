from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from app.database import engine
from app.auth import verify_token

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


class TokenUpdate(BaseModel):
    novo_token: str


@router.put("/{usuario_id}/token")
def update_token(
    usuario_id: int,
    data: TokenUpdate,
    user=Depends(verify_token)
):
    
    if user["id"] != 1:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem alterar tokens"
        )

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE usuarios
                SET token = :token
                WHERE id = :id
            """),
            {
                "id": usuario_id,
                "token": data.novo_token
            }
        )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "status": "success",
        "message": "Token atualizado",
        "usuario_id": usuario_id
    }