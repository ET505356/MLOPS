import streamlit as st
import pandas as pd
from databricks import sql

st.set_page_config(
    page_title="Score de Riesgos",
    layout="wide"
)

st.title("Score de Riesgos")
st.caption("Prueba de conexión Streamlit → Databricks")

st.sidebar.header("Filtros")

nivel_riesgo = st.sidebar.selectbox(
    "Nivel de riesgo",
    ["Todos", "Alto", "Medio", "Bajo"]
)

# ======================================================
# 1. Validación de secrets
# ======================================================

st.subheader("Validación de Secrets")

try:
    server_hostname = st.secrets["databricks"]["server_hostname"]
    http_path = st.secrets["databricks"]["http_path"]
    access_token = st.secrets["databricks"]["access_token"]

    st.success("Se encontró la sección [databricks] en los secrets.")

    col1, col2, col3 = st.columns(3)

    col1.metric("server_hostname", "Cargado" if server_hostname else "Vacío")
    col2.metric("http_path", "Cargado" if http_path else "Vacío")
    col3.metric("access_token", "Cargado" if access_token else "Vacío")

    st.write("**server_hostname leído:**")
    st.code(server_hostname)

    st.write("**http_path leído:**")
    st.code(http_path)

    st.write("**access_token leído:**")
    if access_token:
        st.code(f"{access_token[:6]}...{access_token[-4:]}")
    else:
        st.code("Token vacío")

except Exception as e:
    st.error("No se pudieron leer los secrets.")
    st.exception(e)
    st.stop()


# ======================================================
# 2. Validaciones básicas de formato
# ======================================================

st.subheader("Validación de formato")

errores_formato = []

if server_hostname.startswith("https://"):
    errores_formato.append("El server_hostname NO debe incluir https://")

if server_hostname.endswith("/"):
    errores_formato.append("El server_hostname NO debe terminar con /")

if not http_path.startswith("/sql/"):
    errores_formato.append("El http_path normalmente debe empezar con /sql/")

if not access_token:
    errores_formato.append("El access_token está vacío")

if errores_formato:
    for error in errores_formato:
        st.warning(error)
else:
    st.success("El formato básico de los secrets parece correcto.")


# ======================================================
# 3. Consulta a Databricks
# ======================================================

st.subheader("Prueba de conexión a Databricks")

tabla = "score_riesgos.scoring.score_riesgo_predicciones"

query = f"""
SELECT
    numero_cuenta,
    score_riesgo,
    probabilidad_riesgo,
    nivel_riesgo,
    version_modelo
FROM {tabla}
"""

st.write("**Tabla consultada:**")
st.code(tabla)

st.write("**Query ejecutado:**")
st.code(query, language="sql")


@st.cache_data(ttl=300)
def cargar_datos_desde_databricks():
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    ) as connection:
        return pd.read_sql(query, connection)


try:
    df = cargar_datos_desde_databricks()

    st.success("Conexión exitosa. Datos leídos desde Databricks.")

    if nivel_riesgo != "Todos":
        df = df[df["nivel_riesgo"] == nivel_riesgo]

    st.subheader("Resumen ejecutivo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Clientes evaluados", f"{len(df):,}")
    col2.metric("Riesgo alto", f"{len(df[df['nivel_riesgo'] == 'Alto']):,}")
    col3.metric("Riesgo medio", f"{len(df[df['nivel_riesgo'] == 'Medio']):,}")
    col4.metric("Riesgo bajo", f"{len(df[df['nivel_riesgo'] == 'Bajo']):,}")

    st.divider()

    st.subheader("Predicciones desde Databricks")

    st.dataframe(
        df.sort_values("score_riesgo", ascending=False),
        use_container_width=True
    )

except Exception as e:
    st.error("No fue posible conectarse a Databricks o consultar la tabla.")

    st.info(
        """
        Revisa lo siguiente:
        
        1. Que el SQL Warehouse esté encendido.
        2. Que server_hostname no tenga https://.
        3. Que http_path sea el del SQL Warehouse.
        4. Que el token esté vigente.
        5. Que tu usuario tenga permisos sobre score_riesgos.scoring.score_riesgo_predicciones.
        6. Que la organización permita conexiones externas desde Streamlit Cloud.
        """
    )

    st.exception(e)
