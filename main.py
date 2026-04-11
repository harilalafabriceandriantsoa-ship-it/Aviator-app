import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V900 GOD MODE", layout="wide")

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

# ================= COSMOS ULTRA =================
def cosmos_ultra(server, client, nonce, ref=2.0):
    base_series = [crash(server, client, nonce+i) for i in range(30)]

    avg = statistics.mean(base_series)
    var = statistics.pvariance(base_series)

    streak_low = 0
    for r in reversed(base_series):
        if r < ref:
            streak_low += 1
        else:
            break

    seed_val = int(hashlib.sha256(f"{server}{client}{nonce}".encode()).hexdigest(),16)
    rng = random.Random(seed_val)

    jumps = []
    used = set()

    while len(jumps) < 3:
        base_jump = int((avg + streak_low + (var % 5)))
        jump = max(2, base_jump + rng.randint(1,5))
        if jump not in used:
            jumps.append(jump)
            used.add(jump)

    tours = []

    for idx, j in enumerate(jumps):
        t_nonce = nonce + j
        future = [crash(server, client, t_nonce + k) for k in range(10)]

        min_v = round(min(future),2)
        avg_v = round(statistics.mean(future),2)
        max_v = round(max(future),2)

        variance = statistics.pvariance(future)
        acc = max(0, 100 - variance)

        if acc >= 80 and avg_v > ref:
            sig = "🟢 GO"
        elif acc >= 60:
            sig = "🟡 WAIT"
        else:
            sig = "🔴 SKIP"

        tours.append({
            "tour": idx+1,
            "nonce": t_nonce,
            "jump": j,
            "min": min_v,
            "avg": avg_v,
            "max": max_v,
            "acc": round(acc,2),
            "signal": sig
        })

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

# ---------------- MINES AI ----------------
def mines_ai_multi(server, client, nonce, mines_count):
    risk = monte_carlo(server, client, nonce)
    model = train_model()

    ml = np.zeros(25)

    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred]+=1

    final = (1-risk)*0.7 + ml*0.3
    rank = np.argsort(-final)

    safe = rank[:(5-mines_count)]
    risky = rank[-(5+mines_count)]

    confidence = round(float(np.max(final)*100 - mines_count*5),2)

    st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

    return safe, risky, confidence

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
    st.title("🔥 HUBRIS V900 GOD MODE")

    tab1, tab2, tab3, tab4 = st.tabs(["🌌 COSMOS", "💎 MINES", "🤖 AUTO", "💬 CHAT"])

    # ---------------- COSMOS ----------------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", value=1)

        if st.button("SCAN COSMOS"):
            tours = cosmos_ultra(server, client, nonce)

            for t in tours:
                st.markdown(f"""
                <div style='background:#111;padding:15px;border-radius:12px;
                            border:1px solid #00ffcc;margin-bottom:10px'>
                    <h3>🎯 TOUR {t['tour']} → {t['signal']}</h3>
                    <p>Nonce: {t['nonce']} (+{t['jump']})</p>
                    <p>MIN: {t['min']} | AVG: {t['avg']} | MAX: {t['max']}</p>
                    <p>ACCURACY: {t['acc']}%</p>
                </div>
                """, unsafe_allow_html=True)

    # ---------------- MINES ----------------
    with tab2:
        server_m = st.text_input("Server", key="m1")
        client_m = st.text_input("Client", key="m2")
        nonce_m = st.number_input("Nonce", value=1, key="m3")

        mines_count = st.selectbox("Nombre de mines", [1,2,3])

        if st.button("SCAN MINES"):
            safe, risky, conf = mines_ai_multi(server_m, client_m, nonce_m, mines_count)

            st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)
            st.success(f"SAFE 💎: {list(safe)}")
            st.error(f"RISK ☠️: {list(risky)}")
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
