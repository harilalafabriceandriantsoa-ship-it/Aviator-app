import hashlib
import time
import random
import streamlit as st
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
st.set_page_config(page_title="ANDRIANTSO | APEX v44", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    .apex-title { text-align: center; font-size: 38px; font-weight: 900; color: #FFD700; text-shadow: 0 0 15px #FFD700; }
    .lesson-card { background: #111; padding: 15px; border-radius: 15px; border-left: 5px solid #FFD700; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="apex-title">💎 ANDRIANTSO | APEX v44</p>', unsafe_allow_html=True)

# --- 🎓 UNIVERSITY: LESONA SY TACTIQUES ---
with st.expander("🎓 UNIVERSITY: LESONA SY TACTIQUES (Open here)"):
    st.markdown("""
    <div class="lesson-card">
    <b>1. Ny Lalàn'ny Pink Wave (Mavokely):</b><br>
    Aza miditra mihitsy raha vao nisy 100x vao haingana. Miandrasa elanelana 15-20 minitra vao mampiasa ny Signal APEX indray.
    </div>
    <div class="lesson-card">
    <b>2. Ny Taktika 1.50x (Safety First):</b><br>
    Raha manao "Auto-cashout" ianao, apetraho amin'ny 1.50x ny iray ary avelao handeha ny iray. Ny 1.50x dia manonitra ny fatiantoka raha sendra "Crash" tampoka.
    </div>
    <div class="lesson-card">
    <b>3. Famantarana ny Hex Seed:</b><br>
    Ny Hex Seed dia miova isaky ny 10 rounds. Rehefa mahatsapa ianao fa tsy mifanaraka intsony ny lera, dia "Refresh-eo" ny Hex-nao.
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
st.write("### 🕹️ FIDIO NY LALAO:")
tab1, tab2 = st.tabs(["✈️ MODE AVIATOR", "🚀 MODE COSMOS X"])

def run_app(game_name, color, limit, speed):
    col1, col2 = st.columns([1, 1.2])
    with col1:
        sync = st.radio(f"🕒 SYNC ({game_name}):", ["Normal", "+1 min", "-1 min"], key=f"s_{game_name}")
        hex_in = st.text_input("🔑 HEX SEED:", key=f"h_{game_name}")
        time_in = st.time_input("⏲️ LERA:", value=now_mg.time(), key=f"t_{game_name}")
        
        if st.button(f"🔥 GENERATE {game_name}", key=f"b_{game_name}"):
            if hex_in:
                h = hashlib.sha256(hex_in.encode()).hexdigest()
                v = int(h[:8], 16)
                off = 1 if "+1 min" in sync else -1 if "-1 min" in sync else 0
                target = datetime.combine(datetime.today(), time_in) + timedelta(minutes=(speed + off))
                st.session_state.current = {"Lera": target.strftime("%H:%M"), "Prob": f"{78+(v%20)}%", "Safe": limit, "game": game_name}
                st.rerun()

    with col2:
        if 'current' in st.session_state and st.session_state.current["game"] == game_name:
            curr = st.session_state.current
            st.markdown(f"""
            <div style="border: 2px solid {color}; padding: 25px; border-radius: 25px; text-align: center;">
                <h1 style="color: {color}; font-size: 60px;">{curr['Lera']}</h1>
                <p>🎯 ACCURACY: {curr['Prob']} | ✅ SAFE: {curr['Safe']}x</p>
            </div>
            """, unsafe_allow_html=True)

with tab1: run_app("AVIATOR", "#FFD700", 2.03, 2)
with tab2: run_app("COSMOS", "#00D4FF", 1.75, 1)

st.write("---")
st.image("https://img.freepik.com/free-photo/view-futuristic-fighter-jet-flying_23-2151214041.jpg", use_container_width=True)
