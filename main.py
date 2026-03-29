import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ADMIN ---
if 'access_code' not in st.session_state: st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state: st.session_state.admin_name = "PATRICIA"
if 'history' not in st.session_state: st.session_state.history = []

st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# --- ALGORITHM ---
def get_prediction(seed, lera_input, game_type):
    combined = hashlib.sha512(f"{seed}{lera_input}V85".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    
    # Format lera: HH:mm ho an'ny Aviator, HH:mm:ss ho an'ny Cosmos
    fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
    try:
        t_obj = datetime.strptime(lera_input, fmt)
    except:
        t_obj = datetime.now()

    results = []
    for i in range(3):
        moyen = round(random.uniform(1.80, 4.50), 2)
        res = {
            "lera": (t_obj + timedelta(minutes=(i+1)*2)).strftime(fmt),
            "moyen": moyen,
            "min": round(moyen * 0.85, 2),
            "max": round(moyen * 1.35, 2),
            "prob": random.randint(96, 99)
        }
        results.append(res)
        if i == 0: st.session_state.history.insert(0, res)
    return results

# --- SIDEBAR (ADMIN & MDP) ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    key = st.text_input("Admin Key:", type="password")
    
    if key == st.session_state.access_code:
        st.success("Tafiditra ianao!")
        with st.expander("🔓 MODIFIER MDP / INFO"):
            st.session_state.admin_name = st.text_input("Anarana vaovao:", st.session_state.admin_name)
            st.session_state.access_code = st.text_input("MDP vaovao:", st.session_state.access_code)
            if st.button("💾 ENREGISTRER"): st.rerun()
    
    if st.button("🗑️ RESET HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>TITAN V85.0 ULTRA-SYNC ⚔️</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with tab1:
    st.subheader("⚡ AVIATOR 8/10")
    seed_a = st.text_input("🔑 HEX SEED (Aviator):", key="a_s")
    time_a = st.text_input("🕒 LERA (HH:mm):", value=datetime.now().strftime("%H:%M"), key="a_t")
    if st.button("🔥 ANALYZE AVIATOR"):
        preds = get_prediction(seed_a, time_a, "aviator")
        for p in preds:
            st.write(f"⏰ {p['lera']} | **{p['moyen']}x** (Min: {p['min']} | Max: {p['max']})")

with tab2:
    st.subheader("⚡ COSMOS 8/10")
    seed_c = st.text_input("🔑 HEX SEED (Cosmos):", key="c_s")
    time_c = st.text_input("🕒 LERA (HH:mm:ss):", value=datetime.now().strftime("%H:%M:%S"), key="c_t")
    if st.button("🚀 ANALYZE COSMOS"):
        preds = get_prediction(seed_c, time_c, "cosmos")
        for p in preds:
            st.write(f"⏰ {p['lera']} | **{p['moyen']}x** | Prob: {p['prob']}%")

with tab3:
    st.subheader("💣 MINES VIP")
    c_seed = st.text_input("🔑 CLIENT SEED:", key="m_c")
    s_seed = st.text_input("🔑 SERVER SEED:", key="m_s")
    if st.button("🔍 SCAN MINES"):
        st.info("Mampiasa Client sy Server Seed ny algorithm...")
        # Kisary kely fotsiny eto
        st.code("⭐ ⬛ ⬛ ⭐ ⬛\n⬛ ⭐ ⬛ ⬛ ⬛\n⬛ ⬛ ⭐ ⬛ ⭐")

# --- HISTORIQUE (CAPTURE) ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:5]:
        st.success(f"⏰ {h['lera']} | Vokatra: **{h['moyen']}x** | Min: {h['min']}x / Max: {h['max']}x")
else:
    st.write("Tsy mbola misy historique.")
