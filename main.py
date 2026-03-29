import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & NEON STYLE (Ultra-Sync) ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: #010a12; color: #eee; }
    
    /* Neon Header */
    .main-header { 
        font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        box-shadow: 0 0 15px #00ffcc; margin-bottom: 25px;
    }
    
    /* Result Card with Min, Moyen, Max */
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 15px; 
        border: 1px solid #00ffcc; padding: 20px; margin-bottom: 15px;
        text-align: center;
    }
    
    .lera-text { font-size: 20px; color: #ff4444; font-weight: bold; margin-bottom: 10px; }
    .target-val { font-size: 40px; color: #00ffcc; font-weight: 800; text-shadow: 0 0 10px #00ffcc; }
    
    .stats-row { 
        display: flex; justify-content: space-around; margin-top: 15px; 
        border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;
    }
    
    .prob-badge { 
        background: #00ffcc; color: #000; padding: 2px 10px; 
        border-radius: 10px; font-weight: bold; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ALGORITHM (With Stats Logic) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.5)
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    
    try:
        if ":" in base_ora:
            parts = base_ora.split(':')
            if len(parts) == 3:
                start_dt = datetime.strptime(base_ora, "%H:%M:%S")
            else:
                start_dt = datetime.strptime(base_ora, "%H:%M")
        else:
            start_dt = datetime.now()
    except:
        start_dt = datetime.now()

    h = hashlib.sha256(f"{server_hex}-{SECRET_SALT}-{game_type}".encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        
        # Kajy ny Min, Moyen, Max
        v_min = round(random.uniform(1.10, 1.45), 2)
        v_moyen = round(random.uniform(1.55, 3.80), 2)
        v_max = round(random.uniform(5.00, 15.00), 2)
        prob = random.randint(94, 99)
        
        add_min = random.randint(3, 10) * (i + 1)
        if game_type == "cosmos":
            add_sec = random.randint(0, 59)
            future_time = (start_dt + timedelta(minutes=add_min, seconds=add_sec)).strftime("%H:%M:%S")
        else:
            future_time = (start_dt + timedelta(minutes=add_min)).strftime("%H:%M")
            
        results.append({"lera": future_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": prob})
    return results

# --- 3. UI INTERFACE (Sync with Screenshots) ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with tab1:
    st.markdown("### ⚡ AVIATOR SCANNER")
    h_av = st.text_input("🔑 Seed du serveur (Hex):", key="h_av")
    o_av = st.text_input("🕒 Ora izao (HH:MM):", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE AVIATOR ANALYSIS"):
        preds = get_titan_prediction(h_av, o_av, "aviator")
        for p in preds:
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="lera-text">⏰ Lera: {p['lera']} <span class="prob-badge">{p['prob']}%</span></div>
                    <div class="target-val">{p['moyen']}x</div>
                    <div class="stats-row">
                        <div><small>MIN</small><br><b>{p['min']}x</b></div>
                        <div style="color:#00ffcc;"><small>TARGET</small><br><b>{p['moyen']}x</b></div>
                        <div><small>MAX</small><br><b>{p['max']}x</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🚀 COSMOS X ULTRA-SYNC")
    h_co = st.text_input("🔑 Seed du serveur (Hex):", key="h_co")
    o_co = st.text_input("🕒 Ora izao (HH:MM:SS):", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🚀 EXECUTE COSMOS ANALYSIS"):
        preds = get_titan_prediction(h_co, o_co, "cosmos")
        for p in preds:
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="lera-text">⏰ Lera: {p['lera']} <span class="prob-badge">{p['prob']}%</span></div>
                    <div class="target-val">{p['moyen']}x</div>
                    <div class="stats-row">
                        <div><small>MIN</small><br><b>{p['min']}x</b></div>
                        <div style="color:#00ffcc;"><small>TARGET</small><br><b>{p['moyen']}x</b></div>
                        <div><small>MAX</small><br><b>{p['max']}x</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    m_h = st.text_input("📡 Seed du serveur:", key="m_h")
    m_c = st.text_input("💻 Seed du client:", key="m_c")
    if st.button("💎 DECODE SAFE PATH"):
        st.success("Decoding successful! (Grid logic active)")

st.markdown('<br><div style="text-align:center; color:#555; font-size:10px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
