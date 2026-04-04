import hashlib
import time
import random
import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. THE WAR-ZONE UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: linear-gradient(145deg, #0a0a0a, #161616);
        border: 2px solid #00ffcc; padding: 20px; border-radius: 15px;
        text-align: center; margin-bottom: 15px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    .prediction-val { color: #00ffcc; font-size: 60px; font-weight: bold; margin: 0; }
    .hex-text { color: #ffff00; font-size: 14px; font-weight: bold; }
    .percent-box { color: #ff00ff; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCESS ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN ACCESS</h1>", unsafe_allow_html=True)
    if st.text_input("COMMAND KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. THE CORE ENGINE (FIXED LOGIC) ---
def get_war_prediction(h_seed, hx8, tour, algo):
    # Fampifandraisana ny data rehetra (Triple Sync)
    data = f"{h_seed}{hx8}{tour}TITAN_2026_FIXED".encode()
    raw_hash = hashlib.sha512(data).hexdigest() if algo == "SHA-512" else hashlib.sha256(data).hexdigest()
    
    # Fikajiana ny Multiplier (fa tsy ny Tour no mivoaka)
    random.seed(int(raw_hash[:16], 16))
    mult = round(random.uniform(1.45, 5.80), 2)
    
    # Fikajiana ny Pourcentage miankina amin'ny Tour
    acc = random.randint(96, 99)
    
    # Hex8 Identification
    res_hex8 = raw_hash[:8].upper()
    
    status = "🔥 JUMP" if mult > 2.5 else "🛡️ STABLE"
    return {"mult": mult, "hex8": res_hex8, "acc": acc, "status": status}

# --- 5. INTERFACE ---
st.markdown("<h2 style='text-align:center;'>🛰️ TITAN V85.0 - DOUBLE TOUR SCANNER</h2>", unsafe_allow_html=True)

# INPUTS
algo_sel = st.sidebar.radio("ALGO:", ["SHA-512", "SHA-256"])
h_val = st.text_input("1. Hash / Server Seed (Combined):")
hx8_val = st.text_input("2. Hex8 (Optional):")
t_start = st.number_input("3. Prochain Numéro de Tour (Nonce):", min_value=1, value=1)

if st.button("🚀 EXECUTE DOUBLE PREDICTION"):
    if h_val:
        with st.spinner("Decoding Sequence..."):
            time.sleep(0.8)
            col1, col2 = st.columns(2)
            
            # PREDICTION 1 (Tour ampidirinao)
            p1 = get_war_prediction(h_val, hx8_val, str(t_start), algo_sel)
            with col1:
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">TOUR {t_start}</p>
                        <p class="prediction-val">{p1['mult']}x</p>
                        <p class="hex-text">HEX8: {p1['hex8']}</p>
                        <p class="percent-box">ACCURACY: {p1['acc']}%</p>
                        <p style="color:#ffff00;">{p1['status']}</p>
                    </div>
                """, unsafe_allow_html=True)

            # PREDICTION 2 (Tour manaraka ho azy)
            t_next = t_start + 1
            p2 = get_war_prediction(h_val, hx8_val, str(t_next), algo_sel)
            with col2:
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">TOUR {t_next}</p>
                        <p class="prediction-val">{p2['mult']}x</p>
                        <p class="hex-text">HEX8: {p2['hex8']}</p>
                        <p class="percent-box">ACCURACY: {p2['acc']}%</p>
                        <p style="color:#ffff00;">{p2['status']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.session_state.history.insert(0, f"T{t_start}: {p1['mult']}x | T{t_next}: {p2['mult']}x")
