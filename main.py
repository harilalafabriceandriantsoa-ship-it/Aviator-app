import streamlit as st
import hashlib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon
import plotly.graph_objects as go

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
else:

    st.title("💎 MINES AI V6 HYBRID SYSTEM")

    # ---------------- MEMORY ----------------
    if "memory" not in st.session_state:
        st.session_state.memory = []

    if "real_data_mode" not in st.session_state:
        st.session_state.real_data_mode = False

    # ---------------- FEATURES ----------------
    def features(server, client, nonce):
        base = f"{server}:{client}:{nonce}".encode()
        h1 = hashlib.sha512(base).digest()
        h2 = hashlib.blake2b(h1).digest()
        h3 = hashlib.sha3_256(h2).digest()
        h4 = hashlib.sha256(h3).digest()
        arr = np.array(list(h4[:16]), dtype=np.float32)

        entropy = -np.sum((arr/255) * np.log((arr/255)+1e-9))
        checksum = np.sum(arr) % 256

        return np.concatenate([arr, [entropy, checksum]])

    # ---------------- MONTE CARLO ----------------
    def monte_carlo(server, client, nonce):
        arr = np.zeros(25)
        for i in range(700):
            h = hashlib.sha256(f"{server}:{client}:{nonce*i}".encode()).digest()
            arr[h[0] % 25] += 1
        return arr / np.sum(arr)

    # ---------------- MODEL ----------------
    def train_model():
        if len(st.session_state.memory) < 50:
            return None

        X = np.array([m[0] for m in st.session_state.memory])
        y = np.array([m[1] for m in st.session_state.memory])

        model = ExtraTreesClassifier(
            n_estimators=250,
            max_depth=14,
            random_state=42
        )
        model.fit(X, y)
        return model

    # ---------------- CONFIDENCE ----------------
    def confidence(prob):
        prob = np.clip(prob, 1e-9, 1)
        ent = -np.sum(prob * np.log(prob))
        jsd = jensenshannon(prob, np.ones(25)/25)
        return round(((1 - ent/np.log(25)) * 0.6 + (1 - jsd) * 0.4) * 100, 2)

    # ---------------- VISUAL FUNCTIONS ----------------
    def plot_bar(data, title):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(range(25)), y=data))
        fig.update_layout(title=title, height=300)
        return fig

    def draw_heatmap(prob):
        html = "<div style='display:grid;grid-template-columns:repeat(5,60px);gap:10px;'>"
        for i in range(25):
            val = prob[i]
            if val > 0.06:
                color = "#00ff99"
            elif val < 0.02:
                color = "#ff0033"
            else:
                color = "#ffaa00"

            html += f"<div style='background:{color};height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;font-size:11px;'>{round(val,3)}</div>"
        html += "</div>"
        return html

    # ---------------- CORE ENGINE ----------------
    def predict(server, client, nonce, mines_count):

        mc = monte_carlo(server, client, nonce)
        model = train_model()

        ml = np.zeros(25)
        feat = features(server, client, nonce)

        if model:
            ml = model.predict_proba(feat.reshape(1, -1))[0]
            if len(ml) < 25:
                ml = np.pad(ml, (0, 25 - len(ml)))

        # ---------------- ADAPTIVE FUSION ----------------
        mem = len(st.session_state.memory)

        if mem < 100:
            final = 0.75 * mc + 0.25 * ml
        elif mem < 500:
            final = 0.55 * mc + 0.45 * ml
        else:
            final = 0.4 * mc + 0.6 * ml

        final = final / np.sum(final)

        rank = np.argsort(-final)

        # ---------------- STYLE PRESERVED ----------------
        safe = list(map(int, rank[:5]))
        risky = list(map(int, rank[-5:]))

        conf = confidence(final)

        # ---------------- LEARNING ----------------
        if st.session_state.real_data_mode:
            label = st.number_input("REAL RESULT INDEX (0-24)", 0, 24, 0)
        else:
            label = int(np.argmax(mc))

        st.session_state.memory.append((feat, label))

        return safe, risky, conf, final, mc, ml

    # ---------------- GRID UI ----------------
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

    # ---------------- INPUT ----------------
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", value=1)

    mines_count = st.selectbox("MINES MODE", [1, 2, 3, 4, 5, 6, 7])
    st.session_state.real_data_mode = st.checkbox("REAL DATA MODE")

    # ---------------- RUN ----------------
    if st.button("SCAN MINES V6 HYBRID"):

        safe, risky, conf, final, mc, ml = predict(server, client, nonce, mines_count)

        # ORIGINAL GRID
        st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)

        st.success(f"SAFE 💎: {safe}")
        st.error(f"RISK ☠️: {risky}")
        st.info(f"CONFIDENCE: {conf}%")

        st.write("📦 Memory:", len(st.session_state.memory))

        # ---------------- VISUAL MODE ----------------
        st.subheader("📊 Monte Carlo")
        st.plotly_chart(plot_bar(mc, "Monte Carlo Distribution"))

        st.subheader("🤖 Machine Learning")
        st.plotly_chart(plot_bar(ml, "ML Prediction"))

        st.subheader("⚖️ Final Decision")
        st.plotly_chart(plot_bar(final, "Final AI Output"))

        st.subheader("🔥 AI Heatmap Vision")
        st.markdown(draw_heatmap(final), unsafe_allow_html=True)
