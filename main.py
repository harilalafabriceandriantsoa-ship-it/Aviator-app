import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V1000 GOD MODE", layout="wide")

# ---------------- STYLE ----------------
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
.best {background:#ffff00;color:#000;font-weight:bold;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "memory" not in st.session_state:
    st.session_state.memory = []
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐 HUBRIS ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ---------------- HASH ----------------
def verify_hash(server, client, nonce):
    return hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

# ---------------- CRASH ----------------
def crash(server, client, nonce):
    h = verify_hash(server, client, nonce)
    dec = int(h[-8:],16) or 1
    return round((4294967295*0.97)/dec,2)

# ---------------- FEATURES ----------------
def features(s,c,n):
    h = hashlib.sha256(f"{s}:{c}:{n}".encode()).hexdigest()
    return [int(h[i:i+2],16) for i in range(0,20,2)]

# ---------------- TRAIN MODEL ----------------
def train_model():
    if len(st.session_state.memory) < 30:
        return None
    X = [m[0] for m in st.session_state.memory]
    y = [m[1] for m in st.session_state.memory]
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X,y)
    return model

# ---------------- MONTE CARLO ----------------
def monte_carlo(server, client, nonce):
    scores = np.zeros(25)
    for i in range(150):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).digest()
        idx = int(h[:2],16) % 25
        scores[idx] += 1
    return scores / np.max(scores)

# ---------------- MINES AI (FIXED) ----------------
def mines_ai(server, client, nonce, mines_count):

    risk = monte_carlo(server, client, nonce)

    model = train_model()
    ml = np.zeros(25)

    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred] = 1

    final = (1 - risk)*0.7 + ml*0.3

    rank = np.argsort(-final)

    safe = rank[:5]

    # ✅ FIXED (IMPORTANT)
    risky = rank[-5:]

    best = safe[:2]

    confidence = round(np.mean(final[safe]) * 100, 2)

    st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

    return safe, risky, best, confidence

# ---------------- GRID ----------------
def draw_grid(safe, risky, best):

    safe = list(safe)
    risky = list(risky)
    best = list(best)

    html = "<div class='grid'>"

    for i in range(25):
        if i in best:
            html += "<div class='cell best'>⭐</div>"
        elif i in safe:
            html += "<div class='cell safe'>💎</div>"
        elif i in risky:
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"

    html += "</div>"
    return html

# ---------------- AUTO BET ----------------
def auto_bet(conf):
    bet = st.session_state.balance * 0.01

    if conf > 75:
        if random.random() > 0.5:
            st.session_state.balance += bet
            return "WIN"
        else:
            st.session_state.balance -= bet
            return "LOSE"
    return "SKIP"

# ---------------- UI ----------------
st.title("🔥 HUBRIS V1000 GOD MODE (STABLE FIXED)")

tab1, tab2, tab3 = st.tabs(["💎 MINES", "🤖 AUTO", "💬 CHAT"])

# ---------------- MINES ----------------
with tab1:
    s = st.text_input("Server")
    c = st.text_input("Client")
    n = st.number_input("Nonce", 1)
    mines_count = st.selectbox("Mines", [1,2,3])

    if st.button("SCAN MINES"):
        safe, risky, best, conf = mines_ai(s,c,n,mines_count)

        st.markdown(draw_grid(safe,risky,best), unsafe_allow_html=True)

        st.write("BEST ⭐:", list(best))
        st.write("SAFE 💎:", list(safe))
        st.write("RISK ☠️:", list(risky))
        st.success(f"CONFIDENCE: {conf}%")

# ---------------- AUTO ----------------
with tab2:
    conf = st.slider("Confidence",0,100,50)
    result = auto_bet(conf)

    st.write("RESULT:", result)
    st.write("BALANCE:", st.session_state.balance)

# ---------------- CHAT ----------------
with tab3:
    msg = st.text_input("Message")

    if st.button("SEND"):
        if "play" in msg.lower():
            st.success("🟢 Good signal")
        else:
            st.warning("⚠️ Wait signal")
