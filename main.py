import streamlit as st
import random
import time
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.4 ULTRA", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login System
if not st.session_state.authenticated:
    st.title("🛸 TITAN ULTRA V64.4")
    pwd = st.text_input("ENTER SYSTEM KEY:", type="password")
    if st.button("LOGIN"):
        if pwd == "TITAN2026":
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("WRONG KEY")
    st.stop()

st.markdown("<h1 style='text-align:center; color:#00ffcc;'>TITAN V64.4 ULTRA FIX</h1>", unsafe_allow_html=True)

# --- MINES ENGINE ---
st.subheader("💣 NEURAL MINES (DYNAMIC MODE)")

c_seed = st.text_input("💻 Client Seed:", key="c_s")
s_seed = st.text_input("🖥️ Server Seed:", key="s_s")
nb_mines = st.slider("Mines:", 1, 5, 3)

if st.button("⚡ GENERATE NEW SCAN", use_container_width=True):
    # DYNAMIC HASH: Mampiasa ny 'nanoseconds' mba hampiova ny valiny foana
    # Na mitovy aza ny Seed, ny lera (time) dia tsy hitovy mihitsy
    unique_engine_seed = hash(c_seed + s_seed + str(time.time_ns()))
    random.seed(unique_engine_seed)
    
    # Mifidy toerana 5 vaovao
    stars = random.sample(range(25), k=5)
    st.session_state.history.append(f"Scan at {datetime.now().strftime('%H:%M:%S')}")

    # Grid Display
    grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 8px; justify-content: center;">'
    for i in range(25):
        color = "#ffd700" if i in stars else "#2c3e50"
        grid_html += f'<div style="width:50px; height:50px; background:{color}; border-radius:5px;"></div>'
    st.markdown(grid_html + '</div>', unsafe_allow_html=True)
    st.success("✅ SCAN DYNAMIQUE VITA. MIREHITRA NY KINTANA VAOVAO.")

# --- RESET TOOL ---
st.write("---")
if st.button("🗑️ HAMAFA NY TEKNIQUE REHETRA (RESET)"):
    st.session_state.history = []
    st.rerun()
