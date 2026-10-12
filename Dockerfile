FROM python:3.12-slim

# Evitar archivos .pyc y habilitar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Lima

WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL (psycopg) y zona horaria
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    libpq-dev \
    postgresql-client \
    gcc \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python (soporta requirements.txt del repo real)
COPY requirements*.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi && \
    if [ -f requirements-dev.txt ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

# Copiar el código del proyecto
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]