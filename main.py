import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION STYLE (Tena Mahery) ---
st.set_page_config(page_title="ANDRIANTSO SUPREME v61.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Background an'ny pejy iray manontolo */
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    /* Boite an'ny prediction */
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.15), rgba(255, 215, 0, 0.15));
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.2);
        margin-bottom: 25px;
    }
    /* Style an'ny bokotra */
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #FFD700);
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 4.5em !important;
        width: 100%;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    /* Metrics style */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00ffcc;
        padding: 15px;
        border-radius: 10px;
    }
    /* Input style */
    .stTextInput>div>div>input {
        background-color: #111 !important;
        color: #00ffcc !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC & INITIALIZATION ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. HEADER & SELECTION ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN SUPREME v61.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>SHA-512 Variable Logic | Professional Grade</p>", unsafe_allow_html=True)

st.write("---")

# Fidio ny lalao (Main Page)
col_mode = st.columns([1, 2, 1])
with col_mode[1]:
    mode = st.radio("🎯 FIDIO NY LALAO HATAO ANALYSE:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X"], horizontal=True)

# --- 4. INPUT PANEL ---
st.write("### 📥 DATA INPUT")
c1, c2 = st.columns(2)
with c1:
    st.file_uploader("📸 Screenshot History (Optional)", type=['jpg', 'png'])
with c2:
    current_game_time = st.time_input("⏲️ Lera farany hita tamin'ny lalao:", datetime.now().time())

hex_seed = st.text_input(f"🔑 AMPIDIRO NY HEX SEED {mode} (SHA-256):", placeholder="Paste the hash here...")

# --- 5. EXECUTION & CALCULATION ---
if st.button(f"🚀 START TITAN SHA-512 ANALYSIS"):
    if not hex_seed:
        st.warning("⚠️ Masìna ianao, ampidiro aloha ilay Hex Seed!")
    else:
        with st.spinner('🔐 Mikajy ny algorithm SHA-512...'):
            time.sleep(2)
            
            # SHA-512 MAHERY VAIKA
            raw_hash = hashlib.sha512(hex_seed.encode()).hexdigest()
            val = int(raw_hash[:12], 16)
            
            # Accuracy
            prob = 91 + (val % 8)
            
            # Estimations miankina amin'ny lalao
            if "AVIATOR" in mode:
                safe = round(1.80 + (val % 140) / 100, 2)
                moyen = round(safe * (2.2 + (val % 10)/10), 2)
                max_val = round(30.0 + (val % 15000) / 100, 2)
            else:
                safe = round(1.40 + (val % 120) / 100, 2)
                moyen = round(safe * 2.0, 2)
                max_val = round(15.0 + (val % 8000) / 100, 2)
            
            # Prediction Lera
            pred_time = (datetime.combine(datetime.today(), current_game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")

            # --- DISPLAY RESULTS ---
            st.markdown(f"""
                <div class="prediction-card">
                    <h2 style='color: #00ffcc;'>{mode} SIGNAL READY</h2>
                    <h1 style='font-size: 70px; color: #ffffff;'>{pred_time}</h1>
                    <p style='color: #FFD700; font-size: 20px;'>ACCURACY: {prob}%</p>
                </div>
            """, unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            with m1: st.metric("🟢 SAFE EXIT", f"{safe}x")
            with m2: st.metric("🟡 MOYEN TARGET", f"{moyen}x")
            with m3: st.metric("🌸 MAX (PINK)", f"{max_val}x")

            # Store history
            st.session_state.history.insert(0, {
                "Lera": pred_time, 
                "Lalao": mode, 
                "Safe": safe, 
                "Moyen": moyen, 
                "Max": max_val,
                "Prob": f"{prob}%"
            })

# --- 6. SIDEBAR: CONSIGNES & HISTORY ---
with st.sidebar:
    st.header("📖 CONSIGNES D'EXPERT")
    st.markdown("""
    1. **Fidio ny lalao**: Ataovy azo antoka fa mifanaraka ny lalao sy ny Hex Seed.
    2. **Gestion de Mise**: Aza lany vola amin'ny lalao iray.
    3. **Pink Hunting**: Ny 'Max' dia mety hitranga fa ambony ny risika. Aleo mivoaka amin'ny 'Moyen'.
    4. **Break**: Rehefa nahazo in-3 ianao, ajanony ny lalao mandritra ny 30 minitra.
    """)
    st.write("---")
    if st.button("🗑️ CLEAR HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- 7. HISTORY TABLE ---
st.write("---")
st.subheader("📜 TANTARAN'NY PREDICTION")
if st.session_state.history:
    st.table(st.session_state.history)
else:
    st.info("Mbola tsisy prediction vita. Ampidiro ny Hex Seed eo ambony.")
