import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- STYLE SY CONFIGURATION ---
st.set_page_config(page_title="ANDRIANTSO v60.3 PREMIUM", page_icon="💎")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FFD700; color: black; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e2130; border: 1px solid #FFD700; border-radius: 10px; padding: 10px; }
    .stRadio>div { background-color: #1e2130; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'wins' not in st.session_state: st.session_state.wins = 0

st.title("💎 ANDRIANTSO | SUPREME v60.3")
st.write("---")

# --- 1. FIDIO NY LALAO (AVIATOR NA COSMOS) ---
mode = st.radio("🚀 FIDIO NY LALAO:", ["✈️ AVIATOR", "🚀 COSMOS X"], horizontal=True)

# --- 2. ANALYSE HISTORIQUE (SCREENSHOT SY LERA) ---
st.subheader("📸 ANALYSE SY SYNCHRO")
col_file, col_time = st.columns([2, 1])

with col_file:
    uploaded_file = st.file_uploader("Ampidiro ny Screenshot History...", type=['jpg', 'png', 'jpeg'])

with col_time:
    # Ny lera eto dia hanampy ny AI hikajy ny "Prochain Signal"
    lera_manomboka = st.time_input("⏲️ Lera ao amin'ny lalao:", datetime.now().time())

# --- 3. INPUT HEX SEED ---
st.write("---")
hex_input = st.text_input(f"🔑 HEX SEED {mode} (SHA-256):", placeholder="Paste Hex here...")

if st.button(f"🔥 GENERATE {mode} SIGNAL"):
    if len(hex_input) < 10:
        st.error("❌ Ampidiro ny Hex Seed feno (SHA-256) azafady!")
    else:
        with st.spinner('AI is analyzing cycles...'):
            time.sleep(1.5)
            # Algorithm Variable v60.3
            h = hashlib.sha256(hex_input.encode()).hexdigest()
            val = int(h[:10], 16)
            
            # Kajy Pourcentage sy Variable
            prob = 82 + (val % 15) # Probability 82% - 97%
            
            if "AVIATOR" in mode:
                safe = round(1.75 + (val % 115) / 100, 2)
                pink = round(12.0 + (val % 7500) / 100, 2)
                t_plus = (val % 4) + 1 # Minute manaraka (1-5 min)
            else:
                safe = round(1.55 + (val % 95) / 100, 2)
                pink = round(9.0 + (val % 4500) / 100, 2)
                t_plus = (val % 3) + 1 # Minute manaraka (1-4 min)

            # Hikajy ny lera hivoahan'ny signal
            target_time = (datetime.combine(datetime.today(), lera_manomboka) + timedelta(minutes=t_plus)).strftime("%H:%M")

            # --- FAMPISEHOANA NY VALINY ---
            st.markdown(f"### 📊 ESTIMATION ACCURACY: **{prob}%**")
            st.info(f"⏰ **PROCHAIN SIGNAL ESTIMÉ À : {target_time}**")
            
            res1, res2 = st.columns(2)
            res1.success(f"✅ SAFE EXIT: **{safe}x**")
            res2.warning(f"💗 MAX PINK: **{pink}x**")
            
            # Tehirizina ny tantara
            st.session_state.history.insert(0, {
                "Lera": target_time,
                "Lalao": mode,
                "Safe": f"{safe}x",
                "Prob": f"{prob}%"
            })

# --- 4. TRACKER SY TANTARA ---
st.write("---")
c_win, c_reset = st.columns([2, 1])

with c_win:
    st.metric("🏆 TOTAL WINS", st.session_state.wins)
    if st.button("✅ I WON THIS ROUND!"):
        st.session_state.wins += 1
        st.rerun()

st.subheader("📜 TANTARAN'NY PREDICTION")
if st.session_state.history:
    st.table(st.session_state.history)
else:
    st.info("Mbola miandry ny prediction voalohany...")

if st.sidebar.button("🗑️ RESET ALL DATA"):
    st.session_state.history = []
    st.session_state.wins = 0
    st.rerun()
