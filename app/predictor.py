import os
import json
import time
import joblib
import pandas as pd

class HVACPredictorService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.getenv("MODEL_PATH", os.path.join(base_dir, "model", "champion_rf_v2.joblib"))
        meta_path = os.getenv("META_PATH", os.path.join(base_dir, "model", "model_metadata.json"))

        self.pipeline = joblib.load(model_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.threshold = float(os.getenv("MODEL_THRESHOLD", self.metadata.get("optimal_threshold", 0.30)))
        self.version = self.metadata.get("model_version", "v2.0-champion-rf")
        self.features = self.metadata.get("features")
        self.costo_fn = float(self.metadata.get("cost_fn_usd", 2500.0))
        self.costo_fp = float(self.metadata.get("cost_fp_usd", 250.0))

    def predict_single(self, payload_dict: dict) -> dict:
        t0 = time.perf_counter()
        df_in = pd.DataFrame([payload_dict])[self.features]
        prob = float(self.pipeline.predict_proba(df_in)[0, 1])
        clase = int(prob >= self.threshold)
        latencia = (time.perf_counter() - t0) * 1000.0

        if clase == 1:
            etiqueta = "Sobreconsumo Crítico HVAC (Alerta Activa)"
            accion = "Despachar cuadrilla para inspección termográfica y ajuste de setpoints"
            costo_intervencion = self.costo_fp
            riesgo_mitigado = self.costo_fn
            ahorro_neto_esperado = round((prob * self.costo_fn) - self.costo_fp, 2)
        else:
            etiqueta = "Operación Normal Eficiente"
            accion = "Mantener monitoreo continuo estándar sin despacho a sitio"
            costo_intervencion = 0.0
            riesgo_mitigado = 0.0
            ahorro_neto_esperado = 0.0

        return {
            "prediccion_clase": clase,
            "etiqueta_operativa": etiqueta,
            "probabilidad_critico": round(prob, 4),
            "umbral_aplicado": self.threshold,
            "version_modelo": self.version,
            "evaluacion_opex": {
                "accion_recomendada": accion,
                "costo_inspeccion_usd": costo_intervencion,
                "riesgo_fuga_fn_usd": riesgo_mitigado,
                "beneficio_neto_esperado_usd": ahorro_neto_esperado
            },
            "latencia_ms": round(latencia, 3)
        }
