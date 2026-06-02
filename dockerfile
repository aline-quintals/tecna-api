# =========================
# IMAGEM BASE
# =========================
FROM python:3.11-slim

# =========================
# DIRETÓRIO DE TRABALHO
# =========================
WORKDIR /app

# =========================
# COPIA PROJETO PARA CONTAINER
# =========================
COPY . .

# =========================
# INSTALA DEPENDÊNCIAS
# =========================
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pymysql

# =========================
# EXPOE PORTA DA API
# =========================
EXPOSE 8000

# =========================
# COMANDO PARA RODAR API
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]