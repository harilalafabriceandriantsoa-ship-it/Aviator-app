import streamlit as st
import hashlib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import skew, kurtosis

st.set_page_config(page_title="MINES AI V6 HYBRID", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES AI V6 HYBRID ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
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

st.title("💎 MINES AI V6 HYBRID SYSTEM")

# ---------------- FEATURES ENGINE ----------------
def features(server, client, nonce):
    base = f"{server}:{client}:{nonce}".encode()
    h1 = hashlib.sha512(base).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    h4 = hashlib.sha256(h3).digest()
    arr = np.array(list(h4[:16]), dtype=np.float32)

    # Fanitsiana ny entropy
    prob_dist = arr / (np.sum(arr) + 1e-9)
    entropy = -np.sum(prob_dist * np.log(prob_dist + 1e-9))
    checksum = np.sum(arr) % 256

    return np.concatenate([arr, [entropy, checksum]])

# ---------------- MONTE CARLO ENGINE ----------------
def monte_carlo(server, client, nonce):
    arr = np.zeros(25)
    for i in range(5000):  
        # Fanitsiana ny fomba fanaovana hash
        h = hashlib.sha512(f"{server}:{client}:{nonce}:{i}".encode()).digest()
        arr[h[0] % 25] += 1
    return arr / np.sum(arr)

# ---------------- ML MODEL ----------------
def train_model():
    if len(st.session_state.memory) < 50:
        return None
    X = np.array([m[0] for m in st.session_state.memory])
    y = np.array([m[1] for m in st.session_state.memory])
    model = ExtraTreesClassifier(n_estimators=300, max_depth=16, random_state=42)
    model.fit(X, y)
    return model

# ---------------- ANALYSIS TOOLS ----------------
def confidence(prob):
    prob = np.clip(prob, 1e-9, 1)
    ent = -np.sum(prob * np.log(prob))
    jsd = jensenshannon(prob, np.ones(25)/25)
    var = np.var(prob)
    score = (1 - ent/np.log(25)) * 0.5 + (1 - jsd) * 0.3 + var*10
    return round(min(score, 1)*100, 2)

def draw_grid(safe, risky):
    html = "<div style='display:grid;grid-template-columns:repeat(5,60px);gap:10px;'>"
    for i in range(25):
        if i in safe:
            html += "<div style='background:#00ff99;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>💎</div>"
        elif i in risky:
            html += "<div style='background:#ff0033;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>☠️</div>"
        else:
            html += "<div style='background:#222;height:60px;border:1px solid #444;'></div>"
    html += "</div>"
    return html

# ---------------- INPUT INTERFACE ----------------
col_in1, col_in2 = st.columns(2)
with col_in1:
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
with col_in2:
    nonce = st.number_input("Nonce", value=1)
    mines_count = st.selectbox("MINES MODE", [1,2,3,4,5])

real_data_mode = st.checkbox("REAL DATA MODE (Manual Learning)")

# ---------------- EXECUTION ----------------
if st.button("SCAN MINES V6 HYBRID"):
    if not server or not client:
        st.error("Ampidiro ny Seeds azafady")
    else:
        mc = monte_carlo(server, client, nonce)
        model = train_model()
        ml = np.zeros(25)
        feat = features(server, client, nonce)

        if model:
            ml = model.predict_proba(feat.reshape(1, -1))[0]
            if len(ml) < 25: ml = np.pad(ml, (0, 25 - len(ml)))

        # Hybrid Weighting
        mem_size = len(st.session_state.memory)
        w_ml = min(0.5, mem_size / 1000) # Miakatra ny lanjan'ny ML arakaraka ny memory
        final = (1 - w_ml) * mc + w_ml * ml
        final /= np.sum(final)

        rank = np.argsort(-final)
        safe = list(map(int, rank[:mines_count]))
        risky = list(map(int, rank[-mines_count:]))
        conf = confidence(final)
        risk_score = round((1 - np.max(final)) * 100, 2)

        # Display Result
        st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("CONFIDENCE", f"{conf}%")
        c2.metric("RISK SCORE", f"{risk_score}%")
        c3.metric("MEMORY", mem_size)

        # Update Trends
        st.session_state.trend_conf.append(conf)
        st.session_state.trend_risk.append(risk_score)

        # Learning
        if real_data_mode:
            label = st.number_input("REAL RESULT INDEX (0-24)", 0, 24)
            if st.button("SAVE RESULT TO MEMORY"):
                st.session_state.memory.append((feat, label))
                st.success("Data saved!")
        else:
            st.session_state.memory.append((feat, int(np.argmax(mc))))

        # Charts
        st.subheader("📊 Probability Analysis")
        fig_final = go.Figure(data=[go.Bar(x=list(range(25)), y=final, marker_color='#00ff99')])
        st.plotly_chart(fig_final, use_container_width=True)

        if len(st.session_state.trend_conf) > 1:
            st.subheader("📈 Trends")
            fig_trend = px.line(y=st.session_state.trend_conf, title="Confidence Evolution")
            st.plotly_chart(fig_trend, use_container_width=True)
