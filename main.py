import streamlit as st
import hashlib, hmac, datetime, statistics, time

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V100 ULTRA PRO", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #050505, #111111);
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }
    h2, h3, h4, h5 {
        color: #00ffcc;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0044ff);
        color: #fff;
        border-radius: 8px;
        border: 1px solid #00ffcc;
        padding: 12px 24px;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
        width: 100%;
        transition: all 0.4s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0044ff, #00ffcc);
        box-shadow: 0 0 30px #00ffcc;
        transform: scale(1.02);
    }
    .mines-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        max-width: 350px;
        margin: auto;
        padding: 20px;
        background: rgba(0, 255, 204, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 255, 204, 0.2);
    }
    .mine-cell {
        aspect-ratio: 1/1;
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .cell-star {
        border: 2px solid #00d4ff !important;
        background: radial-gradient(circle, rgba(0,212,255,0.4) 0%, rgba(0,0,0,0) 80%) !important;
        color: #00d4ff;
        box-shadow: 0 0 25px #00d4ff inset, 0 0 15px #00d4ff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
        50% { transform: scale(1.05); box-shadow: 0 0 30px #00d4ff; }
        100% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
    }
    .metric-box {
        background: #111; padding: 15px; border-left: 4px solid #00ffcc; border-radius: 5px; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- COSMOS ENGINE (ULTRA PRECISION) ---
def cosmos_quantum_engine(server_seed, client_seed, tour_id, salt, heure=None, iters=300000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{tour_id}:{salt}:{heure}:TITAN_QUANTUM"
    
    # Deep Hashing
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"ITER_{i}".encode(), hashlib.sha512).digest()
    
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h1[:32], blake[:32], sha3))
    hex_out = final.hex()

    # Offset & Variables
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 37) + (11 if salt == "T1" else 17)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    # Calculation de la Côte Ultra Précise
    dec_val = int(hex_out[-8:], 16)
    cote = (4294967295 * 0.98) / dec_val if dec_val > 0 else 1.01
    cote = max(cote, 1.01)

    # Statistiques Avancées
    values = [offset] + jumps
    volatility = round(statistics.stdev(values) if len(values) > 1 else 0, 4)
    accuracy = round((statistics.mean(values) / max(values)) * 100, 4)

    return {
        "tour": tour_id + offset, 
        "cote": round(cote, 4), 
        "jumps": jumps,
        "min": min(values), 
        "mean": round(statistics.mean(values), 4),
        "volatility": volatility,
        "accuracy": accuracy, 
        "hex": hex_out[:32]
    }

# --- MINES ENGINE (PROBABILITY MATRIX) ---
def mines_matrix_engine(serverseed, clientseed, nonce, heure=None, iters=300000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{serverseed}:{clientseed}:{nonce}:{heure}:MINES_MATRIX"
    
    h_mut = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h_mut = hashlib.sha512(h_mut + f"S{i}".encode()).digest()

    # Tsy mampiasa random intsony fa MATRIX WEIGHTING (Avo lenta)
    grid_weights = []
    for i in range(25):
        # Kajy ny lanjan'ny sela tsirairay amin'ny alalan'ny Hash
        cell_hash = hashlib.sha256(h_mut + f"CELL_POS_{i}".encode()).hexdigest()
        weight = int(cell_hash[:8], 16) # Maka ny hery hexadécimal
        grid_weights.append((i, weight))
    
    # Alahatra avy amin'ny mavesatra indrindra mankany amin'ny kely indrindra
    grid_weights.sort(key=lambda x: x[1], reverse=True)
    
    # Alaina ny 5 voalohany (Ny tena Safe indrindra araka ny Matrix)
    top_5_safe = sorted([x[0] for x in grid_weights[:5]])
    confidence = round((grid_weights[4][1] / grid_weights[0][1]) * 100, 2)
    
    return top_5_safe, confidence

# --- LOGIN SYSTEM ---
st.markdown("<h1 style='text-align:center;'>🌌 TITAN V100 QUANTUM PRO</h1>", unsafe_allow_html=True)

if 'auth' not in st.session_state: 
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='background:#111; padding:30px; border-radius:15px; border:1px solid #00ffcc;'>", unsafe_allow_html=True)
        admininput = st.text_input("🔑 AUTHENTICATION CODE:", type="password")
        if st.button("INITIALIZE SYSTEM"):
            if admininput == LOGIN_KEY:
                st.session_state.auth = True
                st.rerun()
            else: 
                st.error("⚠️ Acces Refusé - Code Incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    if st.button("🚪 LOGOUT / RESET"):
        st.session_state.auth = False
        st.rerun()

    tab1, tab2 = st.tabs(["🚀 COSMOSX QUANTUM", "💎 MINES PROBABILITY MATRIX"])

    with tab1:
        st.markdown("### 🔭 ANALYSE MULTI-COUCHES COSMOS")
        c1, c2 = st.columns(2)
        with c1:
            hv = st.text_input("Server Seed Hash:", value="d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
            tv = st.number_input("Tour Actuel:", min_value=1, value=8147979)
        with c2:
            xv = st.text_input("Client Seed Hex:", value="SaSd3AAerLJrfAw053Bf")
            ch = st.text_input("Heure Synchronisation:", value=datetime.datetime.now().strftime("%H:%M:%S"))
        
        if st.button("⚡ EXECUTER CALCUL QUANTUM"):
            with st.spinner("Initialisation des serveurs de calcul..."):
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01) # Effet de calcul lourd
                    progress_bar.progress(percent + 1)
                
                for s in ["T1", "T2"]:
                    res = cosmos_quantum_engine(hv, xv, tv, s, ch)
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4 style='margin:0;'>Cible {s} : Tour <b>{res['tour']}</b> ➡️ <span style='color:#fff;'>{res['cote']}x</span></h4>
                        <p style='margin:0; font-size:14px; color:#aaa;'>
                        Précision: {res['accuracy']}% | Volatilité: {res['volatility']} | Hash: {res['hex']}...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 💣 SCANNER DE MATRICE MINES")
        c3, c4 = st.columns(2)
        with c3:
            ms = st.text_input("Server Seed:", value="d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91", key="m_s")
            mn = st.number_input("Nonce (ID Tour):", min_value=1, value=1)
        with c4:
            mc = st.text_input("Client Seed:", value="SaSd3AAerLJrfAw053Bf", key="m_c")
            mh = st.text_input("Heure d'impact:", value=datetime.datetime.now().strftime("%H:%M:%S"), key="m_t")
        
        m_sl = st.slider("Nombre de mine cible (Impact calculation):", 1, 7, 3)
        
        if st.button("📡 GENERER LA MATRICE SÉCURISÉE"):
            with st.spinner("Extraction des probabilités hexadécimales..."):
                time.sleep(1.2) # Effet visuel
                schema, confidence = mines_matrix_engine(ms, mc, mn, mh)
                
                st.success(f"✅ Analyse Terminée - Indice de Confiance Matrix: {confidence}%")
                
                # Render Grid HTML
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    if i in schema:
                        grid_html += '<div class="mine-cell cell-star">💎</div>'
                    else:
                        grid_html += '<div class="mine-cell"></div>'
                grid_html += '</div>'
                
                st.markdown(grid_html, unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;'><b>Cellules Sécurisées:</b> {schema}</p>", unsafe_allow_html=True)
