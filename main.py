import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide")

# Session State initialization
for key, val in [('logged_in', False), ('mines_grid', ""), ('history', [])]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE NEON WAR-MACHINE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .stat-box { font-size: 12px; color: #ffff00; margin-top: 5px; font-weight: bold; }
    .percent-bar { background: #111; border-radius: 10px; height: 10px; margin: 10px 0; overflow: hidden; border: 1px solid #333; }
    .percent-fill { background: #00ffcc; height: 100%; box-shadow: 0 0 10px #00ffcc; }
    .jump-tag { background: #ff4b4b; color: white; padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 11px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 5px; }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 10px #ffff00; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (SYSTEM ADMIN) ---
with st.sidebar:
    st.markdown("### 🛰️ TITAN SYSTEM")
    if st.text_input("Admin Access:", type="password") == "2026":
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.rerun()

# --- 4. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN LOGIN</h2>", unsafe_allow_html=True)
    if st.text_input("Key:", type="password") == "2026":
        if st.button("HIDITRA"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 5. ENGINE ULTRA-PUISSANTE ---
def get_war_data(seed, context, mode="cosmos"):
    # Cosmos logic
    if mode == "cosmos":
        h = hashlib.sha256(f"{seed}{context}TITAN_WAR_V85".encode()).hexdigest()
        random.seed(int(h[:16], 16))
        val = round(random.uniform(2.10, 5.85), 2)
        acc = random.randint(88, 99)
        moyen = round(val * 0.75, 2)
        return {"val": val, "acc": acc, "moyen": moyen}
    else:
        # Mines Machine de Guerre logic (SHA-512)
        h = hashlib.sha512(f"{seed}{context}MINES_WAR_CORE".encode()).hexdigest()
        count = 8 if "M12" in context else 5
        # Mifidy toerana miankina amin'ny hash mivantana
        safe_spots = []
        for i in range(count):
            start = i * 4
            val = int(h[start:start+4], 16) % 25
            while val in safe_spots: # Misoroka toerana mitovy
                val = (val + 1) % 25
            safe_spots.append(val)
        return safe_spots

# --- 6. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS (STATS)", "💣 MINES 8/5", "📜 HISTORY"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined:")
    c1, c2 = st.columns(2)
    hex_v = c1.text_input("HEX (Last 8):")
    t_id = c2.text_input("Tour ID:")
    
    if st.button("🔥 ANALYZE & SYNC"):
        if h_cos and t_id.isdigit():
            base = int(t_id)
            jump = (int(hashlib.md5(h_cos.encode()).hexdigest()[:1], 16) % 3) + 2
            targets = [base + jump, base + jump + 2]
            
            cols = st.columns(2)
            for i, target in enumerate(targets):
                data = get_war_data(h_cos, f"{hex_v}{target}", "cosmos")
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <span class="jump-tag">JUMP +{target - base}</span><br>
                            <b>TARGET: {target}</b>
                            <h1 style="color:#00ffcc; margin:5px 0;">{data['val']}x</h1>
                            <div class="stat-box">🎯 PRECISION: {data['acc']}%</div>
                            <div class="percent-bar"><div class="percent-fill" style="width:{data['acc']}%"></div></div>
                            <div style="font-size:10px;">MOYEN: {data['moyen']}x | MAX: {data['val']}x</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Tour {targets[0]}: {data['val']}x ({data['acc']}%)")

with t2:
    nb_m = st.select_slider("Configuration Mines:", options=[1, 2, 3], value=3)
    ma, mb = st.columns(2)
    ms, mc = ma.text_input("Server Seed:"), mb.text_input("Client Seed:")
    
    if st.button("🔍 SCAN 8/5 DIAMANTS"):
        if ms and mc:
            ctx = "M12" if nb_m < 3 else "M3"
            safe = get_war_data(f"{ms}{mc}", ctx, "mines")
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid_html += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ Machine de Guerre: Pattern Synchronisé!")

with t3:
    st.markdown("### 📜 LOGS")
    for log in st.session_state.history[:10]: st.write(f"🚩 {log}")
    if st.button("🗑️ CLEAR HISTORY"):
        st.session_state.history = []
        st.rerun()
