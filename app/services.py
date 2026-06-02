from sqlalchemy import text
from app.database import engine
import traceback


# =========================
# USUÁRIO POR TOKEN
# =========================
def get_user_by_token(token: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, nome, token
                FROM usuarios
                WHERE token = :token
                AND ativo = 1
            """),
            {"token": token}
        ).fetchone()

    return result


# =========================
# SCRIPTS
# =========================
def list_scripts_db():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM scripts")
        ).fetchall()

    return result


def get_script_by_id(script_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM scripts
                WHERE id = :id
            """),
            {"id": script_id}
        ).fetchone()

    return result


# =========================
# LOGS
# =========================
def save_log(usuario_id, script_id, status, stdout, stderr):
    try:
        print("========== DEBUG LOG ==========")
        print("usuario_id:", usuario_id)
        print("script_id:", script_id)
        print("status:", status)
        print("================================")

        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO logs_execucao
                    (
                        usuario_id,
                        script_id,
                        status,
                        stdout,
                        stderr
                    )
                    VALUES
                    (
                        :usuario_id,
                        :script_id,
                        :status,
                        :stdout,
                        :stderr
                    )
                """),
                {
                    "usuario_id": usuario_id,
                    "script_id": script_id,
                    "status": status,
                    "stdout": stdout,
                    "stderr": stderr
                }
            )

        print("✅ LOG SALVO COM SUCESSO")

    except Exception:
        import traceback
        print("❌ ERRO AO SALVAR LOG")
        traceback.print_exc()