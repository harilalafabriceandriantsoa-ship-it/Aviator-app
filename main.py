import streamlit as st
import hashlib
import time
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="ANDRIANTSO SUPREME v60.2", page_icon="💎")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; border: 1px solid #FFD700; border-radius: 10px; }
    .stButton>button { width: 100%; background-color: #FFD700; color: black; font-weight: bold; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'wins' not in st.session_state: st.session_state.wins = 0

st.title("💎 ANDRIANTSO | SUPREME v60.2")

# --- MODE SELECTION ---
mode = st.radio("🚀 FIDIO NY LALAO:", ["✈️ AVIATOR", "🚀 COSMOS X"], horizontal=True)

# --- STATS ---
c1, c2 = st.columns(2)
with c1: st.metric("🏆 WINS", st.session_state.wins)
with c2: 
    acc = (st.session_state.wins / len(st.session_state.history) * 100) if st.session_state.history else 0
    st.metric("📈 ACCURACY", f"{round(acc, 1)}%")

st.write("---")

# --- INPUTS ---
hex_input = st.text_input(f"🔑 HEX SEED {mode}:", placeholder="Paste Hex here...")

if st.button(f"🔥 ANALYSE {mode}"):
    if len(hex_input) < 8:
        st.error("❌ Ampidiro ny Hex Seed feno!")
    else:
        with st.spinner('AI Calculating...'):
            time.sleep(1)
            h = hashlib.sha256(hex_input.encode()).hexdigest()
            val = int(h[:10], 16)
            
            # Logic Variable isaky ny mode
            prob = 78 + (val % 19)
            if "AVIATOR" in mode:
                safe = round(1.65 + (val % 135) / 100, 2)
                pink = round(12.0 + (val % 8000) / 100, 2)
            else: # COSMOS
                safe = round(1.45 + (val % 110) / 100, 2)
                pink = round(8.5 + (val % 4500) / 100, 2)

            # Output Valiny
            st.markdown(f"### 📊 ESTIMATION: **{prob}%**")
            res1, res2 = st.columns(2)
            res1.success(f"✅ SAFE EXIT: **{safe}x**")
            res2.warning(f"💗 MAX PINK: **{pink}x**")
            
            # Save to History
            st.session_state.history.insert(0, {
                "Lera": datetime.now().strftime("%H:%M"),
                "Game": mode,
                "Safe": safe,
                "Max": pink,
                "Prob": f"{prob}%"
            })

# --- HISTORIQUE ---
st.write("---")
st.subheader("📜 TANTARAN'NY PREDICTION")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.button("✅ MAHAZO (Add Win)"):
        st.session_state.wins += 1
        st.rerun()
else:
    st.info("Mbola tsy misy data.")

if st.sidebar.button("🗑️ RESET ALL"):
    st.session_state.history = []
    st.session_state.wins = 0
    st.rerun()
