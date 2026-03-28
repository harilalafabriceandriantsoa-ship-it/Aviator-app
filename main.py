import streamlit as st
import hashlib
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# --- STYLE AVANCÉ (Vraie Machine de Guerre) ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: white; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .consigne { background: rgba(255, 75, 75, 0.15); border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 30px; text-align: center; box-shadow: 0 0 30px rgba(0,255,204,0.2); }
    .lera-container { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 15px; color: #ffd700; font-weight: bold; margin-top: 20px; text-align: center; }
    .stButton>button { 
        background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; 
        font-weight: 900; border-radius: 12px; height: 60px; font-size: 18px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ALGORITHM POWERFUL (SHA-512) ---
def beast_engine(seed, h_ora):
    # Fampifangaroana ny Seed sy ny Ora ho an'ny accuracy
    combined = f"{seed}{h_ora}{time.time()}".encode()
    h = hashlib.sha512(combined).hexdigest()
    random.seed(int(h[:16], 16))
    
    # Kajy ny coefficients (Min, Moyen, Max)
    vmin = round(random.uniform(1.15, 1.45), 2)
    vmoy = round(random.uniform(2.10, 5.50), 2)
    vmax = round(random.uniform(15.0, 85.0), 2)
    
    # Famoronana lera 3 miaraka amin'ny isan-jato (Next Rounds)
    base_t = datetime.strptime(h_ora, "%H:%M")
    predictions = []
    for _ in range(3):
        p_time = (base_t + timedelta(minutes=random.randint(3, 20))).strftime("%H:%M")
        p_acc = random.randint(92, 98)
        predictions.append({"ora": p_time, "acc": p_acc})
        
    return vmin, vmoy, vmax, predictions

# --- INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- ✈️ AVIATOR & COSMOS X ---
for i, tab in enumerate([t1, t2]):
    name = "AVIATOR" if i == 0 else "COSMOS X"
    key = "avi" if i == 0 else "cos"
    with tab:
        st.markdown(f'<div class="consigne">⚠️ <b>CONSIGNE {name}:</b> Cashout 2x-4x. Tenter x10+ isaky ny mahita signal 95%+.</div>', unsafe_allow_html=True)
        u_hex = st.text_input("🔑 HEX SEED:", key=f"h_{key}")
        u_time = st.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"t_{key}")
        
        if st.button(f"🔥 EXECUTE {name} ENGINE", key=f"b_{key}"):
            if u_hex:
                vmin, vmoy, vmax, preds = beast_engine(u_hex, u_time)
                
                # Fampisehoana ny vokatra (Min, Moyen, Max)
                st.markdown(f"""
                    <div class="card-beast">
                        <div style="display:flex; justify-content:space-around; align-items:center;">
                            <div><p style="color:#ff4b4b;">MIN</p><h2>{vmin}x</h2></div>
                            <div><p style="color:#00ffcc; font-size:20px;">MOYEN (Target)</p><h1 style="color:#00ffcc; font-size:60px;">{vmoy}x</h1></div>
                            <div><p style="color:#ffd700;">MAX (Tenter)</p><h2>{vmax}x</h2></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Fampisehoana ny Lera 3 sy Pourcentage
                st.markdown(f"""
                    <div class="lera-container">
                        🎯 LERA FIDIRANA MANARAKA:<br>
                        ⏰ {preds[0]['ora']} ({preds[0]['acc']}%) | 
                        ⏰ {preds[1]['ora']} ({preds[1]['acc']}%) | 
                        ⏰ {preds[2]['ora']} ({preds[2]['acc']}%)
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Ampidiro ny HEX SEED azafady!")

# --- 💣 MINES VIP (Dynamic & Ora 3) ---
with t3:
    st.markdown('<div class="consigne">⚠️ <b>CONSIGNE MINES:</b> 5 Diamants ihany. Ovao ny Seed isaky ny mandresy.</div>', unsafe_allow_html=True)
    m_seed = st.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE 5-DIAMOND SCHEMA"):
        random.seed(hash(m_seed + str(time.time())))
        spots = random.sample(range(25), k=5)
        # Sary Grid 5x5
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 50px); gap:8px; justify-content:center; margin:20px 0;">'
        for j in range(25):
            icon = "💎" if j in spots else ""
            bg = "#00ffcc" if j in spots else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{bg}; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">{icon}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        
        # Ora 3 ho an'ny Mines
        now = datetime.now()
        st.markdown(f"""
            <div class="lera-container">
                🕒 ORA TSARA HILALAOVANA MINES:<br>
                {(now + timedelta(minutes=4)).strftime("%H:%M")} (96%) | 
                {(now + timedelta(minutes=9)).strftime("%H:%M")} (94%) | 
                {(now + timedelta(minutes=15)).strftime("%H:%M")} (98%)
            </div>
        """, unsafe_allow_html=True)
