import hashlib
import time
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
if 'history' not in st.session_state: st.session_state.history = []
if 'stats' not in st.session_state: st.session_state.stats = {"Win": 0, "Loss": 0}

st.set_page_config(page_title="ANDRIANTSO | SUPREME v60", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE PREMIUM STYLE ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FFFFFF; }
    .stApp { background-color: #000000; }
    
    .title-premium {
        text-align: center; font-size: 45px; font-weight: 900;
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
    }
    
    .card-signal {
        background: rgba(15, 15, 15, 0.95); padding: 30px; border-radius: 30px;
        border: 2px solid; text-align: center; margin-bottom: 20px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.5);
    }
    
    .big-timer { font-size: 110px; font-weight: 900; line-height: 1; margin: 10px 0; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #111; border-radius: 20px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 16px; width: 100%; }
    
    .tracker-box {
        background: #111; padding: 15px; border-radius: 15px;
        display: flex; justify-content: space-around; align-items: center;
        border-bottom: 3px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & TRACKER ---
st.markdown('<p class="title-premium">💎 SUPREME TITAN v60.0</p>', unsafe_allow_html=True)

col_t1, col_t2 = st.columns([2, 1])
with col_t1:
    st.markdown(f"""
    <div class="tracker-box">
        <span>🏆 <b>ACCURACY TRACKER</b></span>
        <span style="color:#00FF66;">✅ GAGNÉ: {st.session_state.stats['Win']}</span>
        <span style="color:#FF4B4B;">❌ PERDU: {st.session_state.stats['Loss']}</span>
    </div>
    """, unsafe_allow_html=True)
with col_t2:
    if st.button("🔄 RESET STATS"):
        st.session_state.stats = {"Win": 0, "Loss": 0}
        st.rerun()

# --- MODES ---
tab_avi, tab_cos = st.tabs(["✈️ MODE AVIATOR (GOLD)", "🚀 MODE COSMOS X (NEON)"])

def engine_premium(name, color, safe, speed):
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        st.markdown(f"### 🛠️ {name} SETTINGS")
        
        # 1. Sync
        sync = st.select_slider("🕒 SYNC LERA:", options=["-1m", "Normal", "+1m"], value="Normal", key=f"s_{name}")
        
        # 2. Hex Seed
        hex_in = st.text_input("🔑 HEX SEED (SHA-256):", placeholder="Paste Hex here...", key=f"h_{name}")
        
        # 3. Lera Lalao (Naverina)
        lera_lalao = st.time_input("⏲️ LERA AO AMIN'NY LALAO:", value=now_mg.time(), key=f"t_{name}")
        
        # 4. Sary Analyse (Naverina)
        st.file_uploader("📷 ANALYSE HISTORIQUE (Screenshot)", type=['jpg','png','jpeg'], key=f"f_{name}")

        if st.button(f"🔥 GENERATE {name} SIGNAL", key=f"b_{name}"):
            if hex_in:
                h = hashlib.sha256(hex_in.encode()).hexdigest()
                v = int(h[:10], 16)
                
                # Calculation avec Lera sy Sync
                off = 1 if "+1m" in sync else -1 if "-1m" in sync else 0
                target = datetime.combine(datetime.today(), lera_lalao) + timedelta(minutes=(speed + off))
                
                st.session_state.history.insert(0, {
                    "Lera": target.strftime("%H:%M"),
                    "Game": name,
                    "Safe": safe,
                    "Moyen": round(4.5 + (v % 500)/100, 2),
                    "Max": round(25.0 + (v % 8000)/100, 2),
                    "target_dt": target,
                    "color": color
                })
                st.rerun()

    with c2:
        if st.session_state.history and st.session_state.history[0]["Game"] == name:
            res = st.session_state.history[0]
            diff = (res['target_dt'] - datetime.combine(datetime.today(), datetime.now().time())).total_seconds()
            
            st.markdown(f"""
            <div class="card-signal" style="border-color: {color};">
                <p style="color: {color}; font-weight: bold; letter-spacing: 5px;">{name} SIGNAL ACTIVE</p>
                <div class="big-timer" style="color: {'#00FF66' if diff > 0 else color};">{res['Lera']}</div>
            """, unsafe_allow_html=True)
            
            if diff > 0:
                m, s = divmod(int(diff), 60)
                st.markdown(f"<h2 style='color:#FFD700;'>⌛ TIMER: {m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h1 class='blink' style='color:{color};'>🚀 MIDIRA IZAO!</h1>", unsafe_allow_html=True)
                # Bokotra Validation (Gagné / Perdu)
                col_w, col_l = st.columns(2)
                if col_w.button("✅ GAGNÉ", key=f"win_{time.time()}"):
                    st.session_state.stats["Win"] += 1
                    st.rerun()
                if col_l.button("❌ PERDU", key=f"loss_{time.time()}"):
                    st.session_state.stats["Loss"] += 1
                    st.rerun()
            
            st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px;">
                    <div><b style="color:#888;">SAFE</b><br><span style="color:#00FF66; font-size:22px;">{res['Safe']}x</span></div>
                    <div><b style="color:#888;">MOYEN</b><br><span style="color:#FFD700; font-size:22px;">{res['Moyen']}x</span></div>
                    <div><b style="color:#888;">MAX</b><br><span style="color:{color}; font-size:28px; font-weight:900;">{res['Max']}x</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if diff > -60: time.sleep(1); st.rerun()
        else:
            st.info(f"Vakio ny screenshot dia ampidiro ny Hex Seed ho an'ny {name}...")

with tab_avi: engine_premium("AVIATOR", "#FFD700", 2.03, 2)
with tab_cos: engine_premium("COSMOS", "#00D4FF", 1.75, 1)

# --- HISTORY ---
if st.session_state.history:
    st.write("---")
    st.markdown("### 📜 PREVIOUS SIGNALS")
    st.table(pd.DataFrame(st.session_state.history[:5])[["Lera", "Game", "Safe", "Max"]])
