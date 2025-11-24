# Multi-stage build para optimizar el tamaño de la imagen
FROM python:3.13-slim as builder

# Variables de entorno para construcción
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo temporal
WORKDIR /build

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# ============================================================
# Imagen de producción
# ============================================================
FROM python:3.13-slim as production

# Variables de entorno para ejecución
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/app/.local/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=teamservice.settings

# Crear usuario no-root para seguridad
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Instalar solo dependencias de runtime (sin build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar dependencias de Python desde builder
COPY --from=builder --chown=app:app /root/.local /home/app/.local

# Configurar directorio de trabajo
WORKDIR /app
RUN chown app:app /app

# Cambiar a usuario no-root
USER app

# Copiar código fuente con permisos correctos
COPY --chown=app:app . .

# Crear directorios necesarios
RUN mkdir -p /app/static /app/media /app/logs

# Copiar y configurar script de entrada
COPY --chown=app:app docker/entrypoint_team.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Health check para verificar que el servicio está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8020/ || exit 1

# Exponer puerto
EXPOSE 8020

# Comando por defecto
CMD ["/app/entrypoint.sh"]
