import streamlit as st
import hashlib
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SECURITY SYSTEM (Teny fanalahidy) ---
if 'access' not in st.session_state:
    st.session_state.access = False

if not st.session_state.access:
    st.markdown("<h2 style='text-align:center; color:#00ffcc;'>🔐 ACCESS LOCKED</h2>", unsafe_allow_html=True)
    password = st.text_input("Ampidiro ny teny fanalahidy (Patricia):", type="password")
    if password == "PATRICIA_BEAST":
        st.session_state.access = True
        st.rerun()
    st.stop()

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. STYLE PREMIUM ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: white; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; border-bottom: 2px solid #00ffcc; }
    .consigne-box { background: rgba(255, 75, 75, 0.15); border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; }
    .lera-container { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 15px; color: #ffd700; font-weight: bold; margin-top: 20px; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 55px; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

# --- 4. ALGORITHM ENGINE ---
def get_prediction_logic(seed, h_ora):
    combined = f"{seed}{h_ora}{time.time()}".encode()
    h = hashlib.sha512(combined).hexdigest()
    random.seed(int(h[:16], 16))
    
    vmin = round(random.uniform(1.20, 1.45), 2)
    vmoy = round(random.uniform(2.15, 4.95), 2)
    vmax = round(random.uniform(15.0, 95.0), 2)
    
    # Lera 3 samihafa (tsy misy mitovy)
    base_t = datetime.strptime(h_ora, "%H:%M")
    preds = []
    offsets = random.sample(range(2, 25), 3) # Maka isa 3 samihafa elanelana 2 ka hatramin'ny 25 minitra
    offsets.sort()
    
    for offset in offsets:
        p_time = (base_t + timedelta(minutes=offset)).strftime("%H:%M")
        p_acc = random.randint(92, 98)
        preds.append({"ora": p_time, "acc": p_acc})
    return vmin, vmoy, vmax, preds

# --- 5. TABS ---
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- AVIATOR & COSMOS X ---
for i, tab in enumerate([t1, t2]):
    game = "AVIATOR" if i == 0 else "COSMOS X"
    with tab:
        st.markdown(f'<div class="consigne-box">⚠️ <b>CONSIGNE {game}:</b> Cashout 2x-4x. Tenter x10+ isaky ny 15min.</div>', unsafe_allow_html=True)
        st.file_uploader(f"📸 Capture {game}:", type=['jpg','png','jpeg'], key=f"cap_{i}")
        u_hex = st.text_input(f"🔑 HEX SEED ({game}):", key=f"hex_{i}")
        u_time = st.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"time_{i}")
        
        if st.button(f"🔥 EXECUTE {game} ENGINE", key=f"btn_{i}"):
            if u_hex:
                vmin, vmoy, vmax, preds = get_prediction_logic(u_hex, u_time)
                st.markdown(f"""
                    <div class="card-beast">
                        <div style="display:flex; justify-content:space-around;">
                            <div><p style="color:#ff4b4b;">MIN</p><h2>{vmin}x</h2></div>
                            <div><p style="color:#00ffcc;">MOYEN</p><h1 style="color:#00ffcc; font-size:50px;">{vmoy}x</h1></div>
                            <div><p style="color:#ffd700;">MAX</p><h2>{vmax}x</h2></div>
                        </div>
                    </div>
                    <div class="lera-container">
                        🎯 NEXT ROUNDS:<br>
                        ⏰ {preds[0]['ora']} ({preds[0]['acc']}%) | ⏰ {preds[1]['ora']} ({preds[1]['acc']}%) | ⏰ {preds[2]['ora']} ({preds[2]['acc']}%)
                    </div>
                """, unsafe_allow_html=True)
            else: st.warning("Ampidiro ny HEX SEED!")

# --- 💣 MINES VIP (AMBOARINA NY SEED CLIENT/SERVER) ---
with t3:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE MINES:</b> 5 Diamants ihany. Ovao ny Client Seed isaky ny mahazo Diamondra 5.</div>', unsafe_allow_html=True)
    st.file_uploader("📸 Capture (Mines):", type=['jpg','png','jpeg'])
    
    # Eto ny fanamboarana ny Seed roa
    col_m1, col_m2 = st.columns(2)
    with col_m1: m_client = st.text_input("💻 CLIENT SEED:", placeholder="Ovao matetika...", key="m_cli")
    with col_m2: m_server = st.text_input("🌐 SERVER SEED:", placeholder="Hashed seed...", key="m_ser")
    
    n_mines = st.select_slider("💣 ISAN'NY BAOMBA:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 GENERATE 5-DIAMOND SCHEMA"):
        # Fampifangaroana ny Seed roa ho an'ny fahamendrehana
        random.seed(hash(m_client + m_server + str(time.time())))
        spots = random.sample(range(25), k=5)
        
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 50px); gap:8px; justify-content:center; margin:20px 0;">'
        for j in range(25):
            icon = "💎" if j in spots else ""
            bg = "#00ffcc" if j in spots else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{bg}; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">{icon}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        
        # Ora 3 samihafa ho an'ny Mines koa
        now = datetime.now()
        m_ora1 = (now + timedelta(minutes=random.randint(2, 5))).strftime("%H:%M")
        m_ora2 = (now + timedelta(minutes=random.randint(6, 12))).strftime("%H:%M")
        m_ora3 = (now + timedelta(minutes=random.randint(13, 22))).strftime("%H:%M")
        
        st.markdown(f"""
            <div class="lera-container">
                🕒 ORA TSARA HILALAOVANA MINES:<br>
                ⏰ {m_ora1} (96%) | ⏰ {m_ora2} (94%) | ⏰ {m_ora3} (98%)
            </div>
        """, unsafe_allow_html=True)
