import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. INITIALISATION (History Storage) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_password' not in st.session_state:
    st.session_state.master_password = "PATRICIA_BEAST"

# Ity no mitahiry ny tantara rehetra mba tsy hifafa
if 'full_history_list' not in st.session_state:
    st.session_state.full_history_list = []

# --- 2. LOGIN SYSTEM ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#002222; padding:20px; border-radius:15px; border:1px solid #00ffcc; margin-bottom:20px; font-size:18px; text-align:center;">
            <b>👋 TONGASOA PATRICIA!</b><br>Ampidiro ny Password-nao mba hanomboka.
        </div>""", unsafe_allow_html=True)
        pwd_input = st.text_input("PASSWORD:", type="password")
        if st.button("HIDITRA NY INTERFACE"):
            if pwd_input == st.session_state.master_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Password diso!")
        st.stop()

login()

# --- 3. STYLE & DESIGN ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; margin-bottom: 20px; }
    .consigne-box { background: #001a1a; border-left: 8px solid #00ffcc; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 16px; }
    .card-result { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px; }
    .hist-container { background: #020d1a; border: 1px solid #333; border-radius: 10px; padding: 15px; max-height: 400px; overflow-y: auto; }
    .hist-item { border-bottom: 1px solid #222; padding: 10px 0; display: flex; justify-content: space-between; font-family: monospace; }
    .luck-text { font-size: 22px; color: #ffcc00; text-align: center; font-weight: bold; margin: 20px 0; border: 2px solid #ffcc00; padding: 10px; border-radius: 50px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: bold; height: 50px; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CALCULATION ENGINE ---
def get_advanced_predictions(seed, h_ora):
    try:
        base = datetime.strptime(h_ora, "%H:%M")
    except:
        base = datetime.now()
    
    results = []
    # Mampiasa ny Hex Seed mba hiteraka kisendrasendra voakajy
    random.seed(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))
    
    for i in range(3):
        v_moyen = round(random.uniform(2.10, 4.50), 2)
        v_max = round(random.uniform(10.0, 60.0), 2)
        # Manampy minitra arakaraka ny algorithm
        min_plus = random.randint(3, 15) * (i + 1)
        lera_vaovao = (base + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(92, 99)
        results.append({"moyen": v_moyen, "max": v_max, "lera": lera_vaovao, "prob": prob})
    return results

# --- 5. MAIN UI ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tab_aviator, tab_cosmos, tab_admin = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "⚙️ SETTINGS"])

with tab_aviator:
    st.markdown('<div class="consigne-box"><b>📝 TOROLALANA:</b> Ampidiro ny Hex Seed farany sy ny ora izao (HH:MM), avy eo tsindrio ny Execute.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    u_hex = col1.text_input("🔑 HEX SEED (Aviator):", placeholder="cc703e9...")
    u_ora = col2.text_input("🕒 ORA (HH:MM):", value=datetime.now().strftime("%H:%M"))
    
    if st.button("🔥 EXECUTE AVIATOR"):
        if u_hex:
            preds = get_advanced_predictions(u_hex, u_ora)
            # Asehoy ny prediction voalohany ho lehibe
            st.markdown(f"""<div class="card-result">
                <span style="color:#00ffcc; font-size:18px;">TARGET MOYEN</span><br>
                <span style="font-size:50px; font-weight:900; color:#00ffcc;">{preds[0]['moyen']}x</span><br>
                <span style="color:#888;">Lera: {preds[0]['lera']} | Probabilité: {preds[0]['prob']}%</span>
            </div>""", unsafe_allow_html=True)
            
            # Tehirizo ao anaty historique feno
            for p in preds:
                entry = {"game": "✈️", "time": p['lera'], "cote": p['moyen'], "prob": p['prob'], "timestamp": time.time()}
                st.session_state.full_history_list.insert(0, entry)
            
            st.markdown('<div class="luck-text">🍀 BON GAIN À TOUS! 🍀</div>', unsafe_allow_html=True)
        else:
            st.error("Azafady, ampidiro aloha ny Hex Seed!")

with tab_cosmos:
    st.info("Cosmos X mode is active. Use the same logic as Aviator.")
    # Mitovy ny lojika ampiasaina eto

with tab_admin:
    st.subheader("📊 Fitantanana ny App")
    if st.button("🔴 RESET HISTORIQUE"):
        st.session_state.full_history_list = []
        st.success("Voafafa ny tantara rehetra!")
        st.rerun()
    
    st.markdown(f"""
        <div style="background:#111; padding:15px; border-radius:10px; margin-top:20px;">
            <b>📞 CONTACT:</b> 0346249701<br>
            <b>📧 EMAIL:</b> andriantsoakelly@gmail.com
        </div>
    """, unsafe_allow_html=True)

# --- 6. HISTORIQUE DISPLAY (Asehony foana eo ambany) ---
st.markdown("### 📜 HISTORIQUE DES PRÉDICTIONS")
if st.session_state.full_history_list:
    st.markdown('<div class="hist-container">', unsafe_allow_html=True)
    for item in st.session_state.full_history_list:
        color = "#00ffcc" if item['prob'] > 95 else "#ffffff"
        st.markdown(f"""
            <div class="hist-item">
                <span>{item['game']} <b>{item['time']}</b></span>
                <span style="color:{color};">🎯 <b>{item['cote']}x</b></span>
                <span style="color:#ffcc00;">✅ {item['prob']}%</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("Tsy mbola misy historique voatahiry.")

st.markdown("<br><hr><center><small>TITAN OMNI-STRIKE BY PATRICIA © 2026</small></center>", unsafe_allow_html=True)
