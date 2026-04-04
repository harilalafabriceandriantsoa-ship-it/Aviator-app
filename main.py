import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION SYSTEM ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide")

# Initialization ny fitadidiana (Memory)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE NEON MACHINE DE GUERRE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .war-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 15px #ffff00; color: #ffff00; background: rgba(255, 255, 0, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ADMIN (KEY & RESET) ---
with st.sidebar:
    st.markdown("### 🛰️ TITAN ADMIN PANEL")
    admin_key = st.text_input("Admin Access Key:", type="password")
    if admin_key == "2026":
        st.success("✅ ADMIN ACCESS GRANTED")
        if st.button("🗑️ RESET ALL MACHINE DATA"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.warning("Mila Key Admin raha hanatontosa Reset.")

# --- 4. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    login_key = st.text_input("Ampidiro ny Key Activant:", type="password")
    if st.button("HIDITRA AMIN'NY TITAN"):
        if login_key == "2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Key diso! Jereo ny fanomezana avy amin'ny Admin.")
    st.stop()

# --- 5. ENGINE CORE (SHA-512) ---
def titan_engine(seed, context, mode, count=5):
    if mode == "cosmos":
        h = hashlib.sha256(f"{seed}{context}WAR_V85".encode()).hexdigest()
        random.seed(int(h[:16], 16))
        val = round(random.uniform(1.85, 4.50), 2)
        acc = random.randint(92, 99)
        return {"val": val, "acc": acc}
    else:
        # Mines Machine de Guerre logic (Algorithm SHA-512)
        h = hashlib.sha512(f"{seed}{context}MINES_V85_CORE".encode()).hexdigest()
        safe_spots = []
        for i in range(count):
            # Mifidy toerana miankina amin'ny hash mivantana
            val = int(h[i*5:i*5+5], 16) % 25
            while val in safe_spots: # Misoroka toerana mitovy
                val = (val + 1) % 25
            safe_spots.append(val)
        return safe_spots

# --- 6. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS ANALYZER", "💣 MINES SCANNER", "📜 HISTORY"])

with t1:
    st.markdown("### 🛰️ COSMOS / AVIATOR PREDICTION")
    h_val = st.text_input("Server Hash (Current):")
    t_id = st.text_input("Next Round ID:")
    if st.button("🔥 ANALYZE PATTERN"):
        if h_val and t_id:
            data = titan_engine(h_val, t_id, "cosmos")
            st.markdown(f"""
                <div class="war-card">
                    <p>TARGET PREDICTED</p>
                    <h1 style="color:#00ffcc; font-size:60px;">{data['val']}x</h1>
                    <p>🎯 PRECISION: {data['acc']}%</p>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Round {t_id}: {data['val']}x ({data['acc']}%)")

with t2:
    st.markdown("### 🔍 MINES SHA-512 SCANNER")
    # Isan'ny diamondra azo fidiana (3 hatramin'ny 8)
    nb_diamants = st.select_slider("Isan'ny Diamondra (Target):", options=[3, 4, 5, 6, 7, 8], value=5)
    
    col_a, col_b = st.columns(2)
    s_seed = col_a.text_input("Server Seed:")
    c_seed = col_b.text_input("Client Seed:")
    
    if st.button("🛰️ START DEEP SCAN"):
        if s_seed and c_seed:
            safe = titan_engine(s_seed, c_seed, "mines", count=nb_diamants)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid_html += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ Machine de Guerre: Pattern {nb_diamants} Diamants Synchronisé!")

with t3:
    st.markdown("### 📜 SYSTEM LOGS")
    for log in st.session_state.history[:10]:
        st.write(f"🚩 {log}")
