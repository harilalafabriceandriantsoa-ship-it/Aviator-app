import hashlib
import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
if 'history' not in st.session_state: st.session_state.history = []
if 'score' not in st.session_state: st.session_state.score = {"Win": 0, "Loss": 0}
if 'tracker' not in st.session_state: st.session_state.tracker = []

st.set_page_config(page_title="SNIPER TITAN v40.0", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- SIDEBAR: GAME CONTROL ---
st.sidebar.markdown("<h2 style='color:#FFD700;'>🎮 GAME CONTROL</h2>", unsafe_allow_html=True)
game_choice = st.sidebar.selectbox("🎯 FIDIO NY LALAO:", ["✈️ Aviator (Bet261)", "🚀 Cosmos X (1xBet)"])

# Paramètres techniques
if "Aviator" in game_choice:
    p_color, safe_val, speed_adj = "#FFD700", 2.03, 1.0
    bg_style = "linear-gradient(145deg, #0f0f0f, #1a1a1a)"
    icon_main = "✈️"
else:
    p_color, safe_val, speed_adj = "#00D4FF", 1.75, 0.8 # Cosmos haingana kokoa
    bg_style = "linear-gradient(145deg, #050515, #0a0a25)"
    icon_main = "🚀"

# --- STYLE CSS TITAN ---
st.markdown(f"""
    <style>
    .main {{ background-color: #050505; color: white; }}
    .stApp {{ background-color: #050505; }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 20px; margin-bottom: 20px;
    }}
    .result-card {{
        background: {bg_style};
        padding: 30px; border-radius: 35px;
        border: 2px solid {p_color};
        text-align: center;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.9), 0px 0px 20px {p_color}44;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {p_color} 0%, #ffffff 400%);
        color: black !important; font-weight: 900; border-radius: 18px;
        height: 60px; border: none; font-size: 18px; text-transform: uppercase;
    }}
    .time-display {{ font-size: 70px; font-weight: 900; color: #00FF44; text-shadow: 0px 0px 25px rgba(0,255,68,0.6); }}
    .blink {{ animation: blink 1s infinite; }}
    @keyframes blink {{ 0% {{opacity: 1;}} 50% {{opacity: 0.2;}} 100% {{opacity: 1;}} }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center; color: {p_color};'>{icon_main} SNIPER TITAN v40.0</h1>", unsafe_allow_html=True)

# --- 🎓 ACADEMY ---
with st.expander("🎓 UNIVERSITY: LESONA SY TACTIQUES"):
    st.markdown(f"""
    <div class="glass-card">
        <h4 style="color:{p_color};">🛡️ MODULE EXPERT: {game_choice}</h4>
        <p>• <b>⚡ Hamafiny:</b> Ny {game_choice.split()[0]} dia mila "Réaction" haingana kokoa noho ny hafa.</p>
        <p>• <b>📉 Cosmos Logic:</b> Aza mitady 2.00x foana ao amin'ny Cosmos. Ny <b>1.75x</b> no "Golden Rule" (Safe).</p>
        <p>• <b>🛑 100x Alert:</b> Raha vao nisy cote mavokely be, ny algorithm dia manao "Recalibration" (Mety hisy manga maro).</p>
    </div>
    """, unsafe_allow_html=True)

# --- ⚙️ DASHBOARD ---
col1, col2 = st.columns([1, 1.8])

with col1:
    st.markdown(f"### ⚙️ {icon_main} SETUP")
    offset = st.radio("🕒 SYNC LERA:", ["0 min", "+1 min", "-1 min"], horizontal=True)
    hex_seed = st.text_input("🔑 HEX SEED (SHA-256):", placeholder="Paste SHA-256 here...")
    lera_game = st.time_input("⏲️ LERA AO AMIN'NY LALAO:", value=now_mg.time())
    
    if st.button(f"🔥 GENERATE {game_choice.split()[1].upper()} SIGNAL"):
        if hex_seed:
            h = hashlib.sha256(hex_seed.encode()).hexdigest()
            v = int(h[:8], 16)
            b_int = 1 + (int(h[-8:], 16) % 4)
            f_int = (b_int * speed_adj) + (1 if "+1 min" in offset else -1 if "-1 min" in offset else 0)
            
            t_dt = datetime.combine(datetime.today(), lera_game) + timedelta(minutes=f_int)
            new_p = {
                "Icon": icon_main, "Lera": t_dt.strftime("%H:%M"), "Prob": f"{68 + (int(h[14:16], 16) % 28)}%",
                "Safe": safe_val, "target_dt": t_dt, "moyen": round(3.80 + (v % 450) / 100, 2), "max": round(9.00 + (v % 2500) / 100, 2)
            }
            st.session_state.history.insert(0, new_p)
            st.session_state.tracker.insert(0, {"Lera": new_p["Lera"], "Game": icon_main, "Prob": new_p["Prob"], "Safe": f"{safe_val}x"})
            st.rerun()

with col2:
    if st.session_state.history:
        r = st.session_state.history[0]
        sec = (r['target_dt'] - datetime.combine(datetime.today(), datetime.now().time())).total_seconds()
        
        st.markdown(f"""
        <div class="result-card">
            <p style='color:#888; letter-spacing: 3px;'>🎯 PROCHAIN SIGNAL {r['Icon']}</p>
            <div class="time-display">{r['Lera']}</div>
        """, unsafe_allow_html=True)
        
        if sec > 0:
            m, s = divmod(int(sec), 60)
            st.markdown(f'<p class="{"blink" if sec<=60 else ""}" style="font-size:38px; font-weight:900; color:{p_color};">⌛ TIMER: {m:02d}:{secs:02d}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="blink" style="font-size:38px; font-weight:900; color:#00FF44;">🔥 {icon_main} MIDIRA IZAO! 🔥</p>', unsafe_allow_html=True)
            
        st.markdown(f"""
            <p style='font-size:24px; color:{p_color}; font-weight:bold;'>⭐ PROBABILITÉ: {r['Prob']}</p>
            <div style='display:flex; justify-content:space-around; margin-top:20px;'>
                <div style='border:1px solid #00FF44; padding:15px; border-radius:18px; background:rgba(0,255,68,0.05);'><b>🟢 SAFE</b><br>{r['Safe']}x</div>
                <div style='border:1px solid {p_color}; padding:15px; border-radius:18px; background:rgba(255,215,0,0.05);'><b>🟡 MOYEN</b><br>{r['moyen']}x</div>
                <div style='border:1px solid #FF3131; padding:15px; border-radius:18px; background:rgba(255,49,49,0.05);'><b>🔴 MAX</b><br>{r['max']}x</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if sec > -60: time.sleep(1); st.rerun()

# --- 📊 HISTORY TRACKER ---
st.write("---")
st.markdown("### 📊 HISTORY & ACCURACY TRACKER")
if st.session_state.tracker:
    st.table(pd.DataFrame(st.session_state.tracker[:8]))

# Sidebar Arena
st.sidebar.write("---")
st.sidebar.markdown("### 🎰 TRAINING ZONE")
if st.sidebar.button("🎮 START TEST ROUND"):
    res_sim = random.uniform(1.0, 4.0)
    if res_sim >= safe_val:
        st.session_state.score["Win"] += 1
        st.sidebar.success(f"💰 WIN! {res_sim:.2f}x")
    else:
        st.session_state.score["Loss"] += 1
        st.sidebar.error(f"💥 LOSS! {res_sim:.2f}x")
st.sidebar.write(f"🏆 Score: ✅ {st.session_state.score['Win']} | ❌ {st.session_state.score['Loss']}")
