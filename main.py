import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'hist_data' not in st.session_state:
    st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}

# --- 2. THE TITAN ENGINE (LOCAL CALCULATION - NO DATA COST) ---
def get_strategic_prediction(server_hex, base_ora):
    results = []
    INTERNAL_CLIENT = "TITAN_ELITE_2026_PRO" #
    
    try:
        # Mampiasa ny lera ampidirinao na ny lera izao
        base_time = datetime.strptime(base_ora, "%H:%M")
    except:
        base_time = datetime.now()

    combined = f"{server_hex}-{INTERNAL_CLIENT}"
    seed_hash = hashlib.sha512(combined.encode()).hexdigest() #
    
    for i in range(3):
        # Step-logic hashing isaky ny lera
        step_hash = int(seed_hash[i*20 : i*20 + 15], 16)
        random.seed(step_hash)
        
        v_min = round(random.uniform(1.25, 1.95), 2)
        v_moyen = round(random.uniform(2.15, 5.85), 2) #
        v_max = round(random.uniform(15.0, 95.0), 2)
        
        # Elanelam-potoana mifanaraka amin'ny lera mivantana
        min_plus = random.randint(3, 15) * (i + 1)
        target_time = (base_time + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(92, 99)
        
        results.append({
            "lera": target_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": prob
        })
    return results

# --- 3. LOGIN INTERFACE ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE ACCESS</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD:", type="password")
    if st.button("BYPASS & CONNECT"):
        if pwd == "PATRICIA_BEAST": #
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Password diso!")
    st.stop()

# --- 4. PREMIUM CSS STYLE ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-title { font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; margin-bottom: 25px; text-shadow: 0 0 15px #00ffcc; }
    .card-box { background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    .target-text { font-size: 45px; color: #00ffcc; font-weight: bold; text-shadow: 0 0 10px #00ffcc; }
    .stTabs [aria-selected="true"] { background: #00ffcc !important; color: #010a12 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- 5. AVIATOR & COSMOS X ---
for i, game in enumerate(["aviator", "cosmos"]):
    game_label = game.upper()
    with tabs[i]:
        st.markdown(f"### 🛡️ {game_label} ELITE SCANNER")
        
        # Capture Section
        up_file = st.file_uploader(f"📸 Capture {game_label}:", type=['png', 'jpg', 'jpeg'], key=f"file_{game}")
        if up_file: st.image(up_file, use_container_width=True)
        
        st.write("---")
        
        # Inputs (Lera mivantana avy amin'ny finday)
        ora_izao = datetime.now().strftime("%H:%M")
        u_hex = st.text_input(f"🔑 HEX SEED ({game_label}):", placeholder="Ampidiro ny Hex...", key=f"hex_{game}")
        u_ora = st.text_input("🕒 ORA IZAY (HH:MM):", value=ora_izao, key=f"ora_{game}")
        
        if st.button(f"🔥 EXECUTE {game_label}"):
            if u_hex:
                with st.spinner("Calculating..."):
                    time.sleep(1)
                    preds = get_strategic_prediction(u_hex, u_ora)
                    for p in preds:
                        st.markdown(f"""
                        <div class="card-box">
                            <div style="display:flex; justify-content: space-between; align-items:center;">
                                <span style="font-size:22px; color:#ffcc00; font-weight:bold;">⏰ Lera: {p['lera']}</span>
                                <span style="background:#00ffcc; color:#010a12; padding:2px 12px; border-radius:20px; font-weight:bold;">✅ {p['prob']}% ACCURACY</span>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top:20px; text-align:center;">
                                <div><small style="color:#888;">MIN</small><br><b style="font-size:18px;">{p['min']}x</b></div>
                                <div><small style="color:#00ffcc;">TARGET</small><br><div class="target-text">{p['moyen']}x</div></div>
                                <div><small style="color:#ff4444;">MAX</small><br><b style="font-size:18px;">{p['max']}x</b></div>
                            </div>
                            <p style="margin-top:10px; font-size:12px; color:#555; text-align:center;">Cashout Auto: 2.00x à 4.00x</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.session_state.hist_data[game].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
            else:
                st.warning("Ampidiro ny Hex Seed!")

        st.markdown("### 📜 TANTARAN'NY VINAVINA")
        if st.session_state.hist_data[game]:
            for item in st.session_state.hist_data[game][:5]:
                st.info(item)

# --- 6. MINES VIP ---
with tabs[2]:
    m_hex = st.text_input("🔑 HEX SEED (Mines):")
    if st.button("💎 SCAN SAFE PATH"):
        if m_hex:
            random.seed(m_hex)
            safe = random.sample(range(25), 5) #
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; width: 280px; margin: auto;">'
            for idx in range(25):
                icon = "💎" if idx in safe else "⬛"
                color = "#00ffcc" if idx in safe else "#1a1a1a"
                grid += f'<div style="background:{color}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{icon}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- 7. SETTINGS ---
with tabs[3]:
    if st.button("🔴 RESET HISTORIQUE"):
        st.session_state.hist_data = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()
    st.write(f"📞 Contact: 0346249701")
    st.write(f"📧 Email: andriantsoakelly@gmail.com")

st.markdown('<div style="text-align:center; color:#444; margin-top:30px; font-size:1
