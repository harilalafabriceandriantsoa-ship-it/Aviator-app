import hashlib
import time
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
if 'history' not in st.session_state: st.session_state.history = []

st.set_page_config(page_title="ANDRIANTSO | APEX v50", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE DESIGN UNIFORME ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FFFFFF; }
    .stApp { background-color: #000000; }
    
    .apex-title {
        text-align: center; font-size: 40px; font-weight: 900;
        color: #FFD700; text-shadow: 0 0 20px #FFD700;
    }
    
    .res-card {
        background: #0a0a0a; padding: 30px; border-radius: 35px;
        border: 3px solid; text-align: center;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    }
    
    .time-display { font-size: 85px; font-weight: 900; line-height: 1; margin: 15px 0; }
    
    /* Style ho an'ny tabs */
    .stTabs [data-baseweb="tab-list"] { display: flex; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px; font-weight: 900; width: 200px; height: 50px;
        border-radius: 10px 10px 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="apex-title">💎 ANDRIANTSO | APEX v50</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>UNIVERSAL DUAL-ENGINE SYSTEM</p>", unsafe_allow_html=True)

# --- 📜 UNIVERSITY & CONSIGNES (Mitambatra) ---
with st.expander("🎓 UNIVERSITY & CONSIGNES (Samy mitovy)"):
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
        **📍 BANKROLL MANAGEMENT:**
        - Mise: 2% hatramin'ny 5% ny capital.
        - Objectif: +20% isan'andro dia mijanona.
        """)
    with col_c2:
        st.markdown("""
        **📍 FOMBA FAMPIASANA:**
        - Adika ny **Hex Seed** avy ao amin'ny lalao.
        - Apetaka eo amin'ny vata, dia tsindrio ny **Generate**.
        - Araho ny **Timer** mandra-pahatongan'ny 00:00.
        """)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["✈️ AVIATOR MODE", "🚀 COSMOS MODE"])

def build_engine(name, color, safe, offset):
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown(f"### ⚙️ {name} INPUT")
        # Donnée tokana (Hex Seed)
        hex_val = st.text_input(f"🔑 {name} HEX SEED:", placeholder="Paste Hex Code here...", key=f"hex_{name}")
        
        # Ny AI no mikajy ny lera automatique
        st.write(f"⏰ Lera Finday: **{now_mg.strftime('%H:%M:%S')}**")

        if st.button(f"🔥 GENERATE {name} SIGNAL", key=f"btn_{name}"):
            if hex_val:
                h = hashlib.sha256(hex_val.encode()).hexdigest()
                v = int(h[:8], 16)
                
                # Sync automatique arakaraka ny lalao
                target = now_mg + timedelta(minutes=offset)
                
                st.session_state.history.insert(0, {
                    "Lera": target.strftime("%H:%M"),
                    "Prob": f"{90 + (v % 9)}%",
                    "Safe": safe,
                    "Moyen": round(4.2 + (v % 380)/100, 2),
                    "Max": round(20.0 + (v % 4000)/100, 2),
                    "Game": name,
                    "target_dt": target
                })
                st.rerun()
            else:
                st.error("Ampidiro aloha ny Hex Seed!")

    with c2:
        if st.session_state.history and st.session_state.history[0]["Game"] == name:
            res = st.session_state.history[0]
            diff = (res['target_dt'] - now_mg).total_seconds()
            
            st.markdown(f"""
            <div class="res-card" style="border-color: {color};">
                <p style="color: {color}; font-weight: bold; letter-spacing: 3px;">{name} PREDICTION</p>
                <div class="time-display" style="color: {'#00FF66' if diff > 0 else color};">{res['Lera']}</div>
            """, unsafe_allow_html=True)
            
            if diff > 0:
                m, s = divmod(int(diff), 60)
                st.markdown(f"<h2 style='color:#FFD700;'>⌛ TIMER: {m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 class='blink' style='color:{color};'>🔥 MIDIRA IZAO! 🔥</h2>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin-top: 20px; border-top: 1px solid #333; padding-top: 15px;">
                    <div><b>SAFE</b><br><span style="color:#00FF66; font-size:20px;">{res['Safe']}x</span></div>
                    <div><b>MOYEN</b><br><span style="color:#FFD700; font-size:20px;">{res['Moyen']}x</span></div>
                    <div><b>MAX (PINK)</b><br><span style="color:{color}; font-size:22px; font-weight:900;">{res['Max']}x</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if diff > -60: time.sleep(1); st.rerun()
        else:
            st.info(f"Andrasana ny Hex Seed ho an'ny {name}...")

# --- EXECUTION ---
with tab1:
    build_engine("AVIATOR", "#FFD700", 2.03, 1.5)

with tab2:
    build_engine("COSMOS", "#00D4FF", 1.75, 1.0)

# --- HISTORY ---
if st.session_state.history:
    st.write("---")
    st.markdown("### 📜 HISTORY (Last 3)")
    st.table(pd.DataFrame(st.session_state.history[:3])[["Lera", "Game", "Safe", "Max"]])

# --- RESET ---
if st.button("🗑️ RESET ALL"):
    st.session_state.history = []
    st.rerun()
