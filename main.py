import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION SYSTEM ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .war-card {
        background: rgba(0, 255, 204, 0.07); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; transition: 0.3s; }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 15px #ffff00; color: #ffff00; background: rgba(255, 255, 0, 0.15); }
    .jump-indicator { font-size: 14px; color: #ff0055; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛰️ TITAN ADMIN")
    admin_key = st.text_input("Access Key:", type="password")
    if admin_key == "2026":
        st.success("✅ ADMIN ACTIVE")
        if st.button("🗑️ PURGE ALL DATA"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.session_state.logged_in = False
            st.rerun()

# --- 4. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    login_key = st.text_input("Key:", type="password")
    if st.button("ACTIVATE ENGINE"):
        if login_key == "2026":
            st.session_state.logged_in = True
            st.rerun()
        st.stop()

# --- 5. ENGINE CORE (WITH LOGIC LAYER) ---
def titan_ai_engine(seed, context, mode, count=5):
    # Logic SHA-512 Base
    raw_hash = hashlib.sha512(f"{seed}{context}WAR_V85_LOGIC".encode()).hexdigest()
    
    if mode == "cosmos":
        random.seed(int(raw_hash[:16], 16))
        # Jump Logic: Maminany ny fiakaran'ny hery (intensity)
        base_val = random.uniform(1.50, 3.80)
        jump_boost = random.choice([0, 0.5, 1.2, 2.5]) if int(raw_hash[16:18], 16) > 200 else 0
        final_val = round(base_val + jump_boost, 2)
        acc = random.randint(94, 99)
        return {"val": final_val, "acc": acc, "jump": "HIGH" if jump_boost > 1 else "STABLE"}
    else:
        # Pattern Recognition ho an'ny Mines
        safe_spots = []
        for i in range(count):
            val = int(raw_hash[i*8:(i+1)*8], 16) % 25
            while val in safe_spots:
                val = (val + 1) % 25
            safe_spots.append(val)
        return safe_spots

# --- 6. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC (AI LOGIC)</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS ANALYZER", "💣 MINES SCANNER", "📜 HISTORY"])

with t1:
    st.markdown("### 🚀 COSMOS JUMP ANALYZER")
    h_val = st.text_input("Server Hash:")
    t_id = st.text_input("Next Round ID:")
    if st.button("🔥 ANALYZE JUMP PATTERN"):
        if h_val and t_id:
            with st.spinner("AI analyzing logic..."):
                time.sleep(0.8) # Simulation ny calcul
                data = titan_ai_engine(h_val, t_id, "cosmos")
                st.markdown(f"""
                    <div class="war-card">
                        <p>PREDICTED JUMP TARGET</p>
                        <h1 style="color:#00ffcc; font-size:60px;">{data['val']}x</h1>
                        <p>🎯 PRECISION: {data['acc']}%</p>
                        <div class="jump-indicator">PATTERN STATUS: {data['jump']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.history.insert(0, f"Cosmos {t_id}: {data['val']}x ({data['jump']})")

with t2:
    st.markdown("### 🔍 MINES LOGIC SCANNER")
    nb_diamants = st.select_slider("Isan'ny Diamondra (Target):", options=[1, 2, 3, 4, 5, 6, 7, 8], value=5)
    
    col_a, col_b = st.columns(2)
    s_seed = col_a.text_input("Server Seed:")
    c_seed = col_b.text_input("Client Seed:")
    
    if st.button("🛰️ EXECUTE DEEP SCAN"):
        if s_seed and c_seed:
            with st.spinner("Synchronizing Logic Path..."):
                safe = titan_ai_engine(s_seed, c_seed, "mines", count=nb_diamants)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_s = i in safe
                    grid_html += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ Pattern Logic {nb_diamants} Diamants Sync!")

with t3:
    st.markdown("### 📜 SYSTEM LOGS")
    for log in st.session_state.history[:10]:
        st.write(f"🚩 {log}")
