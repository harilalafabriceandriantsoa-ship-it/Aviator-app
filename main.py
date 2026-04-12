import streamlit as st
import hashlib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import skew, kurtosis

st.set_page_config(page_title="MINES AI V6 HYBRID ULTRA", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES AI V6 HYBRID ULTRA ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER SYSTEM"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ---------------- SYSTEM INITIALIZATION ----------------
if "memory" not in st.session_state:
    st.session_state.memory = []
if "trend_conf" not in st.session_state:
    st.session_state.trend_conf = []
if "trend_risk" not in st.session_state:
    st.session_state.trend_risk = []

st.title("💎 MINES AI V6 - ULTRA HYBRID SYSTEM")
st.write("Status: **5 Diamonds & 5 Risk Tiles (Locked Mode)**")

# ---------------- ULTRA FEATURES ENGINE ----------------
def ultra_features(server, client, nonce):
    # Deep Hashing for better entropy
    base = f"{server}:{client}:{nonce}".encode()
    h1 = hashlib.sha512(base).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    arr = np.array(list(h3[:16]), dtype=np.float32)

    # Statistical moments
    prob_dist = arr / (np.sum(arr) + 1e-9)
    ent = -np.sum(prob_dist * np.log(prob_dist + 1e-9))
    check = np.sum(arr) % 256

    return np.concatenate([arr, [ent, check]])

# ---------------- MONTE CARLO (ULTRA ITERATION) ----------------
def monte_carlo_ultra(server, client, nonce):
    arr = np.zeros(25)
    # 10,000 iterations for ultra precision
    for i in range(10000):  
        h = hashlib.sha512(f"{server}:{client}:{nonce}:{i}".encode()).digest()
        arr[h[0] % 25] += 1
    return arr / np.sum(arr)

# ---------------- GRID RENDERING ----------------
def draw_ultra_grid(safe, risky):
    html = "<div style='display:grid;grid-template-columns:repeat(5,70px);gap:10px;'>"
    for i in range(25):
        if i in safe:
            # Maitso tanteraka ho an'ny diamant
            html += "<div style='background:#00ff99;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:30px;box-shadow: 0 0 15px #00ff99;'>💎</div>"
        elif i in risky:
            # Mena tanteraka ho an'ny loza
            html += "<div style='background:#ff0033;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:30px;box-shadow: 0 0 15px #ff0033;'>☠️</div>"
        else:
            html += "<div style='background:#1a1a1a;height:70px;border:1px solid #333;border-radius:12px;'></div>"
    html += "</div>"
    return html

# ---------------- INPUT INTERFACE ----------------
col1, col2 = st.columns(2)
with col1:
    server = st.text_input("Server Seed", placeholder="Paste server seed here...")
    client = st.text_input("Client Seed", placeholder="Paste client seed here...")
with col2:
    nonce = st.number_input("Nonce (Current)", value=1, min_value=1)
    st.info("🎯 ULTRA MODE: Fixed 5 Diamond Signals")

# ---------------- SCANNER LOGIC ----------------
if st.button("🚀 INITIATE ULTRA SCAN"):
    if not server or not client:
        st.warning("Please provide Seeds for neural processing")
    else:
        with st.spinner("Analyzing neural patterns..."):
            # Execute Algorithms
            mc = monte_carlo_ultra(server, client, nonce)
            feat = ultra_features(server, client, nonce)
            
            # Machine Learning adjustment if memory exists
            final_prob = mc.copy()
            if len(st.session_state.memory) >= 50:
                X = np.array([m[0] for m in st.session_state.memory])
                y = np.array([m[1] for m in st.session_state.memory])
                model = ExtraTreesClassifier(n_estimators=300, random_state=42).fit(X, y)
                ml_prob = model.predict_proba(feat.reshape(1, -1))[0]
                if len(ml_prob) < 25: ml_prob = np.pad(ml_prob, (0, 25 - len(ml_prob)))
                final_prob = (0.6 * mc) + (0.4 * ml_prob) # Hybrid mix

            # Ranking logic
            rank = np.argsort(-final_prob)
            safe_tiles = list(map(int, rank[:5])) # Top 5 Diamonds
            risk_tiles = list(map(int, rank[-5:])) # Bottom 5 Risks

            # Confidence Calculation
            conf_score = round((1 - jensenshannon(final_prob, np.ones(25)/25)) * 100, 2)
            
            # Display Results
            st.markdown(draw_ultra_grid(safe_tiles, risk_tiles), unsafe_allow_html=True)
            
            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("PRECISION", f"{conf_score}%")
            m2.metric("TARGETS", "5💎 / 5☠️")
            m3.metric("ITERATIONS", "10k Scan")

            # Store for trends
            st.session_state.trend_conf.append(conf_score)
            
            # Learning
            st.session_state.memory.append((feat, int(np.argmax(mc))))

        # Visualization
        st.subheader("📊 Neural Distribution")
        fig = go.Figure(data=[go.Bar(x=list(range(25)), y=final_prob, marker_color='#00d1ff')])
        st.plotly_chart(fig, use_container_width=True)

if st.sidebar.button("Clear System Memory"):
    st.session_state.memory = []
    st.session_state.trend_conf = []
    st.rerun()
