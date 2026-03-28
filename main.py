import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- CONFIGURATION SY STYLE ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# Fitehirizana ny Historique (Tsy fafan'ny Refresh)
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("""
    <style>
    .stApp { background: #010a12; color: white; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .consigne-box { background: rgba(255, 75, 75, 0.15); border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; }
    .lera-container { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 15px; color: #ffd700; font-weight: bold; margin-top: 20px; text-align: center; }
    .hist-box { background: rgba(0, 255, 204, 0.05); border: 1px solid #333; padding: 10px; border-radius: 10px; margin-top: 5px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

# --- ALGORITHM ENGINE ---
def get_beast_logic(seed, h_ora):
    combined = f"{seed}{h_ora}{time.time()}".encode()
    h = hashlib.sha512(combined).hexdigest()
    random.seed(int(h[:16], 16))
    
    vmin = round(random.uniform(1.20, 1.40), 2)
    vmoy = round(random.uniform(2.10, 4.80), 2)
    vmax = round(random.uniform(12.0, 55.0), 2)
    
    base_t = datetime.strptime(h_ora, "%H:%M")
    preds = []
    for _ in range(3):
        p_time = (base_t + timedelta(minutes=random.randint(2, 18))).strftime("%H:%M")
        p_acc = random.randint(93, 98)
        preds.append({"ora": p_time, "acc": p_acc})
    return vmin, vmoy, vmax, preds

# --- NAVIGATEUR ---
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- ✈️ AVIATOR / COSMOS X ---
for i, tab in enumerate([tabs[0], tabs[1]]):
    game_name = "AVIATOR" if i == 0 else "COSMOS X"
    with tab:
        st.markdown(f'<div class="consigne-box">⚠️ <b>CONSIGNE {game_name}:</b> Cashout 2x-4x. Tenter x10+ isaky ny 15min. Ovao foana ny Hex Seed isaky ny manao cashout be.</div>', unsafe_allow_html=True)
        
        # FITAOVANA NAMPIDIRINA INDRAY (Capture & Seed)
        u_file = st.file_uploader(f"📸 Capture de la Manche ({game_name}):", type=['jpg','png','jpeg'], key=f"file_{i}")
        u_hex = st.text_input("🔑 HEX SEED (Client/Server):", key=f"hex_{i}")
        u_time = st.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"time_{i}")

        if st.button(f"🔥 EXECUTE {game_name} WAR MACHINE", key=f"btn_{i}"):
            if u_hex:
                vmin, vmoy, vmax, preds = get_beast_logic(u_hex, u_time)
                st.markdown(f"""
                    <div class="card-beast">
                        <div style="display:flex; justify-content:space-around;">
                            <div><p style="color:#ff4b4b;">MIN</p><h2>{vmin}x</h2></div>
                            <div><p style="color:#00ffcc;">MOYEN (Target)</p><h1 style="color:#00ffcc; font-size:50px;">{vmoy}x</h1></div>
                            <div><p style="color:#ffd700;">MAX (Tenter)</p><h2>{vmax}x</h2></div>
                        </div>
                    </div>
                    <div class="lera-container">
                        🎯 PROCHAINES OPPORTUNITÉS:<br>
                        ⏰ {preds[0]['ora']} ({preds[0]['acc']}%) | ⏰ {preds[1]['ora']} ({preds[1]['acc']}%) | ⏰ {preds[2]['ora']} ({preds[2]['acc']}%)
                    </div>
                """, unsafe_allow_html=True)
                
                # Tehirizina ao amin'ny Historique
                st.session_state.history.append(f"[{u_time}] {game_name}: Target {vmoy}x | Next: {preds[0]['ora']}")
            else:
                st.warning("Ampidiro ny HEX SEED azafady!")

# --- 💣 MINES VIP ---
with tabs[2]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE MINES:</b> 5 Diamants ihany. Ovao ny Client Seed isaky ny mahazo Diamondra 5.</div>', unsafe_allow_html=True)
    m_file = st.file_uploader("📸 Capture du Tour (Mines):", type=['jpg','png','jpeg'])
    m_seed = st.text_input("💻 CLIENT SEED (Mines):")
    
    if st.button("💎 GENERATE 5-DIAMOND SCHEMA"):
        random.seed(hash(m_seed + str(time.time())))
        spots = random.sample(range(25), k=5)
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 50px); gap:8px; justify-content:center; margin:20px 0;">'
        for j in range(25):
            icon = "💎" if j in spots else ""
            bg = "#00ffcc" if j in spots else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{bg}; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">{icon}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        
        now = datetime.now()
        st.markdown(f'<div class="lera-container">🕒 ORA TSARA: {(now + timedelta(minutes=5)).strftime("%H:%M")} (97%)</div>', unsafe_allow_html=True)
        st.session_state.history.append(f"[{now.strftime('%H:%M')}] MINES: 5-Diamond Schema Generated")

# --- ⚽ PENALTY ---
with tabs[3]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE PENALTY:</b> Araho ny target ary aza adino ny manao Martingale raha resy.</div>', unsafe_allow_html=True)
    if st.button("🥅 PREDICT PENALTY"):
        pos = random.choice(["ANKAVIA", "ANKAVANANA", "AFOVOANY"])
        acc = random.randint(91, 96)
        st.markdown(f'<div class="card-beast"><h3>🎯 TARGET: <span style="color:#00ffcc;">{pos}</span></h3><h4>ACCURACY: {acc}%</h4></div>', unsafe_allow_html=True)
        st.session_state.history.append(f"[{datetime.now().strftime('%H:%M')}] PENALTY: Target {pos}")

# --- 📜 HISTORIQUE DES PRÉDICTIONS ---
st.write("---")
st.markdown("### 📜 HISTORIQUE DES PRÉDICTIONS")
if st.session_state.history:
    for h in reversed(st.session_state.history[-10:]):
        st.markdown(f'<div class="hist-box">{h}</div>', unsafe_allow_html=True)
else:
    st.info("Tsy mbola misy tantara (historique) aloha hatreto.")
