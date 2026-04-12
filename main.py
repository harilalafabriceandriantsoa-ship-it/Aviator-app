import streamlit as st
import hashlib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon
import plotly.graph_objects as go

st.set_page_config(page_title="MINES AI V7 SAFE EDGE", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES AI V7 SAFE EDGE ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ---------------- INIT ----------------
if "memory" not in st.session_state:
    st.session_state.memory = []

if "model" not in st.session_state:
    st.session_state.model = None

st.title("💎 MINES AI V7 - SAFE EDGE SYSTEM")

# ---------------- FEATURES ----------------
def features(server, client, nonce):
    base = f"{server}:{client}:{nonce}".encode()
    h = hashlib.sha512(base).digest()
    arr = np.array(list(h[:16]), dtype=np.float32)
    return np.concatenate([arr, [np.sum(arr) % 256]])

# ---------------- MONTE CARLO ----------------
def monte_carlo(server, client, nonce):
    arr = np.zeros(25)
    for i in range(500):
        h = hashlib.sha256(f"{server}:{client}:{nonce*i}".encode()).digest()
        arr[h[0] % 25] += 1
    return arr / np.sum(arr)

# ---------------- EDGE FILTER ----------------
def edge_score(p):
    return np.max(p) - np.mean(p)

def volatility(p):
    return np.std(p)

def allow_trade(p):
    if np.max(p) < 0.06:
        return False, "LOW SIGNAL"
    if edge_score(p) < 0.015:
        return False, "NO EDGE"
    if volatility(p) < 0.005:
        return False, "FLAT MARKET"
    return True, "OK"

# ---------------- MODEL TRAIN ----------------
def train_model():
    if len(st.session_state.memory) < 40:
        return None

    X = np.array([m[0] for m in st.session_state.memory])
    y = np.array([m[1] for m in st.session_state.memory])

    model = ExtraTreesClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )
    model.fit(X, y)
    return model

# ---------------- CONFIDENCE ----------------
def confidence(p):
    p = np.clip(p, 1e-9, 1)
    ent = -np.sum(p * np.log(p))
    jsd = jensenshannon(p, np.ones(25)/25)
    return round(((1 - ent/np.log(25)) * 0.6 + (1 - jsd) * 0.4) * 100, 2)

# ---------------- VISUAL ----------------
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

def plot_bar(data, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(25)), y=data))
    fig.update_layout(title=title, height=300)
    return fig

# ---------------- INPUT ----------------
server = st.text_input("Server Seed")
client = st.text_input("Client Seed")
nonce = st.number_input("Nonce", value=1)

# ---------------- RUN ----------------
if st.button("SCAN MINES V7 SAFE EDGE"):

    mc = monte_carlo(server, client, nonce)
    feat = features(server, client, nonce)

    model = train_model()

    ml = np.zeros(25)
    if model:
        ml = model.predict_proba(feat.reshape(1, -1))[0]
        if len(ml) < 25:
            ml = np.pad(ml, (0, 25-len(ml)))

    # FUSION
    final = 0.6 * mc + 0.4 * ml
    final = final / np.sum(final)

    # EDGE CHECK
    ok, reason = allow_trade(final)

    rank = np.argsort(-final)
    safe = list(map(int, rank[:5]))
    risky = list(map(int, rank[-5:]))

    conf = confidence(final)

    # MEMORY (FIXED - no fake label)
    st.session_state.memory.append((feat, np.argmax(final)))

    # OUTPUT
    if not ok:
        st.error(f"🛑 SKIP ROUND: {reason}")
    else:
        st.success("✅ PLAY SIGNAL DETECTED")

        st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)

        st.success(f"SAFE 💎: {safe}")
        st.error(f"RISK ☠️: {risky}")
        st.info(f"CONFIDENCE: {conf}%")

    st.write("📦 Memory:", len(st.session_state.memory))

    # VISUAL
    st.subheader("📊 Distribution")
    st.plotly_chart(plot_bar(final, "FINAL PROBABILITY"))
