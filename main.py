import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta, timezone

if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER LIVE v35.0", layout="wide")

# Lera Madagasikara
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE CSS (NEON & ANIMATION) ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FF8C00 100%);
        color: black !important; font-weight: 900; border-radius: 15px; height: 55px; border: none;
    }
    
    .result-card {
        background: #111; padding: 30px; border-radius: 25px; border: 2px solid #333; text-align: center;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.1);
    }
    
    .countdown-text {
        font-size: 40px; font-weight: 900; color: #FFD700;
        background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 15px;
    }

    /* Animation mitselatra rehefa akaiky ny lera */
    @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }
    .blink { animation: blink 1s infinite; color: #FF3131 !important; }

    .time-display { font-size: 60px; font-weight: 900; color: #00FF44; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🛡️ SNIPER LIVE COUNTDOWN</h1>", unsafe_allow_html=True)

# --- 📚 ACADEMY SECTION ---
with st.expander("📖 ACADEMY: LESONA SY CONSIGNE"):
    st.markdown("""
    <div style="background:#1a1a1a; padding:20px; border-radius:15px; border-left:5px solid #FFD700;">
        <h4 style="color:#FFD700;">1. LIVE COUNTDOWN</h4>
        <p>Jereo ny "TIMER" eo ambanin'ny lera. Raha lasa <b>mena sy mitselatra</b> izy, dia midika izany fa latsaky ny 1 minitra sisa dia manomboka ny round.</p>
        <h4 style="color:#FFD700;">2. SYNC OFFSET</h4>
        <p>Raha taraiky 1 minitra ny lalao, ampiasao ny <b>+1 min</b> mba hifandrindra amin'ny Countdown.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns([1, 1.8])

with col1:
    st.markdown("### ⚙️ SETUP & SYNC")
    offset = st.radio("SYNC LERA:", ["0 min", "+1 min", "-1 min"], horizontal=True)
    uploaded_file = st.file_uploader("📷 UPLOAD HISTORIQUE", type=['jpg','png','jpeg'])
    hex_seed = st.text_input("🔑 HEX SEED:", placeholder="Paste SHA-256 here...")
    lera_game = st.time_input("🕒 LERA AO AMIN'NY LALAO:", value=now_mg.time())
    
    if st.button("🚀 GENERATE SIGNAL"):
        if hex_seed:
            hash_obj = hashlib.sha256(hex_seed.encode())
            hash_hex = hash_obj.hexdigest()
            val_base = int(hash_hex[:8], 16)
            
            # KAJY INTERVALLE & SYNC
            base_int = 1 + (int(hash_hex[-8:], 16) % 4)
            final_int = base_int + (1 if "+1 min" in offset else -1 if "-1 min" in offset else 0)
            
            # ESTIMATION & PROB
            est_min, est_moyen = 2.03, round(4.00 + (val_base % 350) / 100, 2)
            est_max = round(8.00 + (val_base % 1800) / 100, 2)
            prob = 60 + (int(hash_hex[12:14], 16) % 35)
            
            target_dt = datetime.combine(datetime.today(), lera_game) + timedelta(minutes=final_int)
            
            st.session_state.history.insert(0, {
                "min": est_min, "moyen": est_moyen, "max": est_max, 
                "time_str": target_dt.strftime("%H:%M"), "target_dt": target_dt, "prob": prob
            })
            st.rerun()

with col2:
    if st.session_state.history:
        res = st.session_state.history[0]
        
        # --- KAJY NY LIVE COUNTDOWN ---
        now = datetime.now() # Lera finday izao
        diff = res['target_dt'] - datetime.combine(datetime.today(), now.time())
        seconds_left = diff.total_seconds()
        
        st.markdown(f"""
        <div class="result-card">
            <p style="color: #888;">LERA FIDIRANA</p>
            <div class="time-display">{res['time_str']}</div>
        """, unsafe_allow_html=True)
        
        # Fisehon'ny Countdown
        if seconds_left > 0:
            mins, secs = divmod(int(seconds_left), 60)
            blink_class = "blink" if seconds_left <= 60 else ""
            st.markdown(f'<p class="countdown-text {blink_class}">⌛ TIMER: {mins:02d}:{secs:02d}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="countdown-text blink" style="color:#00FF44 !important;">🔥 MIDIRA IZAO! 🔥</p>', unsafe_allow_html=True)
            
        st.markdown(f"""
            <p style="color: #FFD700; font-weight: bold;">PROBABILITÉ: {res['prob']}%</p>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <div style="border:1px solid #00FF44; padding:10px; border-radius:10px;"><b>SAFE</b><br>{res['min']}x</div>
                <div style="border:1px solid #FFD700; padding:10px; border-radius:10px;"><b>MOYEN</b><br>{res['moyen']}x</div>
                <div style="border:1px solid #FF3131; padding:10px; border-radius:10px;"><b>MAX</b><br>{res['max']}x</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mamelombelona ny Countdown isaky ny segondra
        if seconds_left > -60: # Ajanona ny refresh rehefa dila 1 minitra
            time.sleep(1)
            st.rerun()

        if uploaded_file:
            st.image(uploaded_file, caption="Historique de la Manche", use_container_width=True)
