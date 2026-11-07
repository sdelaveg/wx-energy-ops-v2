import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="BBVA Smart HVAC OPEX", layout="wide")
st.title("🏢 BBVA Facility Management — Simulador Predictivo HVAC (OPEX)")
st.markdown("Interfaz ejecutiva conectada al microservicio FastAPI (`/predict` y `/health`).")

with st.sidebar:
    st.header("Estado del Servicio API")
    if st.button("Verificar /health"):
        try:
            r = requests.get(f"{API_URL}/health", timeout=5)
            st.success(f"HTTP {r.status_code} - Servicio Activo")
            st.json(r.json())
        except Exception as e:
            st.error(f"Error conectando a {API_URL}: {e}")

col1, col2 = st.columns(2)
with col1:
    compacidad = st.slider("Compacidad Relativa", 0.60, 0.98, 0.76, 0.01)
    superficie = st.number_input("Área de Superficie (m²)", 500.0, 850.0, 661.5, 5.0)
    pared = st.number_input("Área de Pared (m²)", 240.0, 420.0, 318.5, 5.0)
    techo = st.number_input("Área de Techo (m²)", 110.0, 225.0, 122.5, 2.5)
with col2:
    altura = st.selectbox("Altura Total (m)", [3.5, 7.0], index=1)
    orientacion = st.selectbox("Orientación (2=N, 3=E, 4=S, 5=O)", [2, 3, 4, 5], index=0)
    acristalamiento = st.selectbox("Proporción de Acristalamiento", [0.0, 0.1, 0.25, 0.4], index=1)
    dist_acrist = st.selectbox("Distribución de Acristalamiento", [0, 1, 2, 3, 4, 5], index=1)

if st.button("Ejecutar Diagnóstico Predictivo (/predict)", type="primary"):
    payload = {
        "Compacidad_Relativa": compacidad,
        "Area_Superficie": superficie,
        "Area_Pared": pared,
        "Area_Techo": techo,
        "Altura_Total": altura,
        "Orientacion": orientacion,
        "Area_Acristalamiento": acristalamiento,
        "Distribucion_Acristalamiento": dist_acrist
    }
    res = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
    if res.status_code == 200:
        data = res.json()
        st.subheader(data["etiqueta_operativa"])
        st.metric("Probabilidad de Sobreconsumo Crítico", f"{data['probabilidad_critico']*100:.2f}%")
        st.json(data)
    else:
        st.error(f"Error HTTP {res.status_code}: {res.text}")
