import streamlit as st
import pandas as pd
import numpy as np
import math
import time

# Dashboard Professional Style (Yellow & Black)
st.set_page_config(page_title="Aviator Studio Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffcc00; }
    .stMetric { background-color: #111; border: 1px solid #ffcc00; border-radius: 15px; padding: 15px; }
    div[data-testid="stMetricValue"] { color: #ffcc00; font-size: 45px; }
    .stButton>button { background-color: #ffcc00; color: black; font-weight: bold; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_index=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚀 AVIATOR STUDIO PRO")
st.caption("Master Prediction Engine v11.0 | Ambositra 2026")

with st.sidebar:
    st.header("📥 DATA INPUT")
    hex_val = st.text_input("HEX Seed Farany:")
    cote_val = st.number_input("Cote Nipoitra:", min_value=1.0, value=1.5)
    if st.button("RUN ANALYSIS"):
        if hex_val:
            decimal = int(hex_val[:12], 16)
            root = math.sqrt(decimal)
            st.session_state.history.append({"root": root, "cote": cote_val, "time": time.strftime("%H:%M:%S")})

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    std_dev = df['root'].std() if len(df) > 1 else 0
    # Algorithme de calcul de probabilité
    prob = min(98.8, (df['root'].iloc[-1] % 100) + (20 if df['cote'].iloc[-1] < 1.4 else 0))

    c1, c2, c3 = st.columns(3)
    c1.metric("PROBABILITY x3.00", f"{prob:.1f}%")
    c2.metric("STABILITY (STD)", f"{std_dev:.2f}")
    c3.metric("ROUNDS", len(df))

    st.write("### 📈 Trend Analysis")
    st.line_chart(df['root'])

    if prob >= 95:
        st.warning("🔥 SIGNAL READY")
        if st.button("START 210s COUNTDOWN"):
            p = st.empty()
            for s in range(210, 0, -1):
                p.markdown(f"<h1 style='text-align:center;'>{s}s</h1>", unsafe_allow_html=True)
                time.sleep(1)
            st.balloons()
            st.error("🚀 FIRE! TARGET x3.05")
else:
    st.info("Miandry ny HEX voalohany avy any amin'ny Sidebar...")
