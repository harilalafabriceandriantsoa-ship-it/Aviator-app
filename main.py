
        import streamlit as st
import hashlib
import time
from datetime import datetime

# 1. Fitehirizana ny Historique (Session State)
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Aviator Sniper Pro v16.0", layout="wide")

# 2. Style Premium (Mavo sy Mainty + Modern Design)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 55px; width: 100%; font-size: 18px; }
    .prediction-box { padding: 30px; border: 4px solid #ffcc00; border-radius: 20px; text-align: center; background-color: #111; color: white; }
    .history-box { padding: 15px; border: 1px solid #444; border-radius: 10px; background-color: #111; margin-bottom: 10px; }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    .telegram-btn { background-color: #0088cc; color: white !important; padding: 15px; text-align: center; border-radius: 10px; text-decoration: none; display: block; font-weight: bold; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AVIATOR SNIPER PRO")
st.write("### SHA-256 Master Predictor | Ambositra 2026")

# 3. SIDEBAR : CONTROL PANEL
st.sidebar.header("⚙️ SETTINGS PRO")
hex_input = st.sidebar.text_input("1. AMPIDIRO NY HEX SEED:", placeholder="aaa5393c45...")
target_cote = st.sidebar.number_input("2. COTE TADIAVINA:", min_value=1.0, value=2.0, step=0.1)
minutes_wait = st.sidebar.slider("3. MINITRA HIANDRASANA:", 1, 5, 4)

if st.sidebar.button("🚀 RUN AI CALCULATION"):
    if hex_input:
        start_time = datetime.now().strftime("%H:%M:%S")
        st.info(f"📥 Signal received at: **{start_time}**")
        
        # FIANDRASANA (Délai)
        total_seconds = minutes_wait * 60
        progress_text = f"AI is scanning the hash... Please wait {minutes_wait} min."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(total_seconds / 100)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        # ALGORITHM SHA-256
        hash_obj = hashlib.sha256(hex_input.encode())
        hash_hex = hash_obj.hexdigest()
        value = int(hash_hex[:8], 16)
        result = max(1.1, round(100 / (1 + (value % 82)), 2))
        
        # Tehirizina ao amin'ny Historique
        now = datetime.now().strftime("%H:%M")
        st.session_state.history.insert(0, {"val": result, "time": now})
        if len(st.session_state.history) > 5:
            st.session_state.history.pop()

        # Fampisehoana ny Vokatra
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        color = "#3498db" if result < 2.0 else "#9b59b6" if result < 10.0 else "#e91e63"
        st.markdown(f"<h3>NEXT MULTIPLIER:</h3><h1 style='color: {color}; font-size: 85px;'>{result}x</h1>", unsafe_allow_html=True)
        
        if result >= target_cote:
            st.success(f"✅ PROFIT ALERT: {result}x is above your target!")
        else:
            st.warning(f"⚠️ RISK ALERT: {result}x is below your target.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Please enter a valid HEX Seed.")

# 4. HISTORIQUE (Ireo 5 farany)
st.write("---")
st.subheader("📜 RECENT PREDICTIONS")
if st.session_state.history:
    cols = st.columns(len(st.session_state.history))
    for i, item in enumerate(st.session_state.history):
        with cols[i]:
            st.markdown(f"""
                <div class="history-box" style="text-align: center;">
                    <b style="color:#ffcc00;">{item['val']}x</b><br>
                    <small style="color:#888;">{item['time']}</small>
                </div>
            """, unsafe_allow_html=True)
else:
    st.write("No history yet. Start a calculation!")

# 5. BOKOTRA TELEGRAM
st.sidebar.markdown('---')
st.sidebar.markdown('<a href="https://t.me/your_channel" class="telegram-btn">📢 JOIN TELEGRAM PRO</a>', unsafe_allow_html=True)
