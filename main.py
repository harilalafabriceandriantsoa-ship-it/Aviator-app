import streamlit as st
import hashlib, hmac, random, datetime

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V94 - ULTRA MACHINE", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: auto; padding: 20px; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; color: #444; }
    .cell-star { border: 2px solid #00ffcc !important; background: rgba(0, 255, 204, 0.2) !important; color: #00ffcc !important; box-shadow: 0 0 15px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINES (Tsy misy kitihana ny algorithm) ---

def mines_ultra_engine(server_seed, client_seed, nonce, num_mines, choice=1):
    try:
        base = f"{server_seed}:{client_seed}:{nonce}:{choice}:V94_MINES"
        h1 = hashlib.sha512(base.encode()).digest()
        h2 = hashlib.blake2b(h1).digest()
        hash_int = int.from_bytes(h1 + h2, "big")
        
        grid = list(range(25))
        random.seed(hash_int % 1000000)
        random.shuffle(grid)
        
        # Mamoaka kintana araka ny isan'ny mine (raha 1 mine dia kintana 1)
        # Fa mba ho azo antoka kokoa, mamoaka "Safe Spots" 5 foana izahay
        return grid[:5] 
    except: return []

def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt):
    try:
        base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:V94_COSMOS"
        h1 = hmac.new(b"V94_CORE", base.encode(), hashlib.sha512).hexdigest()
        p_int = int(h1[:12], 16)
        offset = (p_int % 15) + (5 if salt == "T1" else 10)
        jumps = [(p_int % 5) + 2, (p_int % 8) + 3]
        return {"hex": h1, "tour": tour_id + offset, "jumps": jumps}
    except: return None

def aviator_studio_engine(hex_val, heure, salt):
    try:
        hex_clean = "".join(c for c in hex_val if c in "0123456789abcdef")
        h_int = int(hex_clean[:12], 16)
        mask = int(heure.replace(":", "")) ^ int.from_bytes(salt.encode(), "big")
        base = h_int ^ mask
        delta = (base % 5) + (2 if salt == "T1" else 4)
        h_dt = datetime.datetime.strptime(heure, "%H:%M")
        h_new = (h_dt + datetime.timedelta(minutes=delta)).strftime("%H:%M")
        mult = 1.1 + (base % 5000) / 1000.0
        return {"heure": h_new, "mult": mult}
    except: return None

# --- UI ---

st.markdown("<h1 style='text-align:center;'>🔐 TITAN V94 - ADMIN</h1>", unsafe_allow_html=True)
admin_input = st.text_input("Admin Code:", type="password", key="auth")

if admin_input == LOGIN_KEY:
    st.success("✅ Machine Online.")
    t1, t2, t3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR", "💣 MINES"])

    with t1:
        st.subheader("CosmosX Analysis")
        h_v = st.text_input("Hash:", key="h1")
        x_v = st.text_input("Hex:", key="x1")
        tr = st.number_input("Tour Actuel:", value=8137400)
        if st.button("🚀 SCAN COSMOS"):
            if h_v and x_v:
                for s in ["T1", "T2"]:
                    res = cosmos_ultra_engine(h_v, x_v, tr, s)
                    st.info(f"**{s}** | Target: Tour {res['tour']} | Jumps: {res['jumps']}")

    with t2:
        st.subheader("Aviator Studio")
        ah = st.text_input("Hex Value:", key="ah1")
        at = st.text_input("Heure (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"))
        if st.button("✈️ PREDICT"):
            for s in ["T1", "T2"]:
                res = aviator_studio_engine(ah, at, s)
                if res:
                    st.write(f"**{s}** at **{res['heure']}** -> Predict: **{res['mult']:.2f}x**")

    with t3:
        st.subheader("Mines Ultra V94")
        ms = st.text_input("Server Seed:", key="ms1")
        mc = st.text_input("Client Seed:", key="mc1")
        mn = st.text_input("Nonce:", key="mn1")
        
        # --- NY ISAN'NY MINE (1-3) ---
        m_count = st.radio("Nombre de mines amin'ny lalao:", [1, 2, 3], horizontal=True)
        
        if st.button("🛰️ SCAN MINES"):
            # Ny algorithm dia mbola mamoaka kintana 5 matanjaka foana ho fiarovana
            res_mines = mines_ultra_engine(ms, mc, mn, m_count)
            if res_mines:
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_star = i in res_mines
                    grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else ""}</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.success(f"Vokatra ho an'ny lalao misy mines {m_count}.")

elif admin_input != "":
    st.error("❌ Code diso.")
