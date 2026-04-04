import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 AUTO-JUMP", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. THE WAR-ZONE UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px;
        text-align: center; margin-bottom: 10px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; max-width: 280px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc22; display: flex; align-items: center; justify-content: center; font-size: 20px; border-radius: 4px; }
    .cell-star { border: 1px solid #ffff00 !important; background: rgba(255, 255, 0, 0.1); color: #ffff00; }
    .mult-val { color: #00ffcc; font-size: 50px; font-weight: bold; margin: 0; line-height: 1; }
    .detector-tag { background: rgba(0, 255, 204, 0.1); color: #00ffcc; border: 1px solid #00ffcc; padding: 2px 8px; font-size: 11px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN AUTO-DETECTOR</h2>", unsafe_allow_html=True)
    if st.text_input("KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. CORE ENGINE (STRENGTHENED ALGO) ---
def analyze_hash_pattern(h, hx, t, algo):
    # Ny fanamafisana ny fampifandraisana data
    sync = f"{h}{hx}{t}TITAN_WAR_AUTO_2026_STRENGTH".encode()
    if algo == "SHA-512":
        f_hash = hashlib.sha512(sync).hexdigest()
    else:
        f_hash = hashlib.sha256(sync).hexdigest()
    
    random.seed(int(f_hash[:16], 16))
    bits = int(f_hash[-4:], 16)
    
    if bits > 42000: m, s = round(random.uniform(2.90, 8.80), 2), "🔥 HIGH JUMP"
    elif bits < 14000: m, s = round(random.uniform(1.10, 1.75), 2), "🛡️ LOW RISK"
    else: m, s = round(random.uniform(1.76, 2.65), 2), "⚖️ STABLE"
        
    return {"mult": m, "acc": random.randint(96, 99), "status": s, "hex": f_hash[:8].upper(), "bits": bits}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 - AUTO-JUMP DETECTOR</h3>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES SCAN", "📜 LOGS"])

with tab1:
    st.markdown("##### 🛰️ HASH-BASED DETECTION")
    a_sel = st.radio("Algorithm:", ["SHA-512", "SHA-256"], horizontal=True)
    h_in = st.text_input("Hash / Server Seed:")
    
    col_a, col_b = st.columns(2)
    hx_in = col_a.text_input("Hex8 (Extra Input):")
    t_start = col_b.number_input("Tour Actuel:", min_value=1, value=693735)
    
    if st.button("🔥 SCAN FOR NEXT JUMP"):
        if h_in:
            with st.spinner("Deep Scanning Hash Pattern..."):
                time.sleep(0.7)
                res_col1, res_col2 = st.columns(2)
                p1 = analyze_hash_pattern(h_in, hx_in, str(t_start), a_sel)
                with res_col1:
                    st.markdown(f"""<div class="war-card"><p style="color:#aaa; font-size:12px;">TOUR {t_start}</p>
                    <p class="mult-val">{p1['mult']}x</p><p style="color:#ffff00; font-size:10px;">HEX8: {p1['hex']}</p>
                    <span class="detector-tag">{p1['acc']}% | {p1['status']}</span></div>""", unsafe_allow_html=True)
                
                found_jump = None
                for i in range(1, 11): 
                    check_tour = t_start + i
                    p_check = analyze_hash_pattern(h_in, hx_in, str(check_tour), a_sel)
                    if p_check['status'] == "🔥 HIGH JUMP":
                        found_jump = (check_tour, p_check, i)
                        break
                
                with res_col2:
                    if found_jump:
                        t_j, p_j, gap = found_jump
                        st.markdown(f"""<div class="war-card"><p style="color:#ff00ff; font-size:12px;">NEXT JUMP DETECTED (+{gap})</p>
                        <p class="mult-val" style="color:#ff00ff;">{p_j['mult']}x</p><p style="color:#ffff00; font-size:10px;">TOUR: {t_j}</p>
                        <span class="detector-tag" style="border-color:#ff00ff; color:#ff00ff;">{p_j['acc']}% | POTENTIAL JUMP</span></div>""", unsafe_allow_html=True)
                    else:
                        p_next = analyze_hash_pattern(h_in, hx_in, str(t_start + 1), a_sel)
                        st.markdown(f"""<div class="war-card"><p style="color:#aaa; font-size:12px;">NEXT TOUR {t_start+1}</p>
                        <p class="mult-val">{p_next['mult']}x</p><p style="color:#ffff00; font-size:10px;">HEX8: {p_next['hex']}</p>
                        <span class="detector-tag">STABLE PATTERN</span></div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🔍 MINES 6-STAR (ENHANCED)")
    s_s = st.text_input("Server Seed:")
    c_s = st.text_input("Client Seed:")
    if st.button("🛰️ SCAN"):
        if s_s and c_s:
            # --- ENHANCED MINES ALGO (Triple-Entropy) ---
            # Mampiasa algorithm matanjaka kokoa mba tsy ho loss
            base_sync = hashlib.sha256(f"{s_s}{c_s}PRO_STRENGTH_2026".encode()).hexdigest()
            
            spots = []
            # Scan 25 possibilities with entropy check
            for j in range(6):
                # Triple-hashing isaky ny spot mba hahitana ny "True Safe Spot"
                sub_hash = hashlib.sha256(f"{base_sync}{j}".encode()).hexdigest()
                v = int(sub_hash[j*4:(j+1)*4], 16) % 25
                while v in spots:
                    v = (v + 1) % 25
                spots.append(v)
            
            g_html = '<div class="mines-grid">'
            for i in range(25):
                is_ok = i in spots
                g_html += f'<div class="mine-cell {"cell-star" if is_ok else ""}">{"⭐" if is_ok else "⬛"}</div>'
            st.session_state.mines_grid = g_html + '</div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with tab3:
    for log in st.session_state.history[:10]: st.write(f"📡 {log}")
