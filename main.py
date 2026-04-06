import streamlit as st
import hashlib
import random
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.7 - DYNAMIC MACHINE", layout="wide")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: 
    st.session_state.mines_grid = ""

# --- 2. STYLE (WAR INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; transform: scale(1.05); }
    .scan-box { border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>💀 TITAN DYNAMIC MACHINE</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE LETHAL MODE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. THE DYNAMIC CORE ---
def mutate_seed(seed: str) -> str:
    """Mutation kely amin'ny seed: rotate sy xor"""
    rotated = seed[::-1]
    xor_val = ''.join(chr(ord(c) ^ 0x5A) for c in rotated)
    return xor_val

def proof_of_work(h: bytes, difficulty: int = 16) -> bool:
    """Proof-of-Work: hash < target"""
    target = 2 ** (512 - difficulty)
    val = int.from_bytes(h, 'big')
    return val < target

def lethal_engine(s_seed, c_seed, t_id, iters=None):
    """Deep SHA-512 + BLAKE2b Hashing miaraka amin'ny mutation, variable iterations, proof-of-work"""
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

    # Proof-of-Work check
    if not proof_of_work(final, difficulty=20):
        final = hashlib.sha512(final).digest()

    return final.hex()

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.7 - DYNAMIC DEATH MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS (DYNAMIC JUMP)", "💣 MINES (DOUBLE SHUFFLE)"])

with tab1:
    st.markdown("##### 🛡️ HASH-DRIVEN VOLATILE JUMP")
    st.info("Ny algorithm no mifidy elanelana (Gap) miankina amin'ny Hash SHA-512 + BLAKE2b + Proof-of-Work.")
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8137473)
    
    if st.button("🚀 EXECUTE DYNAMIC SCAN"):
        if h_in:
            with st.spinner("Analyzing Hash Stability..."):
                pilot_hash = lethal_engine(h_in, hx_in, t_act, 15000)
                p_int = int(pilot_hash[:8], 16)
                
                j1 = (p_int % 3) + 2
                j2 = j1 + (p_int % 4) + 2
                j3 = j2 + (p_int % 6) + 3
                dynamic_slots = [j1, j2, j3]
                
                for j in dynamic_slots:
                    target_t = t_act + j
                    res_hash = lethal_engine(h_in, hx_in, target_t, 60000)
                    random.seed(int(res_hash[:16], 16))
                    
                    f = int(res_hash[-12:], 16) / 281474976710655.0
                    m = round(random.uniform(15.0, 150.0), 2) if f > 0.96 else round(random.uniform(1.10, 5.50), 2)
                    color = "#ff0000" if m > 10.0 else "#00ffcc"
                    
                    st.markdown(f"""
                        <div class="scan-box" style="border-color: {color};">
                            <span style="color:#aaa;">DYNAMIC TARGET: TOUR {target_t} (GAP +{j})</span><br>
                            <span style="font-size:35px; color:{color}; font-weight:bold;">{m}x</span>
                        </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES HYPER-CHAOS (Variable Iterations + Adaptive Shuffle + Proof-of-Work)")
    st.error("DOUBLE SHUFFLE ACTIVE: Tsy misy pattern raikitra intsony.")
    col_a, col_b = st.columns(2)
    s_s = col_a.text_input("Server Seed:")
    c_s = col_b.text_input("Client Seed:")
    t_id = st.text_input("ID Partie (Next ID):")
    
    if st.button("🛰️ SCAN FOR DYNAMIC SCHEMA"):
        if s_s and c_s and t_id:
            with st.spinner("Executing Variable Iterations..."):
                main_hash = lethal_engine(s_s, c_s, t_id)
                hash_int = int(main_hash, 16)
                
                grid = list(range(25))
                # Shuffle 1
                for i in range(24, 0, -1):
                    j = hash_int % (i + 1)
                    grid[i], grid[j] = grid[j], grid[i]
                    hash_int //= (i + 1)
                
                # Adaptive Shuffle (2 na 3 sosona arakaraka ny hash)
                shuffle_count = 2 if int(main_hash[:4], 16) % 2 == 0 else 3
                random.seed(int(main_hash[-16:], 16))
                for _ in range(shuffle_count):
                    random.shuffle(grid)
                
                spots = grid[:5]
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("SCHEMA LOCKED - ADAPTIVE DOUBLE SHUFFLE PROTECTION ACTIVE")
