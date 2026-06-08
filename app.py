import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Score de Riesgos",
    layout="wide"
)

st.title("Score de Riesgos")
st.caption("Prototipo de dashboard en Streamlit conectado a Databricks")

st.sidebar.header("Filtros")

fecha_corte = st.sidebar.date_input("Fecha de corte")
nivel_riesgo = st.sidebar.selectbox(
    "Nivel de riesgo",
    ["Todos", "Alto", "Medio", "Bajo"]
)

st.subheader("Resumen ejecutivo")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Clientes evaluados", "24,842")
col2.metric("Riesgo alto", "2,186")
col3.metric("Riesgo medio", "7,842")
col4.metric("Riesgo bajo", "14,814")

st.divider()

st.subheader("Predicciones recientes")

df = pd.DataFrame({
    "numero_cuenta": ["1000001234", "1000001235", "1000001236", "1000001237"],
    "score_riesgo": [742, 612, 428, 689],
    "probabilidad_riesgo": [0.0742, 0.1835, 0.5211, 0.1127],
    "nivel_riesgo": ["Bajo", "Medio", "Alto", "Bajo"],
    "version_modelo": ["v1.0", "v1.0", "v1.0", "v1.0"]
})

if nivel_riesgo != "Todos":
    df = df[df["nivel_riesgo"] == nivel_riesgo]

st.dataframe(df, use_container_width=True)
