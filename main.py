import streamlit as st
import hashlib
import time
from datetime import datetime

# Configuration ny pejy
st.set_page_config(page_title="Aviator Sniper Pro v15.0", layout="wide")

# Style Premium (Mavo sy Mainty)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 55px; width: 100%; font-size: 20px; }
    .prediction-box { padding: 30px; border: 4px solid #ffcc00; border-radius: 20px; text-align: center; background-color: #111; color: white; margin-top: 20px; }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    .stNumberInput>div>div>input { background-color: #222; color: #ffcc00; border: 1px solid #ffcc00; }
    .stTextInput>div>div>input { background-color: #222; color: #ffcc00; border: 1px solid #ffcc00; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AVIATOR SNIPER PRO")
st.write("---")

# SIDEBAR : CONTROL PANEL
st.sidebar.header("⚙️ SETTINGS PRO")

# 1. Fampidirana HEX
hex_input = st.sidebar.text_input("1. AMPIDIRO NY HEX SEED:", placeholder="aaa5393c45...")

# 2. Fampidirana COTE
target_cote = st.sidebar.number_input("2. COTE TADIAVINA (OBJECTIF):", min_value=1.0, value=2.0, step=0.1)

# 3. Fampidirana LERA (Délai) - Nataoko raikitra 4 minitra ny max
minutes_wait = st.sidebar.slider("3. MINITRA HIANDRASANA:", 1, 5, 4)

if st.sidebar.button("MAMPIASA NY AI (CALCULER)"):
    if hex_input:
        # Lera nanindriana ny bokotra
        start_time = datetime.now().strftime("%H:%M:%S")
        st.info(f"📥 Signal nampidirina tamin'ny: **{start_time}**")
        
        # FIANDRASANA (3 hatramin'ny 4 minitra)
        total_seconds = minutes_wait * 60
        progress_text = f"Manao calcul scientifique... Miandrasa {minutes_wait} minitra."
        my_bar = st.progress(0, text=progress_text)
        
        # Mampiseho ny fandehan'ny fotoana
        for percent_complete in range(100):
            time.sleep(total_seconds / 100)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        # ALGORITHM SHA-256 (Ilay tena mahery vaika)
        hash_obj = hashlib.sha256(hex_input.encode())
        hash_hex = hash_obj.hexdigest()
        value = int(hash_hex[:8], 16)
        
        # Formula matematika hamoaka multiplier
        result = max(1.1, round(100 / (1 + (value % 85)), 2))
        
        # Fampisehoana ny Vokatra
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        
        if result < 2.0:
            color = "#3498db" # Blue
            status = "❌ SIGNAL BLUE (TSY TSARA)"
        elif result < 10.0:
            color = "#9b59b6" # Purple
            status = "🎯 SIGNAL PURPLE (TSARA)"
        else:
            color = "#e91e63" # Pink
            status = "🔥 SIGNAL PINK (TENA TSARA)"
            
        st.markdown(f"<h3>VINAVINA MANARAKA:</h3><h1 style='color: {color}; font-size: 80px;'>{result}x</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: {color};'>{status}</h2>", unsafe_allow_html=True)
        
        # Fanaraha-maso ny Cote
        if result >= target_cote:
            st.success(f"✅ Mihoatra ny {target_cote}x tadiaviao io!")
        else:
            st.warning(f"⚠️ Ambany noho ny {target_cote}x tadiaviao io.")
            
        st.write(f"Lera nivoahan'ny valiny: **{datetime.now().strftime('%H:%M:%S')}**")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Azafady, ampidiro ny HEX Seed!")
