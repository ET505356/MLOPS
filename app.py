import streamlit as st
import pandas as pd
import plotly.express as px
from databricks import sql

st.set_page_config(
    page_title="Score de Riesgos",
    layout="wide"
)

st.title("Score de Riesgos")
st.caption("Dashboard conectado a Databricks - Unity Catalog")

st.sidebar.header("Filtros")

nivel_riesgo = st.sidebar.selectbox(
    "Nivel de riesgo",
    ["Todos", "Alto", "Medio", "Bajo"]
)

tabla = "score_riesgos.scoring.score_riesgo_predicciones"


@st.cache_data(ttl=300)
def cargar_datos():
    server_hostname = st.secrets["databricks"]["server_hostname"]
    http_path = st.secrets["databricks"]["http_path"]
    access_token = st.secrets["databricks"]["access_token"]

    query = f"""
        SELECT
            numero_cuenta,
            score_riesgo,
            probabilidad_riesgo,
            nivel_riesgo,
            version_modelo
        FROM {tabla}
    """

    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    ) as connection:
        return pd.read_sql(query, connection)


try:
    df = cargar_datos()

    if nivel_riesgo != "Todos":
        df = df[df["nivel_riesgo"] == nivel_riesgo]

    st.subheader("Resumen ejecutivo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Clientes evaluados", f"{len(df):,}")
    col2.metric("Riesgo alto", f"{len(df[df['nivel_riesgo'] == 'Alto']):,}")
    col3.metric("Riesgo medio", f"{len(df[df['nivel_riesgo'] == 'Medio']):,}")
    col4.metric("Riesgo bajo", f"{len(df[df['nivel_riesgo'] == 'Bajo']):,}")

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "Predicciones",
        "Dashboard de riesgo",
        "Descarga"
    ])

    with tab1:
        st.subheader("Predicciones desde Databricks")

        st.dataframe(
            df.sort_values("score_riesgo", ascending=False),
            use_container_width=True
        )

    with tab2:
        st.subheader("Distribución por nivel de riesgo")

        if not df.empty:
            dist = (
                df.groupby("nivel_riesgo")
                .size()
                .reset_index(name="clientes")
            )

            fig = px.pie(
                dist,
                names="nivel_riesgo",
                values="clientes",
                hole=0.45
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Score promedio por nivel de riesgo")

            promedio = (
                df.groupby("nivel_riesgo")["score_riesgo"]
                .mean()
                .reset_index()
            )

            fig_bar = px.bar(
                promedio,
                x="nivel_riesgo",
                y="score_riesgo"
            )

            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No hay datos para los filtros seleccionados.")

    with tab3:
        st.subheader("Descargar resultados")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="score_riesgo_predicciones.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error("No fue posible conectarse a Databricks o consultar la tabla.")
    st.info(
        "Valida que el SQL Warehouse esté activo, que los secrets estén correctos "
        "y que tu usuario tenga permisos sobre score_riesgos.scoring.score_riesgo_predicciones."
    )
    st.exception(e)
