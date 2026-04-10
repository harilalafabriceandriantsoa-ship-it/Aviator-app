import streamlit as st
import hashlib
import random
import statistics
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS V800 AI", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f0f0f,#1c1c1c);color:#00ffcc;}
h1,h2,h3{text-align:center;color:#00ffcc;}
.stButton>button {
    background: linear-gradient(90deg,#00ffcc,#0066ff);
    color:white;border-radius:10px;height:45px;
}
.grid {
    display:grid;
    grid-template-columns:repeat(5,60px);
    gap:10px;justify-content:center;margin-top:20px;
}
.cell {
    width:60px;height:60px;
    display:flex;align-items:center;justify-content:center;
    border-radius:10px;font-size:22px;
}
.safe {background:#00ffcc;color:#000;}
.risk {background:#ff0033;color:#fff;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "memory" not in st.session_state:
    st.session_state.memory = []

# ================= HASH =================
def verify_hash(server, client, nonce):
    return hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

# ================= CRASH (COSMOS CORE) =================
def crash(server, client, nonce):
    h = verify_hash(server, client, nonce)
    dec = int(h[-8:],16) or 1
    return round((4294967295*0.97)/dec,2)

# ================= COSMOS AI =================
def analyse_crash_series(server, client, nonce):
    results = [crash(server, client, nonce+i) for i in range(20)]
    avg = round(statistics.mean(results),2)

    streak_low = 0
    for r in reversed(results):
        if r < 2:
            streak_low += 1
        else:
            break

    signal = "SKIP"
    if streak_low >= 4 and avg > 1.8:
        signal = "PLAY"

    return results, avg, signal

# ================= FEATURES =================
def features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2],16) for i in range(0,20,2)]

# ================= TRAIN ML =================
def train_model():
    if len(st.session_state.memory) < 30:
        return None

    X = [m[0] for m in st.session_state.memory]
    y = [m[1] for m in st.session_state.memory]

    model = RandomForestClassifier(n_estimators=150)
    model.fit(X, y)
    return model

# ================= MINES AI (STRONG IA) =================
def mines_ai(server, client, nonce):
    feat = features(server, client, nonce)

    # Monte Carlo risk engine
    risk = np.zeros(25)
    for i in range(150):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        idx = int(h[:2],16) % 25
        risk[idx] += 1

    risk = risk / (np.max(risk) + 1e-9)

    # ML model
    model = train_model()
    ml = np.zeros(25)

    if model:
        try:
            pred = model.predict([feat])[0]
            ml[pred] = 1
        except:
            pass

    # AI fusion
    final = (1 - risk) * 0.75 + ml * 0.25

    rank = np.argsort(-final)

    safe5 = rank[:5]
    risky = rank[-5:]

    # confidence stable (normalization)
    confidence = float(np.clip(np.max(final) * 100, 0, 100))

    # learning (IMPORTANT)
    st.session_state.memory.append((feat, int(safe5[0])))

    return safe5, risky, confidence

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS V800 AI ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("WRONG PASSWORD")

    st.stop()

# ================= UI =================
st.title("🚀 HUBRIS V800 AI (ML STRONG CORE)")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES AI"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce", 1)

    if st.button("SCAN COSMOS"):
        series, avg, signal = analyse_crash_series(s, c, n)

        st.success(signal)
        st.write("AVG:", avg)
        st.write(series)

# ================= MINES =================
with tab2:
    s = st.text_input("Server", key="m1")
    c = st.text_input("Client", key="m2")
    n = st.number_input("Nonce", 1, key="m3")

    if st.button("SCAN MINES AI"):
        safe, risky, conf = mines_ai(s, c, n)

        st.write("💎 SAFE 5:", list(safe))
        st.write("☠️ RISK:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")
