from fastapi import Header, HTTPException
from sqlalchemy import text
from app.database import engine

# =========================
# VERIFICAÇÃO DE TOKEN
# =========================
def verify_token(x_isy_token: str = Header(...)):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, nome, token 
                FROM usuarios 
                WHERE token = :token AND ativo = 1
            """),
            {"token": x_isy_token}
        ).fetchone()

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou ausente"
        )

    # retorna usuário (MELHOR PRÁTICA)
    return {
        "id": result[0],
        "nome": result[1],
        "token": result[2]
    }