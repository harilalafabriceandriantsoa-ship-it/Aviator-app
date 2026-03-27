import streamlit as st
import hashlib
import time
from datetime import datetime

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="ANDRIANTSO v60.1", page_icon="💎", layout="wide")

# --- STYLE CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #FFD700; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FFD700; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DATA ---
if 'history' not in st.session_state: st.session_state.history = []
if 'wins' not in st.session_state: st.session_state.wins = 0

st.title("💎 ANDRIANTSO | SUPREME v60.1 (Variable Edition)")

# --- DASHBOARD STATS ---
col1, col2, col3 = st.columns(3)
with col1: st.metric("🏆 TOTAL WINS", st.session_state.wins)
with col2: 
    acc = (st.session_state.wins / len(st.session_state.history) * 100) if st.session_state.history else 0
    st.metric("📈 ACCURACY", f"{round(acc, 1)}%")
with col3: st.metric("🔄 SESSIONS", len(st.session_state.history))

# --- GENERATOR LOGIC ---
st.write("---")
hex_input = st.text_input("🔑 AMPIDIRO NY HEX SEED (SHA-256):", placeholder="Paste Hex here...")

if st.button("🔥 GENERATE VARIABLE SIGNAL"):
    if len(hex_input) < 10:
        st.error("❌ HEX SEED fohy loatra! Mila kaody feno avy amin'ny Provably Fair.")
    else:
        with st.spinner('AI Calculating Probability...'):
            time.sleep(1)
            # Algorithm Variable v60.1
            h = hashlib.sha256(hex_input.encode()).hexdigest()
            val = int(h[:10], 16)
            
            # Kajy Variable
            prob = 75 + (val % 21) # Probability eo anelanelan'ny 75% sy 96%
            safe_var = round(1.50 + (val % 150) / 100, 2) # Safe variable 1.50x hatramin'ny 3.00x
            pink_var = round(10.0 + (val % 9000) / 100, 2) # Pink variable
            
            # Fampisehoana ny Valiny
            st.markdown(f"### 📊 ESTIMATION: **{prob}%**")
            c1, c2 = st.columns(2)
            with c1: st.success(f"✅ SAFE EXIT: **{safe_var}x**")
            with c2: st.warning(f"💗 MAX PINK: **{pink_var}x**")
            
            # Tehirizina ao amin'ny History
            new_data = {
                "Lera": datetime.now().strftime("%H:%M:%S"),
                "Hex": hex_input[:10] + "...",
                "Safe": safe_var,
                "Max": pink_var,
                "Prob": f"{prob}%"
            }
            st.session_state.history.insert(0, new_data)

# --- HISTORIQUE DE PRÉDICTION ---
st.write("---")
st.subheader("📜 HISTORIQUE DE PRÉDICTION")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.button("✅ I WON (Add to Wins)"):
        st.session_state.wins += 1
        st.rerun()
else:
    st.info("Mbola tsy misy prediction vita. Ampidiro ny Hex Seed eo ambony.")

if st.button("🗑️ CLEAR ALL DATA"):
    st.session_state.history = []
    st.session_state.wins = 0
    st.rerun()
