import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & ACCESS CONTROL ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

ACCESS_CODE = "ADMIN_TITAN" 

# CSS ho an'ny endrika Neon sy ny Sidebar
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        box-shadow: 0 0 15px #00ffcc; margin-bottom: 25px;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 15px; 
        border: 1px solid #00ffcc; padding: 20px; margin-bottom: 15px;
    }
    .target-val { font-size: 40px; color: #00ffcc; font-weight: 800; text-align: center; }
    .sidebar-text { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="main-header">TITAN V85.0: ACCESS CONTROL</div>', unsafe_allow_html=True)
    code_input = st.text_input("Ampidiro ny kaody mamoha ny app:", type="password")
    if st.button("Mivoha"):
        if code_input == ACCESS_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Kaody diso.")
    st.stop()

# --- 3. SIDEBAR SETTINGS (TEL & BY PATRICIA) ---
with st.sidebar:
    st.markdown("### ⚙️ SETTINGS & PROFILE")
    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Sarina Profile
    st.markdown(f"👤 **Manager:** <span class='sidebar-text'>PATRICIA</span>", unsafe_allow_html=True)
    # Eto no misy ilay Numero finday
    st.markdown(f"📞 **Contact:** <span class='sidebar-text'>+261 34 00 000 00</span>", unsafe_allow_html=True) 
    st.markdown("---")
    st.info("Status: Administrator Mode Active")
    st.write("Ianao irery no afaka manova ny kaody sy ny fikirakirana rehetra eto.")

# --- 4. CORE ENGINE (AVIATOR & COSMOS) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1)
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    try:
        start_dt = datetime.strptime(base_ora, "%H:%M:%S" if game_type=="cosmos" else "%H:%M")
    except:
        start_dt = datetime.now()

    h = hashlib.sha256(f"{server_hex}-{SECRET_SALT}-{game_type}".encode()).hexdigest()
    for i in range(3):
        random.seed(int(h[i*10 : (i+1)*10], 16))
        v_moyen = round(random.uniform(1.5, 4.0), 2)
        add_min = random.randint(3, 10) * (i + 1)
        future_time = (start_dt + timedelta(minutes=add_min)).strftime("%H:%M:%S" if game_type=="cosmos" else "%H:%M")
        results.append({"lera": future_time, "moyen": v_moyen})
    return results

# --- 5. INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with tab1:
    st.markdown("### ⚡ AVIATOR SCANNER")
    st.file_uploader("📸 UPLOAD HISTORIQUE", type=['png', 'jpg', 'jpeg'], key="av_up")
    c1, c2 = st.columns(2)
    h_av = c1.text_input("🔑 HEX:", key="h_av")
    o_av = c2.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE AVIATOR"):
        for p in get_titan_prediction(h_av, o_av, "aviator"):
            st.markdown(f'<div class="prediction-card">⏰ Lera: {p["lera"]}<div class="target-val">{p["moyen"]}x</div></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🚀 COSMOS X SCANNER")
    st.file_uploader("📸 UPLOAD SCREENSHOT", type=['png', 'jpg', 'jpeg'], key="co_up")
    c1, c2 = st.columns(2)
    h_co = c1.text_input("🔑 HEX (Cosmos):", key="h_co")
    o_co = c2.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🚀 EXECUTE COSMOS"):
        for p in get_titan_prediction(h_co, o_co, "cosmos"):
            st.markdown(f'<div class="prediction-card">⏰ Lera: {p["lera"]}<div class="target-val">{p["moyen"]}x</div></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5,6,7], value=3)
    if st.button("💎 DECODE"):
        st.success(f"Analysis for {nb_mines} mines.")

# --- FOOTER ---
st.markdown(f"<br><hr><center style='font-size:12px; color:#444;'>TITAN OMNI-STRIKE BY PATRICIA © 2026<br><b>MANAGER APP MODE ACTIVE</b></center>", unsafe_allow_html=True)
