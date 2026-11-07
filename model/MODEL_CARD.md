# Model Card — Clasificador de Sobreconsumo Crítico HVAC (v2.0-champion-rf)

* **Autor:** Sergio Eduardo de la Vega Herrera
* **Algoritmo:** `Pipeline(SimpleImputer(median) -> StandardScaler -> RandomForestClassifier(n_estimators=150, max_depth=6))`
* **Caso de Uso:** Prevención de fugas OPEX por climatización en inmuebles corporativos de BBVA México.
* **Métricas en Test (u = 0.30):** ROC-AUC = `0.9785`, Recall = `0.8710`, Precisión = `0.8438`, F2-Score = `0.8654`, Brier Score = `0.0529`.
* **Alcance y Limitaciones:** Entrenado sobre el dataset paramétrico *UCI Energy Efficiency* (N = 768, licencia CC BY 4.0). No incorpora aún telemetría IoT de ocupación dinámica en tiempo real.
* **Consideración Ética:** Diseñado exclusivamente para asignación preventiva de presupuesto OPEX/CAPEX; prohibido su uso punitivo hacia gerentes de sucursal.
