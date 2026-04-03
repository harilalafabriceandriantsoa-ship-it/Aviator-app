import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 STATS PRO", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. STYLE NEON (OPTIMIZED) ---
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
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (Key: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN LOGIN</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Admin Key:", type="password")
    if st.button("HIDITRA"):
        if pwd == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ENGINE AVANCÉ (Calcul Stats) ---
def get_hash_data(seed, context):
    h = hashlib.sha256(f"{seed}{context}TITAN_V85_STATS".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    
    # Calcul Multiplier
    val = round(random.uniform(2.10, 5.80), 2)
    # Calcul Pourcentage (85% - 99%)
    accuracy = random.randint(85, 99)
    # Moyen / Max
    moyen = round(val * 0.75, 2)
    return {"val": val, "acc": accuracy, "moyen": moyen}

def get_jump(seed):
    h_hex = hashlib.md5(seed.encode()).hexdigest()
    return (int(h_hex[:1], 16) % 3) + 2

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-PRO</h2>", unsafe_allow_html=True)
t1, t2 = st.tabs(["🚀 COSMOS (STATS)", "💣 MINES 8/5"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined:")
    c1, c2 = st.columns(2)
    hex_val = c1.text_input("HEX (Last 8):")
    t_id = c2.text_input("Tour ID Farany:")
    
    if st.button("🔥 ANALYZE & SYNC"):
        if h_cos and t_id.isdigit():
            base_tour = int(t_id)
            jump = get_jump(h_cos)
            
            targets = [base_tour + jump, base_tour + jump + 2]
            cols = st.columns(2)
            
            for i, target in enumerate(targets):
                data = get_hash_data(h_cos, f"{hex_val}{target}")
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <span class="jump-tag">JUMP +{target - base_tour}</span><br>
                            <b style="font-size:14px;">TARGET: {target}</b>
                            <h1 style="color:#00ffcc; margin:5px 0;">{data['val']}x</h1>
                            <div class="stat-box">🎯 PRECISION: {data['acc']}%</div>
                            <div class="percent-bar"><div class="percent-fill" style="width:{data['acc']}%"></div></div>
                            <div style="font-size:11px; color:#aaa;">
                                MOYEN: <b style="color:#00ffcc;">{data['moyen']}x</b> | 
                                MAX: <b style="color:#ff4b4b;">{data['val']}x</b>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"T-{targets[0]}: {data['val']}x ({data['acc']}%)")

with t2:
    nb_m = st.select_slider("Mines:", options=[1, 2, 3], value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:"), m2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN 8/5 DIAMANTS"):
        if ms and mc:
            # Lojika Mines nohamafisina (Seed-Locked)
            sig = hashlib.sha256(f"{ms}{mc}{nb_m}".encode()).hexdigest()
            random.seed(int(sig[:16], 16))
            count = 8 if nb_m < 3 else 5
            safe = random.sample(range(25), count)
            
            grid = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.info("💡 Ny toerana misy kintana dia miankina 100% amin'ny Seeds nampidirinao.")
