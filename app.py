import streamlit as st

st.set_page_config(page_title="Mini Dashboard", layout="wide")

st.title("Mini Dashboard")
st.caption("Dashboard HTML simple en Streamlit")

st.markdown(
    """
    <style>
      .cards {display:grid;grid-template-columns:repeat(3, minmax(160px, 1fr));gap:14px;margin-top:12px;}
      .card {background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);}
      .label {font-size:13px;color:#6b7280;}
      .value {font-size:28px;font-weight:700;color:#111827;margin-top:4px;}
    </style>
    <div class="cards">
      <div class="card"><div class="label">Ventas Hoy</div><div class="value">$1,240</div></div>
      <div class="card"><div class="label">Usuarios Activos</div><div class="value">86</div></div>
      <div class="card"><div class="label">Conversión</div><div class="value">4.3%</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)
