import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V800 FULL AI", layout="wide")

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
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "memory" not in st.session_state:
    st.session_state.memory = []
if "balance" not in st.session_state:
    st.session_state.balance = 1000

# ---------------- HASH ----------------
def verify_hash(server, client, nonce):
    return hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

# ---------------- CRASH ----------------
def crash(server, client, nonce):
    h = verify_hash(server, client, nonce)
    dec = int(h[-8:],16) or 1
    return round((4294967295*0.97)/dec,2)

# ---------------- COSMOS AI ----------------
def analyse_crash_series(server, client, nonce):
    results = [crash(server, client, nonce+i) for i in range(20)]
    avg = round(statistics.mean(results),2)

    streak_low = 0
    for r in reversed(results):
        if r < 2:
            streak_low += 1
        else:
            break

    signal = "🔴 SKIP"
    if streak_low >= 4 and avg > 1.8:
        signal = "🟢 PLAY"

    return results, avg, streak_low, signal

# ---------------- COSMOS ENTRY ----------------
def cosmos_signals(series):
    signals = []
    for i in range(3):
        part = series[i*5:(i+1)*5]
        if sum(x<2 for x in part) > 3:
            signals.append("🔴")
        else:
            signals.append("🟢")
    return signals

# ---------------- MINES CORE ----------------
def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16],"big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

# ---------------- MONTE CARLO ----------------
def monte_carlo(server, client, nonce):
    scores = np.zeros(25)
    for i in range(200):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).digest()
        val = int.from_bytes(h[:2],"big") % 25
        scores[val]+=1
    return scores/200

# ---------------- FEATURES ----------------
def features(s,c,n):
    h = hashlib.sha256(f"{s}:{c}:{n}".encode()).hexdigest()
    return [int(h[i:i+2],16) for i in range(0,20,2)]

# ---------------- TRAIN ----------------
def train_model():
    if len(st.session_state.memory) < 30:
        return None

    X = [m[0] for m in st.session_state.memory]
    y = [m[1] for m in st.session_state.memory]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X,y)
    return model

# ---------------- MINES AI ----------------
def mines_ai(server, client, nonce):
    risk = monte_carlo(server, client, nonce)
    model = train_model()

    ml = np.zeros(25)

    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred]+=1

    final = (1-risk)*0.7 + ml*0.3
    rank = np.argsort(-final)

    safe5 = rank[:5]
    risky = rank[-5:]
    confidence = round(float(np.max(final)*100),2)

    # learning
    st.session_state.memory.append((features(server,client,nonce), int(safe5[0])))

    return safe5, risky, confidence

# ---------------- AUTO BET ----------------
def auto_bet(conf):
    bet = st.session_state.balance * 0.01

    if conf > 70:
        if random.random() > 0.5:
            st.session_state.balance += bet
            return "WIN"
        else:
            st.session_state.balance -= bet
            return "LOSE"
    return "SKIP"

# ---------------- GRID ----------------
def draw_grid(safe, risky):
    html = "<div class='grid'>"
    for i in range(25):
        if i in safe:
            html += "<div class='cell safe'>💎</div>"
        elif i in risky:
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS SECURE ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")

else:
    st.title("🔥 HUBRIS V800 FULL AI SYSTEM")

    tab1, tab2, tab3, tab4 = st.tabs(["🌌 COSMOS", "💎 MINES", "🤖 AUTO", "💬 CHAT"])

    # ---------------- COSMOS ----------------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", value=1)

        if st.button("SCAN COSMOS"):
            series, avg, streak, signal = analyse_crash_series(server, client, nonce)
            signals3 = cosmos_signals(series)

            st.success(f"GLOBAL: {signal}")
            st.write("3 SIGNAL:", signals3)
            st.write("AVG:", avg)

    # ---------------- MINES ----------------
    with tab2:
        server_m = st.text_input("Server", key="m1")
        client_m = st.text_input("Client", key="m2")
        nonce_m = st.number_input("Nonce", value=1, key="m3")

        if st.button("SCAN MINES"):
            safe, risky, conf = mines_ai(server_m, client_m, nonce_m)

            st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)
            st.success(f"SAFE 5 💎: {list(safe)}")
            st.error(f"RISKY ☠️: {list(risky)}")
            st.info(f"CONFIDENCE: {conf}%")

    # ---------------- AUTO ----------------
    with tab3:
        conf = st.slider("Confidence",0,100,50)
        result = auto_bet(conf)

        st.write("RESULT:", result)
        st.write("BALANCE:", st.session_state.balance)

    # ---------------- CHAT ----------------
    with tab4:
        msg = st.text_input("Message")

        if st.button("SEND"):
            if "play" in msg.lower():
                st.success("🟢 Good entry")
            else:
                st.warning("⚠️ Wait better signal")

    st_autorefresh(interval=10000, limit=None)
