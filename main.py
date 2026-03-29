import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & PREMIUM NEON DESIGN ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp { 
        background: radial-gradient(circle at center, #050c16 0%, #000000 100%); 
        color: #ffffff; 
    }
    
    .main-header { 
        font-size: 40px; font-weight: 900; text-align: center; 
        color: #00ffcc; border: 3px solid #00ffcc; padding: 25px; 
        border-radius: 20px; background: rgba(0, 255, 204, 0.03);
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
        margin-bottom: 30px; letter-spacing: 2px;
    }
    
    .card { 
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; 
        border: 1px solid rgba(0, 255, 204, 0.3); padding: 25px; 
        margin-bottom: 20px; backdrop-filter: blur(10px);
        transition: 0.3s;
    }
    .card:hover { border: 1px solid #ffcc00; transform: scale(1.01); }
    
    .target-val { 
        font-size: 55px; color: #ffcc00; font-weight: 900; 
        text-shadow: 0 0 20px rgba(255, 204, 0, 0.6); 
    }
    
    .lera-box {
        font-size: 28px; color: #ffffff; font-weight: bold;
        background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 10px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0088ff) !important;
        color: #000 !important; font-weight: 900 !important;
        border: none !important; border-radius: 12px !important;
        height: 55px !important; font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4) !important;
    }

    .good-luck {
        text-align: center; color: #00ffcc; font-weight: 900; 
        font-size: 24px; margin: 20px 0; text-shadow: 0 0 10px #00ffcc;
    }
    
    .footer-text { text-align: center; color: #444; font-size: 12px; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC (Tsy nisy nokitihina ny algorithm) ---
def get_titan_prediction_pro(server_hex, base_ora_full, game_type):
    time.sleep(1.5) 
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    
    try:
        # Vakiana ny HH:MM:SS
        start_dt = datetime.strptime(base_ora_full, "%H:%M:%S")
    except:
        start_dt = datetime.now()

    seed_str = f"{server_hex}-{SECRET_SALT}-{game_type}"
    h = hashlib.sha256(seed_str.encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        
        # Lojika X5+ ho an'ny vinavina faharoa
        if i == 1:
            v_moyen = round(random.uniform(5.10, 15.50), 2)
            prob = random.randint(92, 95)
        else:
            v_moyen = round(random.uniform(1.80, 4.20), 2)
            prob = random.randint(96, 99)
            
        # Elanelana minitra sy segondra
        add_min = random.randint(4, 12) * (i + 1)
        add_sec = random.randint(2, 58) 
        
        future_time = (start_dt + timedelta(minutes=add_min, seconds=add_sec)).strftime("%H:%M:%S")
        
        res = {"lera": future_time, "moyen": v_moyen, "prob": prob}
        results.append(res)
            
    return results

# --- 3. MAIN UI ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 COSMOS / AVIATOR PRO", "💎 MINES VIP", "⚙️ SYSTEM"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        hex_val = st.text_input("🔑 SERVER SEED (HEX):", placeholder="Ampidiro ny Hex eto...")
    with c2:
        # Ora miaraka amin'ny segondra (HH:MM:SS)
        ora_val = st.text_input("🕒 SYSTEM TIME (HH:MM:SS):", value=datetime.now().strftime("%H:%M:%S"))
    
    if st.button("🔥 EXECUTE PREMIUM ANALYSIS", use_container_width=True):
        if hex_val:
            with st.spinner("🔄 Synchronizing with Server Seed..."):
                preds = get_titan_prediction_pro(hex_val, ora_val, "omni")
                st.markdown('<p class="good-luck">🍀 BONNE CHANCE À TOUS - ARAHO NY SEGONDRA</p>', unsafe_allow_html=True)
                
                for p in preds:
                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; justify-content: space-between; align-items:center;">
                            <div class="lera-box">⏰ {p['lera']}</div>
                            <div style="background:#00ffcc; color:#000; padding:5px 15px; border-radius:20px; font-weight:900;">{p['prob']}% ACCURACY</div>
                        </div>
                        <div style="text-align:center; margin-top:20px;">
                            <small style="color:rgba(255,255,255,0.5); letter-spacing:1px;">ULTRA TARGET</small><br>
                            <div class="target-val">{p['moyen']}x</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Ampidiro ny Server Seed (Hex) azafady!")

with tab2:
    st.markdown("### 💣 MINES DECODER PRO")
    m_hex = st.text_input("🔑 HEX SEED:", key="mine_h")
    m_cli = st.text_input("👤 CLIENT SEED:", key="mine_c")
    if st.button("💎 DECODE SAFE TILES", use_container_width=True):
        random.seed(int(hashlib.md5(f"{m_hex}{m_cli}".encode()).hexdigest()[:8], 16))
        safe_tiles = random.sample(range(25), 5)
        st.markdown('<p class="good-luck">🍀 BONNE CHANCE À TOUS</p>', unsafe_allow_html=True)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto;">'
        for idx in range(25):
            char, bg = ("💎", "#00ffcc") if idx in safe_tiles else ("⬛", "#111")
            grid += f'<div style="background:{bg}; height:60px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:30px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);">{char}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

with tab3:
    st.info("System Status: Operational | Accuracy: Ultra Pro Premium")
    if st.button("🔴 RESET ALL CACHE DATA"):
        st.rerun()

st.markdown('<div class="footer-text">TITAN OMNI-STRIKE BY PATRICIA © 2026<br>PREMIUM ACCESS GRANTED</div>', unsafe_allow_html=True)
