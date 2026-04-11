import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V900 FINAL", layout="wide")

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
if "memory" not in st.session_state:
    st.session_state.memory = []
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐 HUBRIS SECURE ACCESS")
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

# ---------------- COSMOS ULTRA ----------------
def cosmos_ultra(server, client, nonce, ref=2.0):
    base = [crash(server, client, nonce+i) for i in range(30)]

    avg = statistics.mean(base)
    var = statistics.pvariance(base)

    seed_val = int(hashlib.sha256(f"{server}{client}{nonce}".encode()).hexdigest(),16)
    rng = random.Random(seed_val)

    jumps = list(set([max(2,int(avg)+rng.randint(2,6)) for _ in range(6)]))[:3]

    tours = []

    for i,j in enumerate(jumps):
        n2 = nonce + j
        future = [crash(server, client, n2+k) for k in range(10)]

        min_v = round(max(1.01, min(future)),2)
        avg_v = round(statistics.mean(future),2)
        max_v = round(max(future),2)

        variance = statistics.pvariance(future)
        acc = max(0, 100 - variance)

        if acc > 80 and avg_v > ref:
            sig = "🟢 GO"
        elif acc > 60:
            sig = "🟡 WAIT"
        else:
            sig = "🔴 SKIP"

        tours.append((i+1,n2,j,min_v,avg_v,max_v,round(acc,2),sig))

    return tours

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

# ---------------- MINES AI (FIX 5 DIAMOND) ----------------
def mines_ai(server, client, nonce):
    risk = monte_carlo(server, client, nonce)
    model = train_model()

    ml = np.zeros(25)

    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred]+=1

    final = (1-risk)*0.7 + ml*0.3
    rank = np.argsort(-final)

    safe = rank[:5]          # ✅ TOUJOURS 5 DIAMANTS
    risky = rank[-5:]

    confidence = round(float(np.mean(final[safe]) * 100),2)

    st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

    return safe, risky, confidence

# ---------------- GRID ----------------
def draw_grid(safe, risky):
    html = "<div class='grid'>"
    for i in range(25):
        if i in list(safe):
            html += "<div class='cell safe'>💎</div>"
        elif i in list(risky):
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- UI ----------------
st.title("🔥 HUBRIS V900 FINAL SYSTEM")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES"])

# ---------------- COSMOS ----------------
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce",1)

    if st.button("SCAN COSMOS"):
        res = cosmos_ultra(s,c,n)
        for t in res:
            st.write(f"""
🎯 TOUR {t[0]} → {t[7]}
Nonce: {t[1]} (+{t[2]})
MIN: {t[3]} | AVG: {t[4]} | MAX: {t[5]}
ACCURACY: {t[6]}%
""")

# ---------------- MINES ----------------
with tab2:
    s = st.text_input("Server",key="m1")
    c = st.text_input("Client",key="m2")
    n = st.number_input("Nonce",1,key="m3")

    if st.button("SCAN MINES"):
        safe,risk,conf = mines_ai(s,c,n)
        st.markdown(draw_grid(safe,risk),unsafe_allow_html=True)
        st.write("SAFE 💎:",list(safe))
        st.write("RISK ☠️:",list(risk))
        st.write("CONFIDENCE:",conf,"%")

st_autorefresh(interval=10000,limit=None)
