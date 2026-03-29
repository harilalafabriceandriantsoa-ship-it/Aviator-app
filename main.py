import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & DESIGN (PATRICIA STYLE) ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3); margin-bottom: 25px;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 15px; 
        border: 1px solid #00ffcc; padding: 20px; margin-bottom: 15px;
    }
    .target-val { font-size: 45px; color: #00ffcc; font-weight: 800; text-align: center; text-shadow: 0 0 10px #00ffcc; }
    .lera-red { color: #ff4444; font-weight: bold; font-size: 20px; }
    .prob-badge { background: #00ffcc; color: #000; padding: 2px 10px; border-radius: 10px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff) !important;
        color: #010a12 !important; font-weight: bold !important; width: 100%; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE (TITAN LOGIC) ---
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
        
        v_min = round(random.uniform(1.10, 1.40), 2)
        v_moyen = round(random.uniform(1.50, 4.50), 2)
        v_max = round(random.uniform(5.00, 25.00), 2)
        prob = random.randint(94, 99)
        
        add_min = random.randint(3, 10) * (i + 1)
        if game_type == "cosmos":
            add_sec = random.randint(0, 59)
            future_time = (start_dt + timedelta(minutes=add_min, seconds=add_sec)).strftime("%H:%M:%S")
        else:
            future_time = (start_dt + timedelta(minutes=add_min)).strftime("%H:%M")
            
        results.append({"lera": future_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": prob})
    return results

# --- 3. MAIN UI ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# --- AVIATOR ---
with tab1:
    st.markdown("### ⚡ AVIATOR SCANNER")
    st.file_uploader("📸 UPLOAD SCREENSHOT (HISTORIQUE)", type=['png', 'jpg', 'jpeg'], key="av_up")
    c1, c2 = st.columns(2)
    h_av = c1.text_input("🔑 HEX:", key="h_av")
    o_av = c2.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    
    if st.button("🔥 EXECUTE AVIATOR ANALYSIS"):
        if h_av:
            preds = get_titan_prediction(h_av, o_av, "aviator")
            for p in preds:
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="lera-red">⏰ Lera: {p['lera']}</span>
                        <span class="prob-badge">{p['prob']}%</span>
                    </div>
                    <div class="target-val">{p['moyen']}x</div>
                    <div style="display:flex; justify-content:space-around; margin-top:10px; color:#aaa;">
                        <span>MIN: <b>{p['min']}x</b></span>
                        <span style="color:#00ffcc;">TARGET</span>
                        <span>MAX: <b>{p['max']}x</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- COSMOS X ---
with tab2:
    st.markdown("### 🚀 COSMOS X ULTRA-SYNC")
    st.file_uploader("📸 UPLOAD SCREENSHOT (HISTORIQUE)", type=['png', 'jpg', 'jpeg'], key="co_up")
    c1, c2 = st.columns(2)
    h_co = c1.text_input("🔑 HEX:", key="h_co")
    o_co = c2.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    
    if st.button("🚀 EXECUTE COSMOS ANALYSIS"):
        if h_co:
            preds = get_titan_prediction(h_co, o_co, "cosmos")
            for p in preds:
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="lera-red">⏰ Lera: {p['lera']}</span>
                        <span class="prob-badge">{p['prob']}%</span>
                    </div>
                    <div class="target-val">{p['moyen']}x</div>
                    <div style="display:flex; justify-content:space-around; margin-top:10px; color:#aaa;">
                        <span>MIN: <b>{p['min']}x</b></span>
                        <span style="color:#00ffcc;">TARGET</span>
                        <span>MAX: <b>{p['max']}x</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- MINES VIP ---
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5,6,7], value=3)
    m_h = st.text_input("📡 Seed du serveur:", key="m_h")
    m_c = st.text_input("💻 Seed du client:", key="m_c")
    
    if st.button("💎 DECODE SAFE PATH"):
        if m_h and m_c:
            random.seed(int(hashlib.md5(f"{m_h}{m_c}{nb_mines}".encode()).hexdigest()[:10], 16))
            safe = random.sample(range(25), 5)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto;">'
            for i in range(25):
                char, bg = ("💎", "#00ffcc") if i in safe else ("⬛", "#1a1a1a")
                grid += f'<div style="background:{bg}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- FOOTER (MANAGE APP INFO) ---
st.markdown("<br><hr><center style='font-size:12px; color:#444;'>TITAN OMNI-STRIKE BY PATRICIA © 2026<br>MANAGER MODE ACTIVE</center>", unsafe_allow_html=True)
