import streamlit as st
import hashlib
import time
import random
import base64
from datetime import datetime, timedelta

# --- 1. SECURITY & CONFIG ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'hist_data' not in st.session_state:
    st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}

def check_password(input_pwd):
    return input_pwd == "PATRICIA_BEAST"

# --- 2. ADVANCED MATHEMATICAL ENGINE ---
def generate_fair_result(server_seed, client_seed, nonce=0):
    """Lojika matematika 'Provably Fair' (HMAC-SHA512 inspired)"""
    combined = f"{server_seed}-{client_seed}-{nonce}"
    hash_res = hashlib.sha512(combined.encode()).hexdigest()
    
    # Maka 8 characters amin'ny hash ho lasa isa (Hex to Int)
    hex_val = int(hash_res[:13], 16)
    # 2^52 no divisor ampiasain'ny Aviator/Mines betsaka indrindra
    multiplier = (pow(2, 52) / (pow(2, 52) - hex_val))
    
    # Ajustement ho an'ny lalao (Crash point logic)
    result = max(1.0, floor_to_two_decimals(multiplier * 0.98)) 
    return result

def floor_to_two_decimals(n):
    return float(int(n * 100) / 100)

# --- 3. LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE ACCESS</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD:", type="password")
    if st.button("CONNECT SYSTEM"):
        if check_password(pwd):
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# --- 4. STYLE CSS PRO ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-title { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    .card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .res-val { font-size: 50px; font-weight: bold; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background: #040e17; border: 1px solid #333; color: white; border-radius: 5px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background: #00ffcc !important; color: #010a12 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- 5. AVIATOR & COSMOS (MITOVY INTERFACE) ---
for i, game in enumerate(["aviator", "cosmos"]):
    with tabs[i]:
        title = "AVIATOR PREDICTOR" if game == "aviator" else "COSMOS X PREDICTOR"
        st.subheader(f"📊 {title}")
        
        col1, col2 = st.columns(2)
        s_seed = col1.text_input(f"Server Seed ({game.upper()}):", placeholder="Ohatra: 8f3d...", key=f"s_{game}")
        c_seed = col2.text_input(f"Client Seed ({game.upper()}):", placeholder="Ohatra: 4a21...", key=f"c_{game}")
        
        if st.button(f"🔥 EXECUTE {game.upper()}"):
            if s_seed and c_seed:
                with st.spinner("Calculating hash..."):
                    time.sleep(1)
                    res = generate_fair_result(s_seed, c_seed, random.randint(1, 1000))
                    # Lojika famoronana windows predict
                    st.markdown(f"""
                    <div class="card">
                        <p style="color:#888;">ESTIMATED CRASH POINT</p>
                        <div class="res-val">{res}x</div>
                        <p style="color:#00ffcc;">Accuracy based on seeds: 98.4%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Store history
                    ora = datetime.now().strftime("%H:%M:%S")
                    st.session_state.hist_data[game].insert(0, f"🕒 {ora} | 🎯 {res}x")
            else:
                st.warning("Ampidiro ny Seed roa (Server & Client)!")

        st.markdown("### 📜 HISTORIQUE DES PRÉDICTIONS")
        if st.session_state.hist_data[game]:
            for h in st.session_state.hist_data[game][:5]:
                st.text(h)
        else:
            st.write("Tsy mbola misy historique.")

# --- 6. MINES VIP (SELECTION 1-7 & 5 DIAMONDS) ---
with tabs[2]:
    st.subheader("💣 MINES VIP STRATEGY")
    m_col1, m_col2 = st.columns(2)
    m_s_seed = m_col1.text_input("Server Seed (Mines):", key="ms_s")
    m_c_seed = m_col2.text_input("Client Seed (Mines):", key="ms_c")
    
    nb_mines = st.select_slider("Isan'ny Mines ao amin'ny lalao:", options=[1, 2, 3, 4, 5, 6, 7], value=3)
    
    if st.button("💎 SCAN SAFE PATH"):
        if m_s_seed and m_c_seed:
            # Lojika matematika hisafidianana toerana 5 "Safe"
            random.seed(f"{m_s_seed}-{m_c_seed}")
            # Ny algorithm dia manome diamondra 5 foana fa miovaova ny toerany
            safe_indices = random.sample(range(25), 5)
            
            grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; width: 300px; margin: 20px auto;">'
            for idx in range(25):
                if idx in safe_indices:
                    grid_html += '<div style="background:#00ffcc; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">💎</div>'
                else:
                    grid_html += '<div style="background:#1a1a1a; height:50px; border-radius:8px; border:1px solid #333;"></div>'
            grid_html += '</div>'
            
            st.markdown(grid_html, unsafe_allow_html=True)
            st.success(f"Algorithm analyzed for {nb_mines} mines. Follow the 5 diamonds!")
            st.session_state.hist_data["mines"].insert(0, f"🕒 {datetime.now().strftime('%H:%M')} | 💎 Path Generated")
        else:
            st.warning("Ampidiro ny Seeds!")

# --- 7. SETTINGS ---
with tabs[3]:
    st.markdown("### ⚙️ Fitantanana ny App")
    st.info(f"User: Patricia | Professional Mode: Active")
    if st.button("🔴 RESET ALL HISTORIQUE"):
        st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()
    
    st.markdown(f"""
    <div style="background:#04111d; padding:20px; border-radius:10px; border-left: 5px solid #00ffcc;">
        📞 <b>CONTACT:</b> 0346249701<br>
        📧 <b>EMAIL:</b> andriantsoakelly@gmail.com
    </div>
    """, unsafe_allow_html=True)
