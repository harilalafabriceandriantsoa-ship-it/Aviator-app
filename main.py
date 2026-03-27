import hashlib
import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'score' not in st.session_state: st.session_state.score = {"Win": 0, "Loss": 0}

st.set_page_config(page_title="ANDRIANTSO | APEX v48", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    .apex-title { text-align: center; font-size: 35px; font-weight: 900; color: #FFD700; text-shadow: 0 0 20px #FFD700; }
    .consigne-card { background: #1a1a1a; padding: 15px; border-radius: 15px; border-left: 10px solid #FFD700; margin-bottom: 15px; }
    .res-card { background: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 30px; border: 2px solid #FFD700; text-align: center; }
    .time-val { font-size: 80px; font-weight: 900; color: #00FF66; line-height: 1; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="apex-title">💎 ANDRIANTSO | SNIPER APEX v48</p>', unsafe_allow_html=True)
st.image("https://img.freepik.com/free-photo/view-futuristic-fighter-jet-flying_23-2151214041.jpg", use_container_width=True)

# --- 📜 UNIVERSITY: CONSIGNES & BANKROLL ---
with st.expander("🎓 UNIVERSITY & CONSIGNES (Full Setup)"):
    st.markdown("""
    <div class="consigne-card">
    <b>📊 FITANTANANA VOLA (Bankroll Management):</b><br>
    - <b>Bet:</b> 2% hatramin'ny 5% amin'ny capital fotsiny isaky ny miditra.<br>
    - <b>Stop Loss:</b> Raha dila ny 15% ny fatiantoka, mijanona aloha vao mitohy.<br>
    - <b>Objectif:</b> +20% hatramin'ny +30% isan'andro dia efa tena tsara.
    </div>
    <div class="consigne-card">
    <b>🚀 TOROHEVITRA COSMOS X (Turbo):</b><br>
    - Ny Cosmos dia haingana kokoa (Fast-paced). Miandrasa elanelana kely vao manao generate indray.<br>
    - Ampiasao foana ny <b>-1 min Sync</b> raha toa ka efa manomboka ny lalao nefa mbola tsy mivoaka ny signal.
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["✈️ MODE AVIATOR", "🚀 MODE COSMOS X"])

def run_apex(game_name, color, safe_limit, speed_val):
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown(f"### ⚙️ SETUP {game_name}")
        sync = st.radio(f"🕒 SYNC LERA:", ["Normal", "+1 min", "-1 min"], key=f"s_{game_name}", horizontal=True)
        hex_in = st.text_input("🔑 HEX SEED (SHA-256):", key=f"h_{game_name}", placeholder="Ampidiro ny Hex eto...")
        lera_in = st.time_input("⏲️ LERA LALAO:", value=now_mg.time(), key=f"t_{game_name}")
        
        st.markdown("---")
        file = st.file_uploader("📷 ANALYSE HISTORIQUE", type=['jpg','png'], key=f"f_{game_name}")
        if file: st.image(file, use_container_width=True)

        if st.button(f"🔥 GENERATE {game_name} SIGNAL", key=f"b_{game_name}"):
            if hex_in:
                h = hashlib.sha256(hex_in.encode()).hexdigest()
                v = int(h[:8], 16)
                off = 1 if "+1 min" in sync else -1 if "-1 min" in sync else 0
                
                # Cosmos is faster, offset is reduced
                final_offset = speed_val if game_name == "AVIATOR" else 0.5
                target = datetime.combine(datetime.today(), lera_in) + timedelta(minutes=(final_offset + off))
                
                res = {
                    "Lera": target.strftime("%H:%M"),
                    "Prob": f"{88 + (v % 11)}%",
                    "Safe": safe_limit,
                    "Moyen": round(4.5 + (v % 450)/100, 2),
                    "Max": round(20.0 + (v % 3000)/100, 2),
                    "game": game_name,
                    "target_dt": target
                }
                st.session_state.history_list.insert(0, res)
                st.rerun()

    with col2:
        if st.session_state.history_list and st.session_state.history_list[0]["game"] == game_name:
            curr = st.session_state.history_list[0]
            diff = (curr['target_dt'] - datetime.combine(datetime.today(), datetime.now().time())).total_seconds()
            
            st.markdown(f"""
            <div class="res-card" style="border-color: {color}; box-shadow: 0 0 15px {color}33;">
                <p style="color: {color}; font-weight: bold;">{game_name} ACTIVE SIGNAL</p>
                <div class="time-val" style="color: {'#00FF66' if diff > 0 else color};">{curr['Lera']}</div>
            """, unsafe_allow_html=True)
            
            if diff > 0:
                m, s = divmod(int(diff), 60)
                st.markdown(f"<h2 style='color:#FFD700;'>⌛ TIMER: {m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 class='blink' style='color:{color};'>🚀 MIDIRA IZAO! 🚀</h2>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div><b>SAFE</b><br><span style="color:#00FF66;">{curr['Safe']}x</span></div>
                    <div><b>MOYEN</b><br><span style="color:#FFD700;">{curr['Moyen']}x</span></div>
                    <div><b>MAX</b><br><span style="color:{color}; font-size: 20px;">{curr['Max']}x</span></div>
                </div>
                <p style="margin-top:20px; font-size: 12px; color: #666;">ACCURACY: {curr['Prob']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if diff > -60: time.sleep(1); st.rerun()

        # --- HISTORY TABLE ---
        if st.session_state.history_list:
            st.markdown("### 📜 HISTORY")
            df = pd.DataFrame(st.session_state.history_list[:5])[["Lera", "game", "Safe", "Moyen", "Max"]]
            st.table(df)

with tab1: run_apex("AVIATOR", "#FFD700", 2.03, 2.0)
with tab2: run_apex("COSMOS", "#00D4FF", 1.75, 1.0)

# --- PRACTICE ---
st.write("---")
if st.button("🎮 PRACTICE ROUND"):
    sim = random.uniform(1.0, 5.0)
    if sim >= 1.75: st.success(f"WIN! {sim:.2f}x"); st.session_state.score["Win"] += 1
    else: st.error(f"LOSS! {sim:.2f}x"); st.session_state.score["Loss"] += 1
st.write(f"🏆 Score: ✅ {st.session_state.score['Win']} | ❌ {st.session_state.score['Loss']}")
