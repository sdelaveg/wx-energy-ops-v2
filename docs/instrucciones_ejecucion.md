# Instrucciones de Ejecución del Contenedor Docker (wx-energy-ops:v1.0.0)

## 1. Construcción de la Imagen (docker build)
```bash
docker build -t wx-energy-ops:v1.0.0 .
```

## 2. Ejecución del Contenedor (docker run)
* **Puerto expuesto:** `8000` (TCP)
* **Variables de entorno soportadas:**
  * `MODEL_THRESHOLD`: Umbral de decisión probabilístico (por defecto `0.30`).
  * `PORT`: Puerto de escucha de Uvicorn (por defecto `8000`).
* **Usuario de ejecución interna:** `appuser` (UID `10001`, sin privilegios de `root`).

```bash
docker run -d --name bbva-hvac-api -p 8000:8000 -e MODEL_THRESHOLD=0.30 wx-energy-ops:v1.0.0
```

## 3. Comandos de Verificación y Evidencia
```bash
docker ps --filter "name=bbva-hvac-api"
docker logs bbva-hvac-api
curl -s http://localhost:8000/health
```
