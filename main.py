import streamlit as st
import hashlib
from datetime import datetime

# Configuration haingana
st.set_page_config(page_title="Aviator Sniper Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 50px; }
    .prediction-box { padding: 30px; border: 4px solid #ffcc00; border-radius: 20px; text-align: center; background-color: #111; }
    h1 { color: #ffcc00 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AVIATOR SNIPER PRO")

# SIDEBAR
st.sidebar.header("⚙️ SETTINGS")
hex_seed = st.sidebar.text_input("Ampidiro ny HEX Seed:")

# BOKOTRA EO NO HO EO
if st.sidebar.button("MIKajy AVY HATRANY (0s)"):
    if hex_seed:
        # TSY MISY TIME.SLEEP INTSONY ETO - EO NO HO EO NY VALINY
        
        # Algorithm SHA-256
        hash_obj = hashlib.sha256(hex_seed.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Kajy matematika
        value = int(hash_hex[:8], 16)
        result = max(1.1, round(100 / (1 + (value % 80)), 2))
        
        # Fampisehoana
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        
        if result < 2.0:
            color = "#3498db" # Blue
            status = "❌ SIGNAL BLUE"
        elif result < 10.0:
            color = "#9b59b6" # Purple
            status = "🎯 SIGNAL PURPLE"
        else:
            color = "#e91e63" # Pink
            status = "🔥 SIGNAL PINK"
            
        st.markdown(f"<h3>VINAVINA:</h3><h1 style='color: {color}; font-size: 80px;'>{result}x</h1>", unsafe_allow_html=True)
        st.write(f"## {status}")
        st.write(f"Lera: {datetime.now().strftime('%H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Ampidiro ny HEX!")
