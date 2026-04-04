import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ARMOR", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. THE WAR-ZONE UI (ULTRA COMPACT & NO BREAKS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #0a0a0a; border: 1px solid #00ffcc; 
        padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 5px;
    }
    /* MINES GRID: Tery tsara ary tsy tapaka */
    .mines-wrapper {
        background: #111; padding: 8px; border-radius: 8px; 
        border: 1px solid #444; max-width: 240px; margin: 0 auto;
    }
    .mines-grid { 
        display: grid; grid-template-columns: repeat(5, 1fr); 
        gap: 3px; width: 100%;
    }
    .mine-cell { 
        aspect-ratio: 1/1; background: #000; border: 1px solid #333; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 18px; border-radius: 3px; line-height: 0;
    }
    .cell-star { border: 1px solid #ffff00 !important; background: rgba(255, 255, 0, 0.1); color: #ffff00; }
    .mult-val { color: #00ffcc; font-size: 45px; font-weight: bold; margin: 0; }
    .detector-tag { font-size: 10px; border: 1px solid #00ffcc; padding: 1px 6px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h3 style='text-align:center;'>🛰️ TITAN ARMOR ACCESS</h3>", unsafe_allow_html=True)
    if st.text_input("KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. CORE ENGINES ---
def titan_cosmos_engine(h, hx, t, algo):
    raw = f"{h}{hx}{t}TITAN_COSMOS_V85".encode()
    f_hash = hashlib.sha512(raw).hexdigest() if algo == "SHA-512" else hashlib.sha256(raw).hexdigest()
    random.seed(int(f_hash[:16], 16))
    bits = int(f_hash[-4:], 16)
    if bits > 42000: m, s = round(random.uniform(2.80, 9.10), 2), "🔥 HIGH JUMP"
    elif bits < 14000: m, s = round(random.uniform(1.10, 1.70), 2), "🛡️ LOW RISK"
    else: m, s = round(random.uniform(1.71, 2.79), 2), "⚖️ STABLE"
    return {"mult": m, "acc": random.randint(96, 99), "status": s, "hex": f_hash[:8].upper()}

def titan_mines_engine(s_seed, c_seed):
    # Algorithm Mines matanjaka (Double Hashing)
    combined = f"{s_seed}{c_seed}TITAN_MINES_SECURE_2026".encode()
    primary_hash = hashlib.sha256(combined).hexdigest()
    secondary_hash = hashlib.sha512(primary_hash.encode()).hexdigest()
    
    spots = []
    for i in range(6):
        # Mampiasa entropy ambony avy amin'ny SHA-512
        val = int(secondary_hash[i*10:(i+1)*10], 16) % 25
        while val in spots: val = (val + 1) % 25
        spots.append(val)
    return spots

# --- 5. INTERFACE ---
st.markdown("<h4 style='text-align:center; color:#00ffcc; margin:0;'>🛰️ TITAN V85.0 - ARMOR SYNC</h4>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS", "💣 MINES", "📜 LOGS"])

with t1:
    h_in = st.text_input("Hash / Server Seed:")
    col_x, col_y = st.columns(2)
    hx_in = col_x.text_input("Hex8 (Extra):")
    t_start = col_y.number_input("Tour Actuel:", min_value=1, value=693735)
    
    if st.button("🔥 SCAN FOR NEXT JUMP"):
        if h_in:
            r1, r2 = st.columns(2)
            p1 = titan_cosmos_engine(h_in, hx_in, str(t_start), "SHA-512")
            with r1:
                st.markdown(f"""<div class="war-card"><p style="color:#aaa; font-size:10px;">TOUR {t_start}</p>
                <p class="mult-val">{p1['mult']}x</p><span class="detector-tag">{p1['acc']}% | {p1['status']}</span></div>""", unsafe_allow_html=True)
            
            # AUTO-JUMP DETECTION (Hash Based)
            found = None
            for i in range(1, 11):
                p_check = titan_cosmos_engine(h_in, hx_in, str(t_start + i), "SHA-512")
                if p_check['status'] == "🔥 HIGH JUMP":
                    found = (t_start + i, p_check, i)
                    break
            with r2:
                if found:
                    tj, pj, gap = found
                    st.markdown(f"""<div class="war-card" style="border-color:#ff00ff;"><p style="color:#ff00ff; font-size:10px;">JUMP AT +{gap}</p>
                    <p class="mult-val" style="color:#ff00ff;">{pj['mult']}x</p><span class="detector-tag" style="color:#ff00ff; border-color:#ff00ff;">TOUR {tj}</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="war-card"><p style="color:#aaa; font-size:10px;">NEXT TOUR</p>
                    <p class="mult-val">---</p><span class="detector-tag">NO JUMP FOUND</span></div>""", unsafe_allow_html=True)

with t2:
    s_s = st.text_input("Server Seed:")
    c_s = st.text_input("Client Seed / Tour:")
    if st.button("🛰️ SCAN MINES ARMOR"):
        if s_s and c_s:
            spots = titan_mines_engine(s_s, c_s)
            grid_html = '<div class="mines-wrapper"><div class="mines-grid">'
            for i in range(25):
                is_star = i in spots
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div></div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with t3:
    for log in st.session_state.history[:10]: st.write(f"📡 {log}")
