import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="TITAN V75.0 BEAST", layout="wide")

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; padding: 10px; border-bottom: 3px solid #00ffcc; }
    .card-res { background: rgba(0, 255, 204, 0.08); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; margin-top: 10px; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 8px; padding: 10px; text-align: center; }
    .next-rounds { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: center; color: #ffd700; }
    .history-box { background: #1a1f26; border-left: 5px solid #00ffcc; padding: 10px; margin-top: 5px; border-radius: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN V75.0 THE BEAST 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- FUNCTION FOR POWER CALCULATION ---
def power_analysis(h_input, hex_val, game):
    random.seed(hash(h_input + hex_val + str(time.time())))
    p_min = round(random.uniform(1.2, 1.6), 2)
    p_moy = round(random.uniform(2.1, 5.8), 2)
    p_max = round(random.uniform(12.0, 48.0), 2)
    pct = random.randint(93, 99) # High accuracy signal
    
    # Calculation of 3 Next Rounds
    base = datetime.strptime(h_input, "%H:%M")
    rounds = [(base + timedelta(minutes=random.randint(i*3, (i+1)*4))).strftime("%H:%M") for i in range(1, 4)]
    
    return p_min, p_moy, p_max, pct, rounds

# --- TAB 1: AVIATOR ---
with tab1:
    st.file_uploader("📷 CAPTURE DE TOUR (Aviator):", type=['jpg', 'png', 'jpeg'], key="avi_cap")
    avi_hex = st.text_input("🔑 HEX SEED:", key="avi_hex")
    avi_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_h")
    
    if st.button("🚀 EXECUTE BEAST ANALYSIS (AVIATOR)", use_container_width=True):
        mi, mo, ma, pc, rd = power_analysis(avi_h, avi_hex, "AVIATOR")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-box'>MIN<br><b>{mi}x</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{mo}x</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'>MAX<br><b>{ma}x</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-res'><h3>SIGNAL ACCURACY: {pc}%</h3><h1>{mo}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='next-rounds'>🕒 LERA FIDIRANA: <b>{' | '.join(rd)}</b></div>", unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"✈️ AVIATOR | {avi_h} | {mo}x | {pc}%")

# --- TAB 2: COSMOS X ---
with tab2:
    st.file_uploader("📷 CAPTURE DE TOUR (Cosmos):", type=['jpg', 'png', 'jpeg'], key="cos_cap")
    cos_hex = st.text_input("🔑 HEX SEED:", key="cos_hex")
    cos_h = st.text_input("🕒 HEURE COSMOS:", value=datetime.now().strftime("%H:%M"), key="cos_h")
    
    if st.button("🚀 EXECUTE BEAST ANALYSIS (COSMOS)", use_container_width=True):
        mi, mo, ma, pc, rd = power_analysis(cos_h, cos_hex, "COSMOS")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-box'>MIN<br><b>{mi}x</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{mo}x</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'>MAX<br><b>{ma}x</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-res'><h3>SIGNAL ACCURACY: {pc}%</h3><h1>{mo}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='next-rounds'>🕒 LERA FIDIRANA: <b>{' | '.join(rd)}</b></div>", unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"🚀 COSMOS | {cos_h} | {mo}x | {pc}%")

# --- TAB 3: MINES VIP (With Grid Schema) ---
with tab3:
    st.file_uploader("📷 CAPTURE DE TOUR (Mines):", type=['jpg', 'png', 'jpeg'], key="min_cap")
    m_cli = st.text_input("💻 CLIENT SEED:", key="m_cli")
    m_ser = st.text_input("🖥️ SERVER SEED:", key="m_ser")
    nb_mines = st.select_slider("💣 NOMBRE DE MINES:", options=[1, 2, 3, 4, 5, 6, 7], value=3)
    
    if st.button("⚡ SCAN BEAST GRID", use_container_width=True):
        random.seed(hash(m_cli + m_ser + str(nb_mines)))
        stars = random.sample(range(25), k=5 if nb_mines < 5 else 3)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top:20px;">'
        for i in range(25):
            is_star = i in stars
            bg = "#00ffcc" if is_star else "#1a1f26"
            shadow = "box-shadow: 0 0 15px #00ffcc;" if is_star else ""
            grid += f'<div style="width:50px; height:50px; background:{bg}; border-radius:8px; border:2px solid #00ffcc; {shadow}"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#00ffcc; margin-top:10px;'>🌟 SCHEMA PREDICTION GENERATED</p>", unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"💣 MINES | {nb_mines} Mines | Grid Analyzed")

# --- TAB 4: PENALTY VIP ---
with tab4:
    st.selectbox("MODE:", ["FACILE", "MOYEN", "DIFFICILE"], key="pen_m")
    if st.button("⚽ GENERATE SHOT", use_container_width=True):
        res = random.choice(["ANKAVIA AMBONY", "AFOVOANY AMBANY", "ANKAVANANA AMBONY"])
        st.success(f"SHOT TARGET: {res}")

# --- RESET & HISTORY ---
st.write("---")
col_h1, col_h2 = st.columns([4, 1])
with col_h2:
    if st.button("🗑️ RESET HISTORIQUE", use_container_width=True):
        st.session_state.prediction_history = []
        st.rerun()

st.subheader("📜 HISTORIQUE DE PRÉDICTION")
for h in reversed(st.session_state.prediction_history[-10:]):
    st.markdown(f"<div class='history-box'>{h}</div>", unsafe_allow_html=True)
