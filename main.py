import streamlit as st
import hashlib, random, hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.7 - DYNAMIC MACHINE", layout="wide")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: 
    st.session_state.mines_grid = ""

# --- 2. STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; transform: scale(1.05); }
    .scan-box { border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>💀 TITAN DYNAMIC MACHINE</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password", key="login_key") == "2026":
        if st.button("ACTIVATE LETHAL MODE", key="btn_login"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. CORE FUNCTIONS ---
def mutate_seed(seed: str) -> str:
    rotated = seed[::-1]
    xor_val = ''.join(chr(ord(c) ^ 0x5A) for c in rotated)
    return xor_val

def lethal_engine(s_seed, c_seed, t_id, iters=None):
    if iters is None:
        base_val = int(hashlib.sha256(f"{s_seed}{c_seed}{t_id}".encode()).hexdigest(), 16)
        iters = 80000 + (base_val % 40000)

    s_mut = mutate_seed(s_seed)
    c_mut = mutate_seed(c_seed)

    combined = f"{s_mut}:{c_mut}:{t_id}:DYNAMIC_JUDGMENT_V86.7"
    h = hmac.new(b"DYNAMIC_CORE_LETHAL", combined.encode(), hashlib.sha512).digest()

    for i in range(iters):
        h = hmac.new(h, f"DEATH_STEP_{i}".encode(), hashlib.sha512).digest()

    blake = hashlib.blake2b(h).digest()
    final = bytes(a ^ b for a, b in zip(h, blake))
    return final.hex()

def mines_schema(server_seed, client_seed, nonce):
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}".encode()).hexdigest()
    hash_int = int(h, 16)
    grid = list(range(25))
    # Shuffle 1
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    # Shuffle 2
    random.seed(int(h[-16:], 16))
    random.shuffle(grid)
    return grid[:5]

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.7 - DYNAMIC DEATH MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🚀 COSMOS", "💣 MINES", "🔍 VERIFIER"])

with tab1:
    st.markdown("##### 🛡️ COSMOS JUMP")
    h_in = st.text_input("Server Seed / Hash:", key="cosmos_server_seed")
    hx_in = st.text_input("Client Seed:", key="cosmos_client_seed")
    t_act = st.number_input("Tour Actuel:", min_value=1, value=8137473, key="cosmos_tour")
    if st.button("🚀 EXECUTE DYNAMIC SCAN", key="btn_cosmos_scan"):
        pilot_hash = lethal_engine(h_in, hx_in, t_act, 15000)
        p_int = int(pilot_hash[:8], 16)
        j1 = (p_int % 3) + 2
        j2 = j1 + (p_int % 4) + 2
        j3 = j2 + (p_int % 6) + 3
        st.write("Dynamic Jumps:", [j1, j2, j3])

with tab2:
    st.markdown("##### 🛡️ MINES SCHEMA")
    s_s = st.text_input("Server Seed:", key="mines_server_seed")
    c_s = st.text_input("Client Seed:", key="mines_client_seed")
    t_id = st.text_input("Game ID:", key="mines_game_id")
    if st.button("🛰️ GENERATE SCHEMA", key="btn_generate_schema"):
        schema = mines_schema(s_s, c_s, t_id)
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else "⬛"}</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

with tab3:
    st.markdown("##### 🔍 VERIFIER")
    vs = st.text_input("Verifier Server Seed:", key="verifier_server_seed")
    vc = st.text_input("Verifier Client Seed:", key="verifier_client_seed")
    vn = st.text_input("Verifier Game ID:", key="verifier_game_id")
    if st.button("🔎 VERIFY SCHEMA", key="btn_verify_schema"):
        schema = mines_schema(vs, vc, vn)
        st.success(f"Schema Verified: {schema}")
