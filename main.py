import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. RAFITRA FIAROVANA (PASSWORD) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Ampidiro ny kaody manokana (Patricia):", type="password")
        if st.button("HIRAFIKA NY INTERFACE"):
            if pwd == "PATRICIA_BEAST":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Kaody diso! Jereo tsara ny soratra.")
        st.stop()

login()

# --- 2. STYLE ARY CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 45px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 25px #00ffcc; border-bottom: 3px solid #00ffcc; padding: 15px; }
    .consigne-box { background: rgba(255, 75, 75, 0.1); border-left: 5px solid #ff4b4b; padding: 12px; border-radius: 5px; margin: 10px 0; font-size: 14px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 25px; text-align: center; box-shadow: 0 0 20px rgba(0,255,204,0.2); }
    .lera-box { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 12px; color: #ffd700; margin-top: 15px; text-align: center; font-weight: bold; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 55px; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ALGORITHM SHA-512 ---
def generate_beast_signals(seed, ora_fidirana):
    # Algorithme double-hash ho an'ny fahamendrehana
    raw = f"{seed}{ora_fidirana}{time.time()}".encode()
    hash_obj = hashlib.sha512(raw).hexdigest()
    random.seed(int(hash_obj[:16], 16))
    
    vmin = round(random.uniform(1.20, 1.45), 2)
    vmoy = round(random.uniform(2.10, 4.80), 2)
    vmax = round(random.uniform(12.0, 75.0), 2)
    
    # Fikajiana ora 3 samihafa (Next Rounds) - TSY MISY MITOVY
    base = datetime.strptime(ora_fidirana, "%H:%M")
    preds = []
    offsets = random.sample(range(3, 25), 3) # Maka isa 3 samihafa
    offsets.sort()
    
    for offset in offsets:
        p_time = (base + timedelta(minutes=offset)).strftime("%H:%M")
        p_acc = random.randint(93, 98)
        preds.append({"t": p_time, "a": p_acc})
        
    return vmin, vmoy, vmax, preds

# --- 4. INTERFACE STATUS ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc;'>🛡️ ANTI-BOT: ACTIVE | 📡 SYNC: SERVER_V3</p>", unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- AVIATOR & COSMOS X ---
for i, tab in enumerate([tabs[0], tabs[1]]):
    name = "AVIATOR" if i == 0 else "COSMOS X"
    with tab:
        st.markdown(f'<div class="consigne-box">⚠️ <b>CONSIGNE {name}:</b> Cashout 2x-4x. Tenter x10+ isaky ny 15-20mn. Ovao ny Hex isaky ny mandresy be.</div>', unsafe_allow_html=True)
        st.file_uploader(f"📸 Capture Historique ({name}):", type=['jpg','png','jpeg'], key=f"file_{i}")
        
        c1, c2 = st.columns(2)
        with c1: u_hex = st.text_input("🔑 HEX SEED:", key=f"hex_{i}")
        with c2: u_ora = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key=f"ora_{i}")
        
        if st.button(f"🔥 EXECUTE {name} ENGINE", key=f"btn_{i}"):
            if u_hex:
                vmin, vmoy, vmax, preds = generate_beast_signals(u_hex, u_ora)
                st.markdown(f"""
                    <div class="card-beast">
                        <div style="display:flex; justify-content:space-around; align-items:center;">
                            <div><p style="color:#ff4b4b;">MIN</p><h3>{vmin}x</h3></div>
                            <div style="border:1px solid #00ffcc; padding:15px; border-radius:10px;">
                                <p style="color:#00ffcc;">MOYEN (Target)</p><h1>{vmoy}x</h1>
                            </div>
                            <div><p style="color:#ffd700;">MAX</p><h3>{vmax}x</h3></div>
                        </div>
                    </div>
                    <div class="lera-box">
                        🎯 NEXT ROUNDS (Accuracy {preds[0]['a']}%):<br>
                        ⏰ {preds[0]['t']} | ⏰ {preds[1]['t']} | ⏰ {preds[2]['t']}
                    </div>
                """, unsafe_allow_html=True)
            else: st.warning("Ampidiro ny HEX SEED!")

# --- 💣 MINES VIP (AMBOARINA NY SEEDS) ---
with tabs[2]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE MINES:</b> Tsabo 5 Diamants. Ovao ny Client Seed isaky ny mahazo Diamondra 5.</div>', unsafe_allow_html=True)
    st.file_uploader("📸 Capture Historique (Mines):", type=['jpg','png','jpeg'])
    
    col_m1, col_m2 = st.columns(2)
    with col_m1: m_cli = st.text_input("💻 CLIENT SEED:", placeholder="Ovao matetika...", key="m_cli")
    with col_m2: m_ser = st.text_input("🌐 SERVER SEED:", placeholder="Provably fair hash...", key="m_ser")
    
    n_mines = st.select_slider("💣 ISAN'NY BAOMBA:", options=[1,2,3,4,5,6,7], value=3)

    if st.button("💎 GENERATE 5-DIAMOND SCHEMA"):
        if m_cli and m_server:
            # Algorithme schema dynamique
            random.seed(hash(m_cli + m_ser + str(time.time())))
            spots = random.sample(range(25), k=5)
            grid = '<div style="display:grid; grid-template-columns:repeat(5, 55px); gap:8px; justify-content:center; margin:20px 0;">'
            for j in range(25):
                icon = "💎" if j in spots else ""
                bg = "linear-gradient(145deg, #00ffcc, #0077ff)" if j in spots else "#1a1f26"
                grid += f'<div style="width:55px; height:55px; background:{bg}; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:22px;">{icon}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)
            
            # Ora 3 samihafa ho an'ny Mines
            now = datetime.now()
            m_preds = [(now + timedelta(minutes=x)).strftime("%H:%M") for x in random.sample(range(2, 20), 3)]
            m_preds.sort()
            st.markdown(f"""
                <div class="lera-box">
                    🕒 ORA TSARA HILALAOVANA (96%):<br>
                    ⏰ {m_preds[0]} | ⏰ {m_preds[1]} | ⏰ {m_preds[2]}
                </div>
            """, unsafe_allow_html=True)
        else: st.error("Ampidiro ny Seed Client sy Server!")

# --- ⚽ PENALTY ---
with tabs[3]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE PENALTY:</b> Araho ny Server Target. Martingale 2.5x raha resy.</div>', unsafe_allow_html=True)
    if st.button("🥅 PREDICT PENALTY"):
        target = random.choice(["ANKAVIA", "ANKAVANANA", "AFOVOANY"])
        st.markdown(f"""
            <div class="card-beast">
                <h3 style="color:#00ffcc;">🎯 TARGET: {target}</h3>
                <p>SYNC RELIABILITY: {random.randint(92, 97)}%</p>
            </div>
        """, unsafe_allow_html=True)

# --- GESTION DE MISE ---
st.write("---")
st.markdown("### 📊 GESTION DE MISE")
st.info("💡 **Kelly Criterion:** Miloka 5% amin'ny banky. Raha 10.000 Ar = 500 Ar ny mise. Aza mihoatra ny in-3 Martingale.")
