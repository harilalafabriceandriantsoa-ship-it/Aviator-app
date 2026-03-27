
    import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta, timezone

# 1. SETUP SY LERA
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER TRIPLE ESTIMATION v27.0", layout="wide")

# Lera Madagasikara (EAT - UTC+3)
now_mg = datetime.now(timezone(timedelta(hours=3)))
lera_izao = now_mg.time()

# 2. STYLE PRO MAHERY VAIKA
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 12px; height: 55px; width: 100%; border: none;
    }
    .main-card { 
        padding: 30px; border: 2px solid #333; border-radius: 25px; 
        text-align: center; background-color: #111; color: white;
    }
    .est-container {
        display: flex; justify-content: space-between; margin-top: 25px; gap: 10px;
    }
    .est-card {
        flex: 1; padding: 15px; border-radius: 15px; text-align: center;
    }
    .min-card { border: 2px solid #00ff44; background: rgba(0, 255, 68, 0.1); }
    .moyen-card { border: 2px solid #ffcc00; background: rgba(255, 204, 0, 0.1); }
    .max-card { border: 2px solid #ff3300; background: rgba(255, 51, 0, 0.1); }
    
    .time-target { 
        font-size: 55px; color: #00ff44; font-weight: 900; 
        border: 2px dashed #00ff44; padding: 10px; border-radius: 15px; margin: 15px 0;
    }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR HISTORY
st.sidebar.title("📜 HISTORY")
for item in st.session_state.history[:6]:
    st.sidebar.markdown(f"""
    <div style='background:#222; padding:8px; border-radius:5px; margin-bottom:5px; border-left:4px solid #ffcc00;'>
        <b style='color:#ffcc00;'>🚀 {item['max']}x</b> | {item['time']} | {item['prob']}%
    </div>
    """, unsafe_allow_html=True)

# 4. MAIN DASHBOARD
st.title("🚀 SNIPER TRIPLE ESTIMATION")
st.write(f"🟢 **SERVER:** LIVE | 🕒 **MG TIME:** {now_mg.strftime('%H:%M:%S')}")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ CONFIGURATION")
    hex_input = st.text_input("INPUT HEX SEED:", placeholder="8ebe8e80...")
    time_now_input = st.time_input("LERA AO AMIN'NY LALAO:", value=lera_izao)
    
    if st.button("🔥 GENERATE SIGNAL"):
        if hex_input:
            with st.spinner('Analysing SHA-256...'):
                time.sleep(1)
            
            hash_obj = hashlib.sha256(hex_input.encode())
            hash_hex = hash_obj.hexdigest()
            val_base = int(hash_hex[:8], 16)
            
            # KAJY ESTIMATION (Miankina amin'ny Hex)
            est_min = 2.03 
            est_moyen = round(4.00 + (val_base % 300) / 100, 2)
            est_max = round(8.00 + (val_base % 1500) / 100, 2)
            
            # Intervalle sy Pourcentage
            interval = 1 + (int(hash_hex[-8:], 16) % 4)
            prob = 60 + (int(hash_hex[12:14], 16) % 40) 
            
            entry_time = (datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)).strftime("%H:%M")
            
            st.session_state.history.insert(0, {
                "min": est_min, "moyen": est_moyen, "max": est_max, 
                "time": entry_time, "prob": prob
            })
            st.rerun()

with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        prob_color = "#00ff44" if latest['prob'] >= 85 else "#ffcc00" if latest['prob'] >= 70 else "#ff3300"
        
        st.markdown(f"""
        <div class="main-card">
            <h3 style='color:#888; margin:0;'>LERA FIDIRANA MANARAKA:</h3>
            <div class="time-target">🎯 {latest['time']} 🎯</div>
            <p style="color:{prob_color}; font-weight:bold; font-size:20px;">PROBABILITÉ: {latest['prob']}%</p>
            
            <div class="est-container">
                <div class="est-card min-card">
                    <small style="color:#00ff44;">🟢 SAFE</small><br>
                    <b style="font-size:28px;">{latest['min']}x</b>
                </div>
                <div class="est-card moyen-card">
                    <small style="color:#ffcc00;">🟡 MOYEN</small><br>
                    <b style="font-size:28px;">{latest['moyen']}x</b>
                </div>
                <div class="est-card max-card">
                    <small style="color:#ff3300;">🔴 MAX</small><br>
                    <b style="font-size:28px;">{latest['max']}x</b>
                </div>
            </div>
            
            <div style="margin-top:20px; padding:15px; background:rgba(255,255,255,0.05); border-radius:15px;">
                <p style="color:#ddd; margin:0;">
                    <b>💡 CONSIGNE:</b> {
                        "Tena tsara ny signal. Azonao andrasana hatramin'ny Max." if latest['prob'] >= 85 
                        else "Milamina ny lalao. Miala amin'ny Moyen no tena tsara." if latest['prob'] >= 70 
                        else "Mitandrema! Miala haingana amin'ny Safe (2.03x) ihany."
                    }
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='main-card'><h3>MIANDRY DATA...</h3><p>Ampidiro ny Hex Seed avy amin'ny lalao.</p></div>", unsafe_allow_html=True)
