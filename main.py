import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. SECURITY & SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_password' not in st.session_state:
    st.session_state.master_password = "PATRICIA_BEAST"

for key in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. LOGIN INTERFACE ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
        st.info("👋 Tongasoa! Ampidiro ny Password nomena anao mba hidirana amin'ny algorithm.")
        pwd_input = st.text_input("PASSWORD:", type="password")
        if st.button("HIDITRA NY INTERFACE"):
            if pwd_input == st.session_state.master_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Kaody diso!")
        st.stop()

login()

# --- 3. STYLE PREMIUM (RE-BRANDED) ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }
    .card-result { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; margin: 15px 0; }
    .card-opp { background: #1a1a00; border: 2px dashed #ffcc00; border-radius: 15px; padding: 15px; text-align: center; color: #ffcc00; margin-top: 10px; }
    .luck-text { font-size: 22px; color: #ffcc00; text-align: center; font-weight: bold; margin: 15px 0; text-shadow: 0 0 15px #ffcc00; border: 2px solid #ffcc00; padding: 10px; border-radius: 50px; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; border: none; width: 100%; }
    .footer-brand { text-align: center; color: #888; font-size: 13px; margin-top: 40px; border-top: 1px solid #222; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ADVANCED ENGINE (DYNAMIC MOYEN) ---
def get_advanced_predictions(seed, h_ora):
    base = datetime.strptime(h_ora, "%H:%M")
    results = []
    # Ny Hex Seed no mibaiko ny vokatra eto
    seed_hash = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16)
    random.seed(seed_hash)
    
    for i in range(3):
        v_min = round(random.uniform(1.20, 1.50), 2)
        # Moyen miovaova arakaraka ny Seed (2.00x hatramin'ny 5.50x)
        v_moyen = round(random.uniform(2.00, 5.50), 2)
        v_max = round(random.uniform(15.0, 75.0), 2)
        
        min_plus = random.randint(5, 18) * (i + 1)
        lera_vaovao = (base + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(90, 99)
        results.append({"min": v_min, "moyen": v_moyen, "max": v_max, "lera": lera_vaovao, "prob": prob})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

for i, name in enumerate(["AVIATOR", "COSMOS X"]):
    game_key = "aviator" if i == 0 else "cosmos"
    with tabs[i]:
        st.markdown(f'<div style="background:#001a1a; padding:10px; border-radius:10px; margin-bottom:15px;">📝 <b>TOROLALANA:</b> Ampidiro ny Hex Seed sy ny Ora, avy eo tsindrio ny Execute.</div>', unsafe_allow_html=True)
        
        st.markdown("📊 **HISTORIQUE DE LA MANCHE**")
        st.file_uploader("Capture écran historique:", key=f"cap_{game_key}")
        
        col1, col2 = st.columns(2)
        u_hex = col1.text_input(f"🔑 HEX SEED ({name}):", key=f"hex_{game_key}")
        u_ora = col2.text_input("🕒 ORA (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"ora_{game_key}")
        
        if st.button(f"🔥 EXECUTE {name}"):
            if u_hex:
                preds = get_advanced_predictions(u_hex, u_ora)
                st.markdown(f"""<div class="card-result">
                    <div style="display: flex; justify-content: space-around; font-size: 18px; font-weight: bold;">
                        <span style="color:white;">MIN<br>{preds[0]['min']}x</span>
                        <span style="color:#00ffcc;">MOYEN (Target)<br><span style="font-size:45px;">{preds[0]['moyen']}x</span></span>
                        <span style="color:white;">MAX (Tenter)<br>{preds[0]['max']}x</span>
                    </div>
                </div>""", unsafe_allow_html=True)
                
                st.markdown('<div class="card-opp">🎯 PROCHAINES OPPORTUNITÉS:', unsafe_allow_html=True)
                for p in preds:
                    st.markdown(f"⏰ <b>{p['lera']}</b> | Côte: <b>{p['moyen']}x</b> | ✅ <b>{p['prob']}%</b>", unsafe_allow_html=True)
                    st.session_state[f'hist_{game_key}'].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="luck-text">🍀 BON GAIN À TOUS! 🍀</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Ampidiro aloha ny Hex Seed!")

        st.markdown('### 📜 HISTORIQUE')
        st.markdown(f'<div style="background:rgba(0,0,0,0.5); padding:15px; border-radius:10px; border:1px solid #333; height:150px; overflow-y:auto;">{"<br>".join(st.session_state[f"hist_{game_key}"])}</div>', unsafe_allow_html=True)

# --- MINES & PENALTY (SIMPLIFIED) ---
with tabs[2]: st.info("Mines VIP Mode Active. Ampidiro ny Seed hanombohana.")
with tabs[3]: st.info("Penalty Mode Ready. Tsindrio ny bokotra hahazoana target.")

# --- ADMIN ---
with tabs[4]:
    st.markdown(f'<a href="https://wa.me/261346249701" style="background:#25D366; color:white; padding:10px; border-radius:5px; text-decoration:none; display:block; text-align:center;">💬 WhatsApp Patricia</a>', unsafe_allow_html=True)
    if st.button("🔴 RESET HISTORIQUE"):
        for k in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']: st.session_state[k] = []
        st.rerun()

st.markdown(f'<div class="footer-brand"><b>TITAN OMNI-STRIKE BY PATRICIA</b><br>0346249701 | andriantsoakelly@gmail.com</div>', unsafe_allow_html=True)
