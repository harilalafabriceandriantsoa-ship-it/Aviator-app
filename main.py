import streamlit as st
import hashlib, random, hmac

st.set_page_config(page_title="TITAN V86.7 - COSMOS & MINES", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def lethal_engine(s_seed, c_seed, t_id, iters=None):
    if iters is None:
        base_val = int(hashlib.sha256(f"{s_seed}{c_seed}{t_id}".encode()).hexdigest(), 16)
        iters = 80000 + (base_val % 40000)
    combined = f"{s_seed}:{c_seed}:{t_id}:COSMOS_V86.7"
    h = hmac.new(b"COSMOS_CORE", combined.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h = hmac.new(h, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h).digest()
    final = bytes(a ^ b for a, b in zip(h, blake))
    return final.hex()

def mines_schema(server_seed, client_seed, nonce, mines_choice=1):
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}:{mines_choice}".encode()).hexdigest()
    hash_int = int(h, 16)
    grid = list(range(25))
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    random.seed(int(h[-16:], 16))
    random.shuffle(grid)
    return grid[:5]  # Always 5 diamonds

# --- INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.7 - COSMOS & MINES</h3>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💣 MINES", "🔍 VERIFIER"])

with tab1:
    st.markdown("##### 🌌 COSMOS PREDICTION")
    s_seed = st.text_input("Server Seed:", key="cosmos_server_seed")
    c_seed = st.text_input("Client Seed:", key="cosmos_client_seed")
    t_id = st.number_input("Tour ID:", min_value=1, value=1001, key="cosmos_tour")
    if st.button("🚀 RUN COSMOS", key="btn_cosmos"):
        cosmos_hash = lethal_engine(s_seed, c_seed, t_id, 15000)
        p_int = int(cosmos_hash[:8], 16)
        jump1 = (p_int % 3) + 2
        jump2 = jump1 + (p_int % 4) + 2
        jump3 = jump2 + (p_int % 6) + 3
        st.write("Cosmos Prediction Jumps:", [jump1, jump2, jump3])

with tab2:
    st.markdown("##### 💣 MINES SCHEMA (Always 5 Diamonds)")
    s_s = st.text_input("Server Seed:", key="mines_server_seed")
    c_s = st.text_input("Client Seed:", key="mines_client_seed")
    t_id = st.text_input("Game ID:", key="mines_game_id")
    mines_choice = st.slider("Select Mines Choice (1–3):", 1, 3, 1, key="mines_choice")
    if st.button("🛰️ GENERATE SCHEMA", key="btn_generate_schema"):
        schema = mines_schema(s_s, c_s, t_id, mines_choice)
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else ""}</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

with tab3:
    st.markdown("##### 🔍 VERIFIER (Always 5 Diamonds)")
    vs = st.text_input("Verifier Server Seed:", key="verifier_server_seed")
    vc = st.text_input("Verifier Client Seed:", key="verifier_client_seed")
    vn = st.text_input("Verifier Game ID:", key="verifier_game_id")
    mines_choice_v = st.slider("Verifier Mines Choice (1–3):", 1, 3, 1, key="verifier_mines_choice")
    if st.button("🔎 VERIFY SCHEMA", key="btn_verify_schema"):
        schema = mines_schema(vs, vc, vn, mines_choice_v)
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else ""}</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        st.info("Verifier is the official source of truth. Always 5 diamonds, schema differs for choice 1–3.")
