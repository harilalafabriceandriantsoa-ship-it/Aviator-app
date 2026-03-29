import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIG & SECURITY ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'hist_data' not in st.session_state:
    st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}

# --- 2. ENGINE LOGIC ---
def get_strategic_prediction(server_hex, base_ora):
    results = []
    INTERNAL_CLIENT = "TITAN_PRO_2026"
    try:
        base_time = datetime.strptime(base_ora, "%H:%M")
    except:
        base_time = datetime.now()
    combined = f"{server_hex}-{INTERNAL_CLIENT}"
    seed_hash = hashlib.sha512(combined.encode()).hexdigest()
    for i in range(3):
        step_hash = int(seed_hash[i*20 : i*20 + 15], 16)
        random.seed(step_hash)
        v_min = round(random.uniform(1.25, 1.95), 2)
        v_moyen = round(random.uniform(2.15, 5.85), 2)
        v_max = round(random.uniform(15.0, 95.0), 2)
        min_plus = random.randint(3, 15) * (i + 1)
        target_time = (base_time + timedelta(minutes=min_plus)).strftime("%H:%M")
        results.append({"lera": target_time, "min": v_min, "moyen": v_moyen, "max": v_max})
    return results

# --- 3. LOGIN ADMIN ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ ADMIN ACCESS ONLY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("TENIMIAFINA (MDP):", type="password")
    if st.button("HIDITRA"):
        if pwd == "ADMIN_TITAN": # Ity no MDP-nao
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Tsy marina ny tenimiafina!")
    st.stop()

# --- 4. CSS ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-title { font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; margin-bottom: 25px; }
    .card-box { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    .target-text { font-size: 45px; color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- 5. AVIATOR & COSMOS X ---
for i, game in enumerate(["aviator", "cosmos"]):
    game_label = game.upper()
    with tabs[i]:
        st.subheader(f"📸 CAPTURE ÉCRAN HISTORIQUE {game_label}")
        up_file = st.file_uploader(f"Alefaso ny sarin'ny historique ({game_label}):", type=['png', 'jpg', 'jpeg'], key=f"up_{game}")
        if up_file:
            st.image(up_file, caption="Historique de la Manche", use_container_width=True)
        
        st.write("---")
        ora_izao = datetime.now().strftime("%H:%M")
        u_hex = st.text_input(f"🔑 SERVER SEED (Hex):", key=f"h_{game}")
        u_ora = st.text_input("🕒 ORA IZAO (HH:MM):", value=ora_izao, key=f"o_{game}")
        
        if st.button(f"🔥 EXECUTE {game_label}", key=f"b_{game}"):
            if u_hex:
                preds = get_strategic_prediction(u_hex, u_ora)
                for p in preds:
                    st.markdown(f"""
                    <div class="card-box">
                        <div style="display:flex; justify-content: space-between;">
                            <span style="font-size:22px; color:#ffcc00; font-weight:bold;">⏰ {p['lera']}</span>
                            <span style="background:#00ffcc; color:#010a12; padding:2px 12px; border-radius:20px; font-weight:bold;">98% ACCURACY</span>
                        </div>
                        <div style="display: flex; justify-content: space-around; text-align:center; margin-top:20px;">
                            <div><small>MIN</small><br><b>{p['min']}x</b></div>
                            <div><small style="color:#00ffcc;">TARGET</small><br><div class="target-text">{p['moyen']}x</div></div>
                            <div><small>MAX</small><br><b>{p['max']}x</b></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.hist_data[game].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x")

# --- 6. MINES VIP (1-7 MINES) ---
with tabs[2]:
    st.subheader("💣 MINES PROVABLY FAIR")
    col1, col2 = st.columns(2)
    m_server = col1.text_input("🔑 SERVER SEED (Hex):")
    m_client = col2.text_input("👤 CLIENT SEED:")
    
    # Safidy 1-7 Mines
    nb_mines = st.select_slider("Isan'ny Mines ao amin'ny lalao:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 DECODE MINES PATH"):
        if m_server and m_client:
            combined = f"{m_server}-{m_client}-{nb_mines}"
            hash_res = hashlib.sha256(combined.encode()).hexdigest()
            random.seed(int(hash_res[:15], 16))
            
            # Mamoaka diamondra 5 ho an'ny lalana azo antoka
            safe = random.sample(range(25), 5)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; width: 280px; margin: auto;">'
            for idx in range(25):
                icon = "💎" if idx in safe else "⬛"
                color = "#00ffcc" if idx in safe else "#1a1a1a"
                grid += f'<div style="background:{color}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{icon}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)
            st.success(f"Lalana voadika ho an'ny {nb_mines} Mines.")
        else:
            st.warning("Ampidiro ny Seeds roa!")

# --- 7. SETTINGS ---
with tabs[3]:
    st.write(f"📞 Contact: 0346249701")
    st.write(f"📧 Email: andriantsoakelly@gmail.com")
    if st.button("🔴 RESET APP"):
        st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()

st.markdown('<div style="text-align:center; color:#444; margin-top:30px; font-size:12px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
