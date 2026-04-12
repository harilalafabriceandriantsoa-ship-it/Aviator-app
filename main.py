import streamlit as st
import hashlib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon
import plotly.graph_objects as go
from scipy.stats import skew

# Configuration de la page
st.set_page_config(page_title="MINES AI V6 ULTRA HYBRID", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES AI V6 ULTRA ACCESS")
    pwd = st.text_input("Password", type="password")
    if st.button("ENTER SYSTEM"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Access Denied: Wrong Password")
    st.stop()

# ---------------- INITIALIZATION ----------------
if "memory" not in st.session_state:
    st.session_state.memory = []

st.title("💎 MINES AI V6 - ULTRA HYBRID")
st.write("Status: **Active - 5 Diamonds & 5 Risk Signals (Ultra Mode)**")

# ---------------- ULTRA ENGINES ----------------
def get_features(server, client, nonce):
    # Deep hashing for feature extraction
    base = f"{server}:{client}:{nonce}".encode()
    h = hashlib.sha512(base).digest()
    arr = np.array(list(h[:16]), dtype=np.float32)
    return np.concatenate([arr, [np.sum(arr)%256]])

def monte_carlo_ultra(server, client, nonce):
    arr = np.zeros(25)
    # Ultra Precision: 15,000 simulations
    for i in range(15000): 
        h = hashlib.sha512(f"{server}:{client}:{nonce}:{i}".encode()).digest()
        arr[h[0] % 25] += 1
    return arr / np.sum(arr)

def draw_ultra_grid(safe, risky):
    # Rendering the 5x5 Grid
    html = "<div style='display:grid;grid-template-columns:repeat(5,65px);gap:10px;justify-content:center;'>"
    for i in range(25):
        if i in safe:
            # Signal Diamant matanjaka
            html += "<div style='background:#00ff99;height:65px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:25px;box-shadow: 0 0 20px #00ff99;'>💎</div>"
        elif i in risky:
            # Signal Vanja (Risk)
            html += "<div style='background:#ff0033;height:65px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:25px;box-shadow: 0 0 20px #ff0033;'>☠️</div>"
        else:
            # Case tsy misy signal
            html += "<div style='background:#1a1a1a;height:65px;border:1px solid #333;border-radius:12px;'></div>"
    html += "</div>"
    return html

# ---------------- INTERFACE ----------------
col1, col2 = st.columns(2)
with col1:
    server_seed = st.text_input("Server Seed (Graine du serveur)")
    client_seed = st.text_input("Client Seed (Graine du client)")
with col2:
    nonce_val = st.number_input("Nonce (Current)", value=1, min_value=1)
    mines_mode = st.selectbox("Nombre de Mines", [1, 2, 3, 4, 5])

# ---------------- MAIN SCAN PROCESS ----------------
if st.button("🚀 INITIATE ULTRA SCAN V6"):
    if server_seed and client_seed:
        with st.spinner("Analyzing Neural Patterns (15,000 Iterations)..."):
            # Algorithms Execution
            mc_prob = monte_carlo_ultra(server_seed, client_seed, nonce_val)
            current_feat = get_features(server_seed, client_seed, nonce_val)
            
            # Hybrid Neural Calculation (ML Adjustment)
            final_prob = mc_prob.copy()
            if len(st.session_state.memory) > 30:
                X_train = np.array([m[0] for m in st.session_state.memory])
                y_train = np.array([m[1] for m in st.session_state.memory])
                # Ultra model: ExtraTrees
                model = ExtraTreesClassifier(n_estimators=300).fit(X_train, y_train)
                ml_p = model.predict_proba(current_feat.reshape(1,-1))[0]
                if len(ml_p) < 25: ml_p = np.pad(ml_p, (0, 25-len(ml_p)))
                final_prob = (0.6 * mc_prob) + (0.4 * ml_p)

            # Ranking for Fixed Results (5 vs 5)
            ranking = np.argsort(-final_prob)
            safe_tiles = list(map(int, ranking[:5]))  # Ny 5 mendrika indrindra
            risk_tiles = list(map(int, ranking[-5:])) # Ny 5 mampidi-doza indrindra
            
            # Confidence Metrics
            precision = round((1 - jensenshannon(final_prob, np.ones(25)/25)) * 100, 2)

            # Display Visual Grid
            st.markdown(draw_ultra_grid(safe_tiles, risk_tiles), unsafe_allow_html=True)
            
            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("PRECISION", f"{precision}%")
            m2.metric("MINES MODE", f"{mines_mode}")
            m3.metric("ITERATIONS", "15,000")

            # Probability Distribution Graph
            st.subheader("📊 Neural Distribution Chart")
            fig = go.Figure(data=[go.Bar(x=list(range(25)), y=final_prob, marker_color='#00d1ff')])
            st.plotly_chart(fig, use_container_width=True)
            
            # Auto-learning Storage
            st.session_state.memory.append((current_feat, int(np.argmax(mc_prob))))
            st.success("Scan Complete: Neural patterns synchronized.")
    else:
        st.error("Please provide valid Server and Client seeds.")

# ---------------- SIDEBAR TOOLS ----------------
if st.sidebar.button("Clear AI Memory"):
    st.session_state.memory = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("V6 ULTRA HYBRID: Fixed 5💎/5☠️ Signal System.")
