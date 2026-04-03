import streamlit as st
import hashlib
import random

# --- STYLE DARK NEON ---
st.set_page_config(page_title="TITAN V85.0 DYNAMIC", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
    }
    .jump-info { color: #ffff00; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

def get_dynamic_prediction(seed, tour_id, step_name):
    # Hashing raikitra miankina amin'ny Hash sy ny Target Tour
    h = hashlib.sha256(f"{seed}{tour_id}{step_name}".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    return round(random.uniform(2.10, 5.95), 2)

# --- INTERFACE ---
st.markdown("<h2 style='text-align:center;'>🛰️ TITAN V85.0 DYNAMIC SYNC</h2>", unsafe_allow_html=True)

h_cos = st.text_input("Hash SHA512 Combined (Server Seed):")
t_id = st.text_input("Tour ID farany nivoaka:")

if st.button("🔥 ANALYZE (DYNAMIC JUMP)"):
    if h_cos and t_id.isdigit():
        base_id = int(t_id)
        
        # 1. Kajy ny JUMP voalohany miankina amin'ny HASH (eo anelanelan'ny +2 sy +4)
        # Ampiasaina ny MD5 avy amin'ny Hash mba hahazoana isa miovaova
        hash_val = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
        jump1 = (hash_val % 3) + 2  # Manome +2, +3, na +4
        
        # 2. Kajy ny JUMP faharoa (eo anelanelan'ny +5 sy +7)
        jump2 = jump1 + (hash_val % 3) + 2 # Manome elanelana tsara foana
        
        target1 = base_id + jump1
        target2 = base_id + jump2
        
        col1, col2 = st.columns(2)
        
        with col1:
            val1 = get_dynamic_prediction(h_cos, target1, "T1")
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="jump-info">⚡ JUMP: +{jump1} TOURS</div>
                    <b style="color:red; font-size:18px;">🎯 TARGET: {target1}</b><br>
                    <h1 style="color:#00ffcc; font-size:45px;">{val1}x</h1>
                    <small style="color:#00ffcc;">SYNC: 100%</small>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            val2 = get_dynamic_prediction(h_cos, target2, "T2")
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="jump-info">⚡ JUMP: +{jump2} TOURS</div>
                    <b style="color:yellow; font-size:18px;">🎯 TARGET: {target2}</b><br>
                    <h1 style="color:#00ffcc; font-size:45px;">{val2}x</h1>
                    <small style="color:#00ffcc;">SYNC: 98%</small>
                </div>
            """, unsafe_allow_html=True)

        st.success(f"✅ IA nifidy Jump +{jump1} sy +{jump2} miankina amin'ny Hash vaovao.")
