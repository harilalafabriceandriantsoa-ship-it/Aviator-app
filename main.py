import streamlit as st
import hashlib, hmac
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon

st.set_page_config(page_title="MINES AI STABLE", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES AI STABLE ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")
else:

    st.title("💎 MINES AI STABLE SYSTEM")

    # ---------------- MEMORY ----------------
    if "memory" not in st.session_state:
        st.session_state.memory = []

    # ---------------- FEATURES ----------------
    def features(server, client, nonce):
        base = f"{server}:{client}:{nonce}".encode()
        h1 = hashlib.sha512(base).digest()
        h2 = hashlib.blake2b(h1).digest()
        h3 = hashlib.sha3_256(h2).digest()
        h4 = hashlib.sha256(h3).digest()
        arr = list(h4[:16])
        entropy = -sum([p/255*np.log((p/255)+1e-9) for p in arr])
        checksum = sum(arr) % 256
        return np.array(arr + [entropy, checksum], dtype=np.float32)

    # ---------------- MONTE CARLO ----------------
    def monte_carlo(server, client, nonce):
        arr = np.zeros(25)
        for i in range(1000):  # iteration betsaka kokoa
            h = hashlib.sha512(f"{server}:{client}:{nonce*i}".encode()).digest()
            arr[h[0] % 25] += 1
        return arr / np.sum(arr)

    # ---------------- TRAIN MODEL ----------------
    def train_model():
        if len(st.session_state.memory) < 40:
            return None
        X = np.array([m[0] for m in st.session_state.memory])
        y = np.array([m[1] for m in st.session_state.memory])
        model = ExtraTreesClassifier(
            n_estimators=300,
            max_depth=15,
            random_state=42
        )
        model.fit(X, y)
        return model

    # ---------------- CONFIDENCE ----------------
    def confidence(prob):
        prob = np.clip(prob, 1e-9, 1)
        entropy = -np.sum(prob * np.log(prob))
        jsd = jensenshannon(prob, np.ones(25)/25)
        score = (1 - entropy/np.log(25)) * 0.7 + (1 - jsd) * 0.3
        return round(score * 100, 2)

    # ---------------- CORE AI ----------------
    def predict(server, client, nonce, mines_count):
        mc = monte_carlo(server, client, nonce)
        model = train_model()
        ml = np.zeros(25)
        if model:
            ml = model.predict_proba(features(server, client, nonce).reshape(1, -1))[0]
            if len(ml) < 25:
                ml = np.pad(ml, (0, 25 - len(ml)))
        # dynamic weighting
        mem_size = len(st.session_state.memory)
        if mem_size < 100:
            final = 0.8 * mc + 0.2 * ml
        elif mem_size < 500:
            final = 0.6 * mc + 0.4 * ml
        else:
            final = 0.4 * mc + 0.6 * ml
        final = final / np.sum(final)
        rank = np.argsort(-final)
        safe = list(map(int, rank[:5]))
        risky = list(map(int, rank[-5:]))
        conf = confidence(final)
        # safe learning
        label = int(np.argmax(mc))
        st.session_state.memory.append((features(server, client, nonce), label))
        return safe, risky, conf

    # ---------------- GRID UI (UNCHANGED STYLE) ----------------
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

    # ---------------- INPUTS ----------------
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", value=1)
    mines_count = st.selectbox("MINES MODE", [1, 2, 3, 4, 5, 6, 7])  # ✅ 1–7

    # ---------------- RUN ----------------
    if st.button("SCAN MINES"):
        safe, risky, conf = predict(server, client, nonce, mines_count)
        st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)
        st.success(f"SAFE 💎: {safe}")
        st.error(f"RISK ☠️: {risky}")
        st.info(f"CONFIDENCE: {conf}%")
        st.write("📦 Memory size:", len(st.session_state.memory))
