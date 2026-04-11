import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS V800 AI CLEAN", layout="wide")

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
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "login" not in st.session_state:
    st.session_state.login = False

# ================= HASH =================
def verify_hash(server, client, nonce):
    return hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

# ================= CRASH =================
def crash(server, client, nonce):
    h = verify_hash(server, client, nonce)
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

# ================= COSMOS =================
def analyse_crash_series(server, client, nonce):
    series = [crash(server, client, nonce+i) for i in range(20)]

    avg = float(np.mean(series))
    var = float(np.var(series))

    streak = 0
    for x in reversed(series):
        if x < 2:
            streak += 1
        else:
            break

    score = min(100, max(0, (avg * 10) + (streak * 5) - var))

    if score >= 80:
        signal = "🟢 PLAY"
    elif score >= 60:
        signal = "🟡 WAIT"
    else:
        signal = "🔴 SKIP"

    return series, avg, var, streak, score, signal

# ================= FEATURES =================
def features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return np.array([int(h[i:i+2], 16) for i in range(0, 20, 2)])

# ================= ML TRAIN =================
def train_model():
    if len(st.session_state.memory) < 30:
        return None

    X = np.array([m[0] for m in st.session_state.memory])
    y = np.array([m[1] for m in st.session_state.memory])

    if len(set(y)) < 2:
        return None

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# ================= MINES AI =================
def mines_ai(server, client, nonce):
    feat = features(server, client, nonce)

    risk = np.zeros(25)
    for i in range(150):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        idx = int(h[:2], 16) % 25
        risk[idx] += 1

    risk = risk / (np.max(risk) + 1e-9)

    model = train_model()
    ml = np.zeros(25)

    if model is not None:
        try:
            pred = int(model.predict([feat])[0])
            if 0 <= pred < 25:
                ml[pred] = 1
        except:
            pass

    final = (1 - risk) * 0.75 + ml * 0.25
    rank = np.argsort(-final)

    safe5 = rank[:5]
    risky = rank[-5:]
    confidence = float(np.clip(np.max(final) * 100, 0, 100))

    # learning safe
    st.session_state.memory.append((feat, int(safe5[0])))

    return safe5, risky, confidence

# ================= LOGIN =================
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
st.title("🚀 HUBRIS V800 AI (CLEAN ZERO ERROR VERSION)")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES AI"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce", 1)

    if st.button("SCAN COSMOS"):
        series, avg, var, streak, score, signal = analyse_crash_series(s, c, n)

        st.success(signal)
        st.write("Series:", series)
        st.write("AVG:", avg)
        st.write("VAR:", var)
        st.write("STREAK:", streak)
        st.progress(int(score))

# ================= MINES =================
with tab2:
    s = st.text_input("Server", key="m1")
    c = st.text_input("Client", key="m2")
    n = st.number_input("Nonce", 1, key="m3")

    if st.button("SCAN MINES AI"):
        safe, risky, conf = mines_ai(s, c, n)

        st.write("💎 SAFE:", list(safe))
        st.write("☠️ RISK:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")

st_autorefresh(interval=10000, limit=None)
