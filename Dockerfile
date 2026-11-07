# ==============================================================================
# ETAPA 1: Builder de dependencias (Multi-stage build para reducir tamaño final)
# ==============================================================================
FROM python:3.11.8-slim-bookworm AS builder

WORKDIR /build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# ==============================================================================
# ETAPA 2: Imagen de Producción Ligera y Endurecida (Usuario No-Root)
# ==============================================================================
FROM python:3.11.8-slim-bookworm AS production

LABEL maintainer="Sergio Eduardo de la Vega Herrera <sergie@bbva-mlops.mx>"
LABEL version="v1.0.0"
LABEL description="Microservicio Predictivo de Sobreconsumo HVAC - BBVA Facility Management"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_THRESHOLD=0.30 \
    PORT=8000

WORKDIR /app

# Crear grupo y usuario sin privilegios de root (Buenas prácticas de seguridad)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copiar artefactos del proyecto asignando permisos al usuario no-root
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup model/ ./model/
COPY --chown=appuser:appgroup tests/ ./tests/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
