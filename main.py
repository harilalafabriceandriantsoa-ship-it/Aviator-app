import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

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

# ---------------- COSMOS ----------------
def cosmos_ultra(server, client, nonce, ref):
    base = [crash(server, client, nonce+i) for i in range(30)]

    seed_val = int(hashlib.sha256(f"{server}{client}{nonce}".encode()).hexdigest(),16)
    rng = random.Random(seed_val)

    jumps = sorted(list(set([rng.randint(3,10) for _ in range(6)])))[:3]

    tours = []

    for i,j in enumerate(jumps):
        n2 = nonce + j
        future = [crash(server, client, n2+k) for k in range(12)]

        min_v = round(max(1.01, min(future)),2)
        avg_v = round(statistics.mean(future),2)
        max_v = round(max(future),2)

        variance = statistics.pvariance(future)
        acc = max(0, 100 - (variance*5))

        if min_v > ref:
            sig = "🟢 GO"
        elif avg_v > ref:
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

# ---------------- MINES GOD MODE ----------------
def mines_ai(server, client, nonce, mines_count):

    combined_scores = np.zeros(25)

    # 🔁 multi-nonce scan
    for offset in range(5):
        risk = monte_carlo(server, client, nonce+offset)
        combined_scores += (1-risk)

    combined_scores /= 5

    # 🧠 ML
    model = train_model()
    ml = np.zeros(25)
    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred]+=1

    # 📊 stability
    variance = np.var(combined_scores)
    stability = 1/(1+variance)

    # 🎯 final score
    final = combined_scores*0.6 + ml*0.2 + stability*0.2

    rank = np.argsort(-final)

    safe = rank[:5]
    risky = rank[-(5+mines_count)]

    best = safe[:2]

    confidence = round(np.mean(final[safe])*100 - (mines_count*5),2)

    st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

    return safe, risky, best, confidence

# ---------------- GRID ----------------
def draw_grid(safe, risky, best):
    html = "<div class='grid'>"
    for i in range(25):
        if i in list(best):
            html += "<div class='cell best'>⭐</div>"
        elif i in list(safe):
            html += "<div class='cell safe'>💎</div>"
        elif i in list(risky):
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- AUTO ----------------
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
st.title("🔥 HUBRIS V1000 GOD MODE")

tab1, tab2, tab3, tab4 = st.tabs(["🌌 COSMOS", "💎 MINES", "🤖 AUTO", "💬 CHAT"])

# COSMOS
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce",1)
    ref = st.number_input("Côte référence",2.0)

    if st.button("SCAN COSMOS"):
        res = cosmos_ultra(s,c,n,ref)
        for t in res:
            st.write(f"""
🎯 TOUR {t[0]} → {t[7]}
Nonce: {t[1]} (+{t[2]})
MIN: {t[3]} | AVG: {t[4]} | MAX: {t[5]}
ACCURACY: {t[6]}%
""")

# MINES
with tab2:
    s = st.text_input("Server",key="m1")
    c = st.text_input("Client",key="m2")
    n = st.number_input("Nonce",1,key="m3")
    mines_count = st.selectbox("Mines", [1,2,3])

    if st.button("SCAN MINES"):
        safe,risk,best,conf = mines_ai(s,c,n,mines_count)
        st.markdown(draw_grid(safe,risk,best),unsafe_allow_html=True)
        st.write("BEST ⭐:",list(best))
        st.write("SAFE 💎:",list(safe))
        st.write("CONFIDENCE:",conf,"%")

# AUTO
with tab3:
    conf = st.slider("Confidence",0,100,50)
    result = auto_bet(conf)
    st.write("RESULT:",result)
    st.write("BALANCE:",st.session_state.balance)

# CHAT
with tab4:
    msg = st.text_input("Message")
    if st.button("SEND"):
        if "play" in msg.lower():
            st.success("🟢 Good entry")
        else:
            st.warning("⚠️ Wait better signal")

st_autorefresh(interval=10000,limit=None)
