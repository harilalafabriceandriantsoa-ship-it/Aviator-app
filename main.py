import streamlit as st
import random
from datetime import datetime

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: white; }
    .prediction-card {
        background: rgba(22, 27, 34, 0.9); border: 2px solid #00ffcc;
        border-radius: 15px; padding: 25px; text-align: center; margin-top: 20px;
    }
    .accuracy-text { color: #ffd700; font-size: 18px; font-weight: bold; }
    .history-item { font-size: 15px; border-bottom: 1px solid #333; padding: 8px; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History
if 'avi_history' not in st.session_state: st.session_state.avi_history = []

st.title("🚀 TITAN PREDICTION")

# --- INPUTS ---
lera_avi = st.text_input("🕒 Lera fidirana (HH:MM):", value=datetime.now().strftime("%H:%M"))
hex_avi = st.text_input("🔑 HEX SEED:")

if st.button("⚡ ANALYSE"):
    if hex_avi:
        # Fikajiana kisendrasendra
        res = f"{round(random.uniform(2.0, 10.0), 2)}x"
        acc = f"{random.randint(95, 99)}%"
        
        # Fametrahana ao amin'ny History
        st.session_state.avi_history.insert(0, f"{lera_avi} ⮕ {res} ({acc} Acc)")
        
        # Fampisehoana ny vokatra misy Lera sy Accuracy
        st.markdown(f"""
            <div class='prediction-card'>
                <p style='color: #888;'>HEURE: {lera_avi}</p>
                <h1 style='font-size: 45px;'>{res}</h1>
                <p class='accuracy-text'>ESTIMATION: {acc} ACCURACY</p>
            </div>
        """, unsafe_allow_html=True)

# --- HISTORIQUE DE PRÉDICTION ---
st.write("---")
st.subheader("📜 Historique de Prédiction")
for item in st.session_state.avi_history[:5]:
    st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)
