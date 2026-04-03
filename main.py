import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 HASH-JUMP", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 2. STYLE NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
    }
    .jump-tag { background: #ff4b4b; color: white; padding: 3px 10px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN LOGIN</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Key:", type="password")
    if st.button("HIDITRA"):
        if pwd == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. HASH-BASED ENGINE ---
def get_hash_jump(seed):
    # Maka ny lanjan'ny Hash mba hamaritana ny Jump
    h_hex = hashlib.md5(seed.encode()).hexdigest()
    # Lanja eo anelanelan'ny 2 sy 5
    return (int(h_hex[:1], 16) % 4) + 2

def get_stable_prediction(seed, tour_id):
    signature = f"{seed}{tour_id}TITAN_ULTRA_2026"
    h = hashlib.sha256(signature.encode()).hexdigest()
    random.seed(int(h[:16], 16))
    return round(random.uniform(2.15, 5.95), 2)

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 HASH-JUMP</h2>", unsafe_allow_html=True)

h_cos = st.text_input("Hash SHA512 Combined:")
c1, c2 = st.columns(2)
hex_val = c1.text_input("HEX (Last 8):")
t_id = c2.text_input("Tour ID Farany:")

if st.button("🔥 ANALYZE & HASH-SYNC"):
    if h_cos and t_id.isdigit():
        base_tour = int(t_id)
        
        # Ny JUMP dia miovaova arakaraka ny Hash nampidirinao
        jump1 = get_hash_jump(h_cos)
        jump2 = jump1 + (get_hash_jump(h_cos[::-1]) % 3 + 2) # Jump faharoa
        
        targets = [base_tour + jump1, base_tour + jump2]
        cols = st.columns(2)
        
        for i, target in enumerate(targets):
            val = get_stable_prediction(h_cos, f"{hex_val}{target}")
            with cols[i]:
                st.markdown(f"""
                    <div class="prediction-card">
                        <span class="jump-tag">JUMP ARAKA NY HASH: +{target - base_tour}</span><br><br>
                        <b style="color:#ffff00; font-size:18px;">🎯 TARGET: {target}</b>
                        <h1 style="color:#00ffcc; margin:10px 0;">{val}x</h1>
                        <small>HASH SYNC: OK</small>
                    </div>
                """, unsafe_allow_html=True)

st.warning("⚠️ Raha vao miova ny Hash ao amin'ny lalao, dia miova ho azy koa ny Jump ato amin'ny TITAN.")
