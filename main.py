import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at center, #0a192f 0%, #010a12 100%); color: #eee; }
    .main-header { 
        font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 20px; border-radius: 15px; 
        background: rgba(0, 255, 204, 0.05); margin-bottom: 25px;
    }
    .card { 
        background: rgba(255, 255, 255, 0.02); border-radius: 15px; 
        border: 1px solid rgba(0, 255, 204, 0.2); padding: 20px; margin-bottom: 15px;
    }
    .target-val { font-size: 45px; color: #ffcc00; font-weight: 800; text-shadow: 0 0 10px #ffcc00; }
    .stButton>button {
        background: linear-gradient(45deg, #ff00cc, #3333ff) !important;
        color: white !important; font-weight: bold !important;
        border: none !important; border-radius: 10px !important;
        height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC (Tsy misy niova) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.2)
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    
    try:
        if game_type == "cosmos":
            start_dt = datetime.strptime(base_ora, "%H:%M:%S")
        else:
            start_dt = datetime.strptime(base_ora, "%H:%M")
    except:
        start_dt = datetime.now()

    h = hashlib.sha256(f"{server_hex}-{SECRET_SALT}-{game_type}".encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        
        v_moyen = round(random.uniform(1.80, 15.50), 2)
        prob = random.randint(92, 99)
        add_min = random.randint(4, 12) * (i + 1)
        
        if game_type == "cosmos":
            add_sec = random.randint(2, 58)
            future_time = (start_dt + timedelta(minutes=add_min, seconds=add_sec)).strftime("%H:%M:%S")
        else:
            future_time = (start_dt + timedelta(minutes=add_min)).strftime("%H:%M")
            
        res = {"lera": future_time, "moyen": v_moyen, "prob": prob}
        results.append(res)
            
    return results

# --- 3. MAIN UI ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# --- AVIATOR & COSMOS (Namboarina ny Label) ---
with t1:
    st.markdown("### ⚡ AVIATOR SCANNER")
    c1, c2 = st.columns(2)
    h_av = c1.text_input("🔑 Seed du serveur (Hex):", key="h_av") # Namboarina ny anarany
    o_av = c2.text_input("🕒 Ora izao (HH:MM):", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE AVIATOR", use_container_width=True):
        if h_av:
            preds = get_titan_prediction(h_av, o_av, "aviator")
            for p in preds:
                st.markdown(f'<div class="card"><div style="display:flex; justify-content: space-between;"><span style="color:#ffcc00; font-weight:bold;">⏰ Lera: {p["lera"]}</span><span>{p["prob"]}%</span></div><div style="text-align:center;"><div class="target-val">{p["moyen"]}x</div></div></div>', unsafe_allow_html=True)

with t2:
    st.markdown("### 🚀 COSMOS X ULTRA-SYNC")
    c1, c2 = st.columns(2)
    h_co = c1.text_input("🔑 Seed du serveur (Hex):", key="h_co") # Namboarina ny anarany
    o_co = c2.text_input("🕒 Ora izao (HH:MM:SS):", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🔥 EXECUTE COSMOS", use_container_width=True):
        if h_co:
            preds = get_titan_prediction(h_co, o_co, "cosmos")
            for p in preds:
                st.markdown(f'<div class="card"><div style="display:flex; justify-content: space-between;"><span style="color:#00ffcc; font-weight:bold;">⏰ Lera: {p["lera"]}</span><span>{p["prob"]}%</span></div><div style="text-align:center;"><div class="target-val">{p["moyen"]}x</div></div></div>', unsafe_allow_html=True)

# --- MINES VIP (Namboarina ny Label hifanaraka amin'ny sary) ---
with t3:
    st.markdown("### 💣 MINES VIP")
    m_h = st.text_input("📡 Seed du serveur:", key="m_h") # Namboarina araka ny sary
    m_c = st.text_input("💻 Seed du client:", key="m_c")   # Namboarina araka ny sary
    if st.button("💎 DECODE", use_container_width=True):
        if m_h and m_c:
            random.seed(int(hashlib.md5(f"{m_h}{m_c}".encode()).hexdigest()[:10], 16))
            safe = random.sample(range(25), 5)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto;">'
            for i in range(25):
                char, bg = ("💎", "#00ffcc") if i in safe else ("⬛", "#1a1a1a")
                grid += f'<div style="background:{bg}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

st.markdown('<br><div style="text-align:center; color:#444; font-size:12px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
