import streamlit as st
import hashlib
import time
import base64
from datetime import datetime, timedelta, timezone

# 1. SETUP SY LERA MADAGASIKARA
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER ULTRA v21.0", layout="wide")

# Mikajy ny lera eto Madagasikara (UTC+3)
now_mg = datetime.now(timezone(timedelta(hours=3)))
lera_izao = now_mg.time()

# 2. SOUND ENGINE (Bip-Bip)
def play_sound():
    # Feo "Bip" fohy ho an'ny signal
    audio_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# 3. STYLE MAHERY VAIKA
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 15px; 
        height: 65px; width: 100%; font-size: 22px; border: none;
        box-shadow: 0px 0px 20px #ffcc00;
    }
    .prediction-box { 
        padding: 30px; border: 5px double #ffcc00; border-radius: 25px; 
        text-align: center; background-color: #111; color: white;
    }
    .time-target { 
        font-size: 45px; color: #00ff44; font-weight: 900; 
        border: 3px solid #00ff44; padding: 20px; margin: 15px 0; 
        border-radius: 20px; background-color: #001a00;
        text-shadow: 0px 0px 15px #00ff44;
    }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SNIPER ULTRA v21.0")
st.write(f"### SERVER TIME: {now_mg.strftime('%H:%M:%S')} (EAT)")

# 4. SIDEBAR CONFIGURATION
st.sidebar.header("🛠️ CONFIGURATION")
hex_input = st.sidebar.text_input("INPUT HEX SEED:", placeholder="8ebe8e80...")

# Eto no namboarina mba ho lera Madagasikara avy hatrany
time_now_input = st.sidebar.time_input("LERA AO AMIN'NY LALAO:", value=lera_izao)

if st.sidebar.button("🔥 GENERATE SIGNAL NOW"):
    if hex_input:
        with st.spinner('⚡ CALCULATING...'):
            time.sleep(1)
        
        # SHA-256 ALGORITHM
        hash_obj = hashlib.sha256(hex_input.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Multiplier
        val_m = int(hash_hex[:8], 16)
        result = max(1.1, round(100 / (1 + (val_m % 78)), 2))
        
        # Intervalle (1-4 minitra)
        val_t = int(hash_hex[-8:], 16)
        interval = 1 + (val_t % 4)
        
        # Lera fidirana
        entry_dt = datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)
        entry_time = entry_dt.strftime("%H:%M")
        
        # FEONY
        play_sound()
        
        # Tehirizina
        st.session_state.history.insert(0, {"val": result, "time": entry_time, "int": interval})

        # DISPLAY
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        st.markdown(f"<h3>LERA FIDIRANA (STRIKE):</h3>", unsafe_allow_html=True)
        st.markdown(f'<div class="time-target">🎯 {entry_time} 🎯</div>', unsafe_allow_html=True)
        
        color = "#00d4ff" if result < 2.0 else "#ffcc00" if result < 10.0 else "#ff0055"
        st.markdown(f"<h3>EXPECTED:</h3><h1 style='color: {color}; font-size: 95px;'>{result}x</h1>", unsafe_allow_html=True)
        st.success(f"Signal generated at {now_mg.strftime('%H:%M')} | Gap: {interval}m")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Ampidiro ny HEX Seed!")

# 5. HISTORIQUE
st.write("---")
st.subheader("📜 PREVIOUS STRIKES")
if st.session_state.history:
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.history[:5]):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align:center; border:2px solid #333; padding:10px; border-radius:15px; background-color:#111;">
                    <b style="color:#ffcc00;">{item['val']}x</b><br>
                    <span style="color:#00ff44;">{item['time']}</span>
                </div>
            """, unsafe_allow_html=True)
