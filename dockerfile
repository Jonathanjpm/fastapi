FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de requisitos primero para aprovechar la cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY src/ ./src/

# Cambiar al directorio src
WORKDIR /app/src

# Exponer el puerto que usa FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]