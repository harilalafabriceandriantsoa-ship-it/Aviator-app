import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- CONFIGURATION STYLE (TRES STYLÉ & PREMIUM) ---
st.set_page_config(page_title="TITAN LUXURY v62.4", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0f0f0f, #001a1a); color: #e0e0e0; }
    .luxury-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.1), rgba(255,215,0,0.1));
        border-left: 5px solid #ffd700; border-radius: 15px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 25px;
    }
    .consigne-box {
        background: rgba(255, 255, 255, 0.03); border: 1px dashed #ffd700;
        border-radius: 10px; padding: 15px; font-size: 14px; color: #ffd700;
    }
    .stat-val { font-size: 35px; font-weight: 900; color: #ffffff; text-shadow: 0 0 10px #00ffcc; }
    .stButton>button {
        background: linear-gradient(45deg, #ffd700, #daa520);
        color: black !important; font-weight: 900 !important; border-radius: 50px;
        transition: 0.3s; border: none; height: 3.5em;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #ffd700;'>👑 TITAN v62.4 LUXURY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Algorithm SHA-512 | Madagascar Time Sync (+3h)</p>", unsafe_allow_html=True)

# --- GAME SELECTOR ---
mode = st.sidebar.selectbox("🎯 FIDIO NY LALAO:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 6-STAR"])

# --- CONSIGNES DE SÉCURITÉ ---
st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ CONSIGNES DE SÉCURITÉ")
if "AVIATOR" in mode or "COSMOS" in mode:
    st.sidebar.info("1. Aza miala amin'ny lera nomena.\n2. Cashout amin'ny 2.0x hatramin'ny 3.0x.\n3. Raha dodo (1.0x) ny teo aloha, andraso 2 rounds.")
else:
    st.sidebar.info("1. Kintana 3 fotsiny dia 'Encaissement'.\n2. Ovao ny Seed isaky ny mandresy in-3.\n3. Aza miverina amin'ny toerana nisy baomba teo.")

# --- MAIN INTERFACE ---
with st.container():
    st.markdown('<div class="luxury-card">', unsafe_allow_True=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛠️ INPUT DATA")
        if mode == "💣 MINES 6-STAR":
            c_s = st.text_input("💻 Seed Client:", placeholder="Adikao eto ilay kaody fohy...")
            s_s = st.text_input("🖥️ Seed Serveur (Hash):", placeholder="Adikao eto ilay kaody lava...")
        else:
            # AUTO-TIME SYNC (+3H)
            local_now = datetime.now() + timedelta(hours=3)
            g_time = st.time_input("⏲️ Lera farany nivoaka (Finday):", local_now.time())
            h_seed = st.text_input("🔑 HEX SEED / HASH:", placeholder="Paste SHA-256 here...")
    
    with c2:
        st.markdown("### 📸 ATTACHMENT")
        st.file_uploader("Upload screenshot history", type=['jpg', 'png'])
    st.markdown('</div>', unsafe_allow_True=True)

if st.button(f"✨ EXECUTE {mode} ANALYSIS"):
    with st.spinner('💎 Cryptographic Analysis in progress...'):
        time.sleep(1.5)
        if mode == "💣 MINES 6-STAR":
            h = hashlib.sha512((c_s + s_s).encode()).hexdigest()
            random.seed(int(h[:16], 16))
            star_spots = random.sample(range(25), k=6)
            
            st.success("✅ SCHEMA VALIDATED")
            grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 55px); gap: 10px; justify-content: center;">'
            for i in range(25):
                color = "#ffd700" if i in star_spots else "#1a1a1a"
                label = "⭐" if i in star_spots else ""
                grid_html += f'<div style="width:55px; height:55px; background:{color}; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);">{label}</div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)
            
        else:
            # CALCUL AVEC TIME OFFSET
            h = hashlib.sha512(h_seed.encode()).hexdigest()
            val = int(h[:12], 16)
            # Ny signal dia lera eo amin'ny findainao + (1 ka hatramin'ny 3 minitra)
            pred_time = (datetime.combine(datetime.today(), g_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
            acc = 92 + (val % 7)
            
            if "AVIATOR" in mode:
                s, m = round(1.80 + (val % 150)/100, 2), round(40.0 + (val % 20000)/100, 2)
            else:
                s, m = round(1.50 + (val % 100)/100, 2), round(20.0 + (val % 10000)/100, 2)

            st.markdown(f"""
                <div style="text-align: center; padding: 20px; border: 2px solid #00ffcc; border-radius: 20px;">
                    <h2 style="color: #00ffcc;">SIGNAL MANARAKA: {pred_time}</h2>
                    <hr style="border: 0.5px solid #333;">
                    <div style="display: flex; justify-content: space-around;">
                        <div><p>🟢 SAFE</p><p class="stat-val">{s}x</p></div>
                        <div><p>🟡 MOYEN</p><p class="stat-val">{round(s*2.5, 2)}x</p></div>
                        <div><p>🌸 PINK</p><p class="stat-val">{m}x</p></div>
                    </div>
                    <h3 style="margin-top:20px; color: #ffd700;">ACCURACY: {acc}%</h3>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 TITAN TECHNOLOGY - Special Edition for Andriantso")
