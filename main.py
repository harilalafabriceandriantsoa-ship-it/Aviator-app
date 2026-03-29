import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & LOGIN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'access_code' not in st.session_state: st.session_state.access_code = "2026"
if 'history' not in st.session_state: st.session_state.history = []

st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛡️ TITAN V85.0 LOGIN</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Admin Key:", type="password")
    if st.button("HIDITRA"):
        if pwd == st.session_state.access_code:
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("Diso ny kaody!")
    st.stop()

# --- 2. SIDEBAR (MANAGER & MODIF MDP) ---
with st.sidebar:
    st.markdown("### 👤 MANAGER: PATRICIA")
    key_check = st.text_input("Hamarino ny Admin Key hanovana azy:", type="password")
    if key_check == st.session_state.access_code:
        st.success("Azonao ovaina ny MDP")
        new_pwd = st.text_input("MDP vaovao:", type="password")
        if st.button("💾 TEHIRIZINA"):
            st.session_state.access_code = new_pwd
            st.success("Voatahiry!")
    
    st.markdown("---")
    if st.button("🗑️ RESET HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- 3. ALGORITHM 8/10 ---
def get_prediction(seed, lera_input, game_type):
    combined = hashlib.sha256(f"{seed}{lera_input}{game_type}".encode()).hexdigest()
    random.seed(int(combined[:10], 16))
    fmt = "%H:%M"
    try: t_obj = datetime.strptime(lera_input, fmt)
    except: t_obj = datetime.now()

    results = []
    for i in range(1, 4):
        moyen = round(random.uniform(1.80, 4.50), 2)
        p = {
            "tour": i,
            "lera": (t_obj + timedelta(minutes=i*2)).strftime(fmt),
            "moyen": moyen,
            "min": round(moyen * 0.85, 2),
            "max": round(moyen * 1.30, 2),
            "prob": random.randint(97, 99)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 4. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>TITAN V85.0 ULTRA-SYNC ⚔️</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# --- AVIATOR & COSMOS ---
for tab, g_name in zip([tab1, tab2], ["AVIATOR", "COSMOS X"]):
    with tab:
        st.subheader(f"⚡ {g_name} SCANNER")
        # --- CAPTURE DE LA MANCHE (UPLOAD) ---
        st.markdown("📸 **UPLOAD SCREENSHOT (HISTORIQUE)**")
        st.file_uploader("Drag and drop file here", type=['png', 'jpg', 'jpeg'], key=f"file_{g_name}")
        
        col1, col2 = st.columns(2)
        seed = col1.text_input("🔑 SERVER SEED (HEX):", key=f"seed_{g_name}")
        lera = col2.text_input("🕒 LERA (HH:mm):", value=datetime.now().strftime("%H:%M"), key=f"time_{g_name}")
        
        if st.button(f"🔥 EXECUTE {g_name}"):
            if seed:
                preds = get_prediction(seed, lera, g_name.lower())
                cols = st.columns(3)
                for i, p in enumerate(preds):
                    with cols[i]:
                        st.markdown(f"""
                        <div style="background:rgba(0,255,204,0.1); border:1px solid #00ffcc; padding:10px; border-radius:10px; text-align:center;">
                            <b style="color:#ff4444;">TOUR {p['tour']}</b><br>
                            <b>{p['lera']}</b><br>
                            <span style="font-size:30px; color:#00ffcc;">{p['moyen']}x</span><br>
                            <small>Min: {p['min']} | Max: {p['max']}</small>
                        </div>""", unsafe_allow_html=True)

with tab3:
    st.subheader("💣 MINES VIP")
    st.slider("Mines:", 1, 24, 3)
    if st.button("🔍 SCAN"):
        st.code("⭐ ⬛ ⬛ ⭐ ⬛\n⬛ ⭐ ⬛ ⬛ ⬛\n⬛ ⬛ ⭐ ⬛ ⭐")

# --- 5. LAST PREDICTIONS (CAPTURE) ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:6]:
        st.info(f"⏰ {h['lera']} | Vokatra: **{h['moyen']}x** (Min: {h['min']}x / Max: {h['max']}x)")
else:
    st.write("Tsy mbola misy historique.")
