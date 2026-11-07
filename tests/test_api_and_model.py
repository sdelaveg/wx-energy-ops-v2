from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_01_health_endpoint():
    """Verifica disponibilidad del servicio /health y versión del modelo."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert data["model_version"] == "v2.0-champion-rf"
    assert data["active_threshold"] == 0.30

def test_02_funcional_1_sucursal_eficiente_clase_0():
    """Caso Funcional 1: Edificio de 1 nivel (3.5m) altamente eficiente -> Clase 0."""
    payload = {
        "Compacidad_Relativa": 0.62, "Area_Superficie": 808.5, "Area_Pared": 367.5,
        "Area_Techo": 220.5, "Altura_Total": 3.5, "Orientacion": 2,
        "Area_Acristalamiento": 0.10, "Distribucion_Acristalamiento": 1
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["prediccion_clase"] == 0
    assert data["probabilidad_critico"] < 0.30

def test_03_funcional_2_corporativo_critico_clase_1():
    """Caso Funcional 2: Corporativo 2 niveles (7.0m) con alto acristalamiento (0.40) -> Clase 1."""
    payload = {
        "Compacidad_Relativa": 0.79, "Area_Superficie": 637.0, "Area_Pared": 343.0,
        "Area_Techo": 147.0, "Altura_Total": 7.0, "Orientacion": 2,
        "Area_Acristalamiento": 0.40, "Distribucion_Acristalamiento": 2
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["prediccion_clase"] == 1
    assert data["probabilidad_critico"] >= 0.80
    assert data["evaluacion_opex"]["costo_inspeccion_usd"] == 250.0

def test_04_funcional_3_sensibilidad_umbral_operativo():
    """Caso Funcional 3: Inmueble compacto de 2 niveles con acristalamiento medio (0.25) -> Clase 1."""
    payload = {
        "Compacidad_Relativa": 0.90, "Area_Superficie": 563.5, "Area_Pared": 318.5,
        "Area_Techo": 122.5, "Altura_Total": 7.0, "Orientacion": 4,
        "Area_Acristalamiento": 0.25, "Distribucion_Acristalamiento": 3
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["prediccion_clase"] == 1
    assert data["umbral_aplicado"] == 0.30

def test_05_funcional_4_tipologia_limitrofe_inspeccion_preventiva():
    """Caso Funcional 4: Tipología limítrofe (Caso forense Act 6: Compacidad 0.76, Altura 7.0, Acrist 0.1)."""
    payload = {
        "Compacidad_Relativa": 0.76, "Area_Superficie": 661.5, "Area_Pared": 416.5,
        "Area_Techo": 122.5, "Altura_Total": 7.0, "Orientacion": 5,
        "Area_Acristalamiento": 0.10, "Distribucion_Acristalamiento": 3
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["prediccion_clase"] == 1
    assert data["version_modelo"] == "v2.0-champion-rf"

def test_06_extremo_1_valores_limite_dominio_sin_ventanas():
    """Caso Extremo 1 (Valor Límite): Máxima compacidad (0.98), mínima superficie (514.5) y 0% ventanas."""
    payload = {
        "Compacidad_Relativa": 0.98, "Area_Superficie": 514.5, "Area_Pared": 294.0,
        "Area_Techo": 110.25, "Altura_Total": 7.0, "Orientacion": 2,
        "Area_Acristalamiento": 0.0, "Distribucion_Acristalamiento": 0
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 0.0 <= data["probabilidad_critico"] <= 1.0

def test_07_extremo_2_combinacion_fisica_contradictoria():
    """Caso Extremo 2 (Combinación Inusual): Compacidad máxima (0.98) con Superficie máxima (808.5) y Altura mínima (3.5)."""
    payload = {
        "Compacidad_Relativa": 0.98, "Area_Superficie": 808.5, "Area_Pared": 416.5,
        "Area_Techo": 220.5, "Altura_Total": 3.5, "Orientacion": 5,
        "Area_Acristalamiento": 0.40, "Distribucion_Acristalamiento": 5
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["prediccion_clase"] in [0, 1]

def test_08_extremo_3_fuera_de_rango_negativo_y_exceso():
    """Caso Extremo 3 (Fuera de Rango): Area_Superficie negativa (-150) y Acristalamiento > 1.0 (1.85) -> HTTP 422."""
    payload = {
        "Compacidad_Relativa": 0.76, "Area_Superficie": -150.0, "Area_Pared": 318.5,
        "Area_Techo": 122.5, "Altura_Total": 7.0, "Orientacion": 2,
        "Area_Acristalamiento": 1.85, "Distribucion_Acristalamiento": 1
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 422

def test_09_extremo_4_campo_faltante_json_incompleto():
    """Caso Extremo 4 (Campo Faltante): JSON sin Area_Superficie ni Compacidad_Relativa -> HTTP 422 sin caída."""
    payload = {
        "Area_Pared": 318.5, "Area_Techo": 122.5, "Altura_Total": 7.0,
        "Orientacion": 2, "Area_Acristalamiento": 0.25, "Distribucion_Acristalamiento": 2
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 422

def test_10_extremo_5_tipo_dato_incorrecto_texto():
    """Caso Extremo 5 (Tipo Incorrecto): Cadena de texto en campo numérico Altura_Total -> HTTP 422."""
    payload = {
        "Compacidad_Relativa": 0.76, "Area_Superficie": 661.5, "Area_Pared": 318.5,
        "Area_Techo": 122.5, "Altura_Total": "siete_metros_texto", "Orientacion": 2,
        "Area_Acristalamiento": 0.25, "Distribucion_Acristalamiento": 2
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 422
