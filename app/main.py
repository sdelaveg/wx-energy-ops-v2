import time
from fastapi import FastAPI, HTTPException
from app.schemas import InmuebleInput, PrediccionOutput
from app.predictor import HVACPredictorService

START_TIME = time.time()
predictor_service = HVACPredictorService()

app = FastAPI(
    title="BBVA Facility Management - HVAC OPEX Predictive API",
    description="Servicio MLOps contenerizado para detección temprana de sobreconsumo energético HVAC.",
    version="1.0.0"
)

@app.get("/health", tags=["Monitoreo y Salud"])
def health_check():
    return {
        "status": "healthy",
        "service": "wx-energy-ops-api",
        "model_loaded": predictor_service.pipeline is not None,
        "model_version": predictor_service.version,
        "active_threshold": predictor_service.threshold,
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }

@app.post("/predict", response_model=PrediccionOutput, tags=["Inferencia OPEX"])
def predict_overconsumption(inmueble: InmuebleInput):
    try:
        resultado = predictor_service.predict_single(inmueble.model_dump())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno de inferencia: {str(e)}")
