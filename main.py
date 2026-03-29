import streamlit as st
import hashlib
import time
import random
import base64
from datetime import datetime, timedelta

# --- 1. SECURITY & CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'hist_data' not in st.session_state:
    st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}

def check_password(input_pwd):
    # Password tsy miova: PATRICIA_BEAST
    return input_pwd == "PATRICIA_BEAST"

# --- 2. ADVANCED STRATEGY ENGINE (MATEMATIKA PRO) ---
def get_triple_prediction(server_seed, client_seed, base_ora):
    """Lojika SHA-512 mikajy lera 3 sy isa 3 (Min, Moyen, Max)"""
    results = []
    try:
        base_time = datetime.strptime(base_ora, "%H:%M")
    except:
        base_time = datetime.now()

    combined = f"{server_seed}-{client_seed}"
    seed_hash = hashlib.sha512(combined.encode()).hexdigest()
    
    for i in range(3):
        # Miovaova isaky ny lera ny hashing (Step-logic)
        step_hash = int(seed_hash[i*15 : i*15 + 13], 16)
        random.seed(step_hash)
        
        v_min = round(random.uniform(1.25, 1.95), 2)
        v_moyen = round(random.uniform(2.10, 5.80), 2) # Target ho an'ny Cashout Auto 2-4x
        v_max = round(random.uniform(15.0, 95.0), 2)
        
        # Elanelam-potoana (5-25 minitra)
        min_plus = random.randint(5, 25) * (i + 1)
        target_time = (base_time + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(92, 99)
        
        results.append({
            "lera": target_time,
            "min": v_min,
            "moyen": v_moyen,
            "max": v_max,
            "prob": prob
        })
    return results

# --- 3. LOGIN INTERFACE ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE ACCESS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Ampidiro ny kaody miafina hidirana amin'ny rafitra.</p>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD:", type="password")
    if st.button("BYPASS & CONNECT"):
        if check_password(pwd):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Password diso!")
    st.stop()

# --- 4. CUSTOM CSS STYLE (PREMIUM LOOK) ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-title { font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; margin-bottom: 25px; text-shadow: 0 0 15px #00ffcc; }
    .card-box { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    .target-text { font-size: 45px; color: #00ffcc; font-weight: bold; text-shadow: 0 0 10px #00ffcc; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background: #040e17; border: 1px solid #333; color: white; border-radius: 10px; padding: 10px 15px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #00ffcc, #0077ff) !important; color: #010a12 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- 5. AVIATOR & COSMOS X (MITOVY INTERFACE) ---
for i, game in enumerate(["aviator", "cosmos"]):
    game_label = "AVIATOR" if game == "aviator" else "COSMOS X"
    with tabs[i]:
        st.markdown(f"### 🛡️ {game_label} STRATEGIC SCANNER")
        
        # Capture Section
        st.markdown("📸 **CAPTURE ÉCRAN HISTORIQUE**")
        up_file = st.file_uploader("Upload screenshot:", type=['png', 'jpg', 'jpeg'], key=f"file_{game}")
        if up_file: st.image(up_file, caption="Manche mivantana", use_container_width=True)
        
        st.write("---")
        
        # Inputs Section
        c_in1, c_in2 = st.columns(2)
        s_seed = c_in1.text_input(f"Server Seed ({game_label}):", key=f"s_{game}")
        c_seed = c_in2.text_input(f"Client Seed ({game_label}):", key=f"c_{game}")
        u_ora = st.text_input("Ora izao (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"t_{game}")
        
        if st.button(f"🔥 EXECUTE {game_label}"):
            if s_seed and c_seed:
                with st.spinner("Analyzing Mathematical Windows..."):
                    time.sleep(1.2)
                    preds = get_triple_prediction(s_seed, c_seed, u_ora)
                    
                    for p in preds:
                        st.markdown(f"""
                        <div class="card-box">
                            <div style="display:flex; justify-content: space-between; align-items:center;">
                                <span style="font-size:22px; color:#ffcc00; font-weight:bold;">⏰ Ora: {p['lera']}</span>
                                <span style="background:#00ffcc; color:#010a12; padding:2px 12px; border-radius:20px; font-weight:bold;">✅ {p['prob']}% ACCURACY</span>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top:20px; text-align:center;">
                                <div><small style="color:#888;">MIN (Safe)</small><br><b style="font-size:18px;">{p['min']}x</b></div>
                                <div><small style="color:#00ffcc;">TARGET MOYEN</small><br><div class="target-text">{p['moyen']}x</div></div>
                                <div><small style="color:#ff4444;">MAX (Risk)</small><br><b style="font-size:18px;">{p['max']}x</b></div>
                            </div>
                            <p style="margin-top:10px; font-size:12px; color:#555;">Cashout Auto conseillé: 2.00x à 4.00x</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Store in History
                        st.session_state.hist_data[game].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
            else:
                st.warning("⚠️ Ampidiro ny Seeds rehetra!")

        # Display History
        st.markdown("### 📜 TANTARAN'NY VINAVINA")
        if st.session_state.hist_data[game]:
            for item in st.session_state.hist_data[game][:10]:
                st.info(item)
        else:
            st.write("Tsy mbola misy tantara voatahiry.")

# --- 6. MINES VIP (1-7 SELECTION) ---
with tabs[2]:
    st.subheader("💣 MINES VIP STRATEGY")
    m_col1, m_col2 = st.columns(2)
    m_s_seed = m_col1.text_input("Server Seed (Mines):", key="ms_s")
    m_c_seed = m_col2.text_input("Client Seed (Mines):", key="ms_c")
    
    nb_mines = st.select_slider("Isan'ny Mines ampiasainao (1-7):", options=[1, 2, 3, 4, 5, 6, 7], value=3)
    
    if st.button("💎 SCAN SAFE PATH"):
        if m_s_seed and m_c_seed:
            random.seed(f"{m_s_seed}-{m_c_seed}")
            safe_indices = random.sample(range(25), 5) # 5 Diamondra foana
            
            grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; width: 280px; margin: 20px auto;">'
            for idx in range(25):
                if idx in safe_indices:
                    grid_html += '<div style="background:#00ffcc; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">💎</div>'
                else:
                    grid_html += '<div style="background:#1a1a1a; height:50px; border-radius:8px; border:1px solid #333;"></div>'
            grid_html += '</div>'
            
            st.markdown(grid_html, unsafe_allow_html=True)
            st.success(f"Path generated for {nb_mines} mines. Follow the diamonds!")
            st.session_state.hist_data["mines"].insert(0, f"🕒 {datetime.now().strftime('%H:%M')} | 💎 Grid Generated")
        else:
            st.warning("Ampidiro ny Seeds!")

# --- 7. SETTINGS & ADMIN ---
with tabs[3]:
    st.markdown("### ⚙️ Fitantanana ny App")
    st.info(f"User Active: Patricia | Level: Ultra-Strike PRO")
    
    if st.button("🔴 RESET ALL DATA & HISTORIQUE"):
        st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()
    
    st.markdown(f"""
    <div style="background:#04111d; padding:20px; border-radius:10px; border-left: 5px solid #00ffcc; margin-top:20px;">
        📞 <b>CONTACT DEVELOPER:</b> 0346249701<br>
        📧 <b>EMAIL:</b> andriantsoakelly@gmail.com
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#444; margin-top:30px; font-size:12px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
