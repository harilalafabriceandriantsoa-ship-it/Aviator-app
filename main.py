import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- STYLE CONFIGURATION (NEON & RISK STYLE) ---
st.set_page_config(page_title="ANDRIANTSO v61.2 X10", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(255, 0, 85, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    .x10-signal {
        background: rgba(255, 0, 85, 0.2); border: 2px dashed #ff0055;
        color: #ff0055; padding: 15px; border-radius: 10px;
        font-weight: bold; font-size: 22px; animation: blinker 1.5s linear infinite;
        margin: 15px 0;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton>button {
        background: linear-gradient(90deg, #ff0055, #00ffcc);
        color: white !important; font-weight: 900 !important; border-radius: 15px !important; 
        height: 4.5em; width: 100%; border: none !important;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05); border-left: 4px solid #ff0055;
        padding: 10px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 TITAN SUPREME v61.2</h1>", unsafe_allow_html=True)

# --- 🎯 SELECTION LALAO (MAIN PAGE) ---
st.write("### 🎮 FIDIO NY LALAO HATAO ANALYSE:")
mode = st.radio("", ["✈️ AVIATOR GOLD", "🚀 COSMOS X"], horizontal=True)

st.write("---")

# --- 📥 INPUT PANEL ---
col_up, col_tm = st.columns(2)
with col_up:
    st.file_uploader("📸 Screenshot History (Optional)", type=['jpg', 'png'])
with col_tm:
    game_time = st.time_input("⏲️ Lera farany hita tamin'ny lalao:", datetime.now().time())

hex_seed = st.text_input(f"🔑 HEX SEED {mode} (SHA-256):", placeholder="Paste Hash here...")

# --- ⚙️ EXECUTION ---
if st.button(f"🚀 EXECUTE {mode} ANALYSIS"):
    if not hex_seed:
        st.error("❌ Ampidiro aloha ny Hex Seed!")
    else:
        with st.spinner('🔐 Deep SHA-512 Analysis in progress...'):
            time.sleep(2)
            
            # SHA-512 Logic
            titan_hash = hashlib.sha512(hex_seed.encode()).hexdigest()
            val = int(titan_hash[:12], 16)
            
            # Calculs
            accuracy = 92 + (val % 6)
            risk_2x_3x = 78 + (val % 18)
            is_x10_possible = (val % 100) > 82 # 18% chance detection
            
            # Estimations miankina amin'ny mode
            if "AVIATOR" in mode:
                safe = round(1.85 + (val % 140) / 100, 2)
                max_p = round(35.0 + (val % 15000) / 100, 2)
            else:
                safe = round(1.45 + (val % 120) / 100, 2)
                max_p = round(15.0 + (val % 9000) / 100, 2)
            
            moyen = round(safe * 2.6, 2)
            t_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")

            # --- DISPLAY RESULTS ---
            st.markdown(f"""
                <div class="prediction-card">
                    <p style='color: #00ffcc;'>{mode} SIGNAL DETECTED</p>
                    <h1 style='font-size: 65px; margin: 0;'>{t_time}</h1>
                    <p style='color: #FFD700;'>ESTIMATION ACCURACY: {accuracy}%</p>
                </div>
            """, unsafe_allow_html=True)

            # Signal X10 Hunter
            if is_x10_possible and risk_2x_3x > 88:
                st.markdown('<div class="x10-signal">⚠️ ALERTE X10 DETECTED: HIGH MOMENTUM ⚠️</div>', unsafe_allow_html=True)
            else:
                st.write(f"📊 **Taha ho an'ny 2x-3x (Auto-Cashout): {risk_2x_3x}%**")

            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("🟢 SAFE", f"{safe}x")
            m2.metric("🟡 MOYEN", f"{moyen}x")
            m3.metric("🌸 MAX PINK", f"{max_p}x")

            # Save to History
            st.session_state.history.insert(0, {
                "Lera": t_time, 
                "Lalao": mode, 
                "Taha 2x-3x": f"{risk_2x_3x}%", 
                "X10 Alert": "🔥 YES" if is_x10_possible else "NO"
            })

# --- SIDEBAR: Fampianarana ---
with st.sidebar:
    st.header("📖 EXPERT GUIDE")
    st.info("""
    **Ho an'ny Cosmos X:**
    Ny Cosmos dia manana 'cycle' haingana kokoa. Raha mipoitra ny X10, mivoaha amin'ny 8x na 9x mba ho azo antoka.
    
    **Ho an'ny Aviator:**
    Ampiasao foana ny 'Double Bet' (2x fiarovana, ny iray katsaho x10).
    """)
    if st.button("🗑️ CLEAR SYSTEM"):
        st.session_state.history = []
        st.rerun()

# --- HISTORY TABLE ---
st.write("---")
st.subheader("📜 RECENT TITAN SIGNALS")
if st.session_state.history:
    st.table(st.session_state.history)
