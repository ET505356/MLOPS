import streamlit as st

st.set_page_config(page_title="Mini Tablero", layout="wide")

st.title("Mini Tablero")
st.caption("Dashboard HTML en Streamlit")

metrics = [
    ("Ventas hoy", "$1,240"),
    ("Usuarios activos", "86"),
    ("Conversión", "4.3%"),
]
cards_html = "\n".join(
    f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div></div>'
    for label, value in metrics
)

st.markdown(
    f"""
    <style>
      .cards {display:grid;grid-template-columns:repeat(auto-fit, minmax(160px, 1fr));gap:14px;margin-top:12px;}
      .card {background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);}
      .label {font-size:13px;color:#6b7280;}
      .value {font-size:28px;font-weight:700;color:#111827;margin-top:4px;}
    </style>
    <div class="cards">{cards_html}</div>
    """,
    unsafe_allow_html=True,
)
