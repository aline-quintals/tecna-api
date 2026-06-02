from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# =========================
# USUÁRIOS
# =========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    token = Column(String(255))
    ativo = Column(Boolean, default=True)


# =========================
# SCRIPTS
# =========================
class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    descricao = Column(Text)
    caminho = Column(String(255))
    ativo = Column(Boolean, default=True)


# =========================
# LOGS DE EXECUÇÃO
# =========================
class LogExecucao(Base):
    __tablename__ = "logs_execucao"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer)
    script_id = Column(Integer)
    data_execucao = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))
    stdout = Column(Text)
    stderr = Column(Text)