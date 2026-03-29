import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# INITIALISATION (SANS TOUCHER AU CODE INITIAL)
if 'access_code' not in st.session_state: 
    st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state: 
    st.session_state.admin_name = "PATRICIA"
if 'admin_phone' not in st.session_state:
    st.session_state.admin_phone = "0346249701"
if 'hist_av' not in st.session_state: st.session_state.hist_av = []
if 'hist_co' not in st.session_state: st.session_state.hist_co = []

st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        box-shadow: 0 0 15px #00ffcc; margin-bottom: 25px;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 12px; 
        border: 1px solid #00ffcc; padding: 15px; margin-bottom: 10px;
    }
    .target-val { font-size: 38px; color: #00ffcc; font-weight: 800; text-align: center; }
    .prob-badge { background: #00ffcc; color: #000; padding: 4px 10px; border-radius: 20px; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-around; border-top: 1px solid #333; margin-top: 8px; padding-top: 8px; font-size: 12px; }
    .stat-val { color: #00ffcc; font-weight: bold; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: 20px auto; }
    .mine-cell { background: #1a1a1a; height: 55px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 1px solid #333; }
    .diamond-cell { background: rgba(0, 255, 204, 0.2); border: 1px solid #00ffcc; box-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN SYSTEM ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.markdown('<div class="main-header">TITAN V85.0: ACCESS CONTROL</div>', unsafe_allow_html=True)
    code_input = st.text_input("Ampidiro ny kaody fidirana:", type="password")
    if st.button("Mivoha"):
        if code_input == st.session_state.access_code:
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("Kaody diso.")
    st.stop()

# --- 3. SIDEBAR (MANAGER & HIDDEN ADMIN) ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    st.markdown(f"📞 **WhatsApp:** {st.session_state.admin_phone}")
    
    st.markdown("### ⚙️ USER SETTINGS")
    if st.button("🗑️ RESET MY HISTORY"):
        st.session_state.hist_av = []
        st.session_state.hist_co = []
        st.success("Voadio ny tantara!")
        time.sleep(1)
        st.rerun()

    st.markdown("---")
    # ADMIN PANEL: Mipoitra rehefa ampidirina ny kaody secret (access_code)
    admin_key = st.text_input("Admin Key (Secret):", type="password")
    if admin_key == st.session_state.access_code:
        with st.expander("🔓 CONTROL PANEL"):
            st.warning("Fanovana ho an'ny Admin ihany")
            new_name = st.text_input("Anarana vaovao:", st.session_state.admin_name)
            new_mdp = st.text_input("Kaody Admin vaovao:", st.session_state.access_code, type="password")
            new_phone = st.text_input("WhatsApp vaovao:", st.session_state.admin_phone)
            
            if st.button("💾 SAVE CHANGES"):
                st.session_state.admin_name = new_name
                st.session_state.access_code = new_mdp
                st.session_state.admin_phone = new_phone
                st.success("Voatahiry!")
                time.sleep(1)
                st.rerun()

# --- 4. ALGORITHM ENGINE ---
def get_3_preds(seed, base_ora, game_type):
    results = []
    h = hashlib.sha256(f"{seed}-{game_type}-V85".encode()).hexdigest()
    try:
        fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
        dt = datetime.strptime(base_ora, fmt)
    except: dt = datetime.now()
    
    for i in range(3):
        random.seed(int(h[i*8:(i+1)*8], 16))
        moyen = round(random.uniform(1.8, 4.5), 2)
        p = {
            "lera": (dt + timedelta(minutes=(i+1)*4)).strftime(fmt),
            "moyen": moyen, 
            "min": round(moyen*0.8, 2), 
            "max": round(moyen*1.5, 2),
            "prob": random.randint(95, 99)
        }
        results.append(p)
        if game_type == "aviator": st.session_state.hist_av.append(f"{p['lera']} | {p['moyen']}x")
        else: st.session_state.hist_co.append(f"{p['lera']} | {p['moyen']}x")
    return results

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# AVIATOR
with tab1:
    st.markdown("### ⚡ AVIATOR SCANNER")
    st.file_uploader("📸 UPLOAD HISTORIQUE DE LA MANCHE", key="av_up")
    c1, c2 = st.columns(2)
    h_av = c1.text_input("🔑 HEX SEED:", key="h_av")
    o_av = c2.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    
    if st.button("🔥 EXECUTE AVIATOR"):
        for p in get_3_preds(h_av, o_av, "aviator"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stat-row">
                    <span>MIN: <span class="stat-val">{p['min']}x</span></span>
                    <span>MOYEN: <span class="stat-val">{p['moyen']}x</span></span>
                    <span>MAX: <span class="stat-val">{p['max']}x</span></span>
                </div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("#### 📜 LAST PREDICTIONS")
    for item in reversed(st.session_state.hist_av[-5:]):
        st.info(item)

# COSMOS X
with tab2:
    st.markdown("### 🚀 COSMOS X SCANNER")
    st.file_uploader("📸 UPLOAD SCREENSHOT", key="co_up")
    c1, c2 = st.columns(2)
    h_co = c1.text_input("🔑 HEX SEED:", key="h_co")
    o_co = c2.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    
    if st.button("🚀 START COSMOS"):
        for p in get_3_preds(h_co, o_co, "cosmos"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stat-row">
                    <span>MIN: <span class="stat-val">{p['min']}x</span></span>
                    <span>MOYEN: <span class="stat-val">{p['moyen']}x</span></span>
                    <span>MAX: <span class="stat-val">{p['max']}x</span></span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("#### 📜 LAST PREDICTIONS")
    for item in reversed(st.session_state.hist_co[-5:]):
        st.info(item)

# MINES VIP
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    s_serv = st.text_input("📡 Seed du serveur (Hex):")
    s_cli = st.text_input("💻 Seed du client (Hex):")
    if st.button("💎 DECODE SAFE PATH"):
        if s_serv and s_cli:
            combined = hashlib.sha256(f"{s_serv}{s_cli}".encode()).hexdigest()
            random.seed(int(combined[:10], 16))
            diamond_pos = random.sample(range(25), 5)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"diamond-cell" if i in diamond_pos else ""}">{"💎" if i in diamond_pos else "⬛"}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)

st.markdown(f"<center style='font-size:12px; color:#444; margin-top:30px;'>TITAN OMNI-STRIKE BY {st.session_state.admin_name} © 2026<br>MANAGER APP MODE ACTIVE</center>", unsafe_allow_html=True)
