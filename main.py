import streamlit as st
import numpy as np
import hashlib
import sqlite3
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# ================== APP ==================
st.set_page_config(page_title="HUBRIS V700 REAL ACCURACY AI", layout="wide")
st.title("🚀 HUBRIS V700 REAL ACCURACY AI + LEARNING SYSTEM")

# ================== DATABASE ==================
def init_db():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        server TEXT,
        client TEXT,
        nonce INTEGER,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

def save_history(s,c,n,res):
    conn = sqlite3.connect("hubris.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO history VALUES (?,?,?,?)",(s,c,n,str(res)))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("hubris.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")
    data = cur.fetchall()
    conn.close()
    return data

# ================== MINES CORE ==================
def mines_core(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    nums = [int(h[i:i+2],16)%25 for i in range(0,50,2)]

    seen=[]
    for n in nums:
        if n not in seen:
            seen.append(n)
    return seen

# ================== COSMOS ==================
def cosmos_signal(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return np.array([int(h[i:i+2],16) for i in range(0,32,2)]) / 255

# ================== RISK MODEL ==================
def risk_model(server, client, nonce):
    freq = np.zeros(25)

    for i in range(120):
        grid = mines_core(server, client, nonce+i)
        for g in grid:
            freq[g] += 1

    return freq / np.max(freq)

# ================== DIAMONDS ==================
def top5_diamonds(risk):
    return np.argsort(risk)[:5]

# ================== ML MODEL ==================
model = RandomForestClassifier(n_estimators=80)

def train_model(history):
    X, y = [], []

    for h in history:
        s, c, n, res = h

        mines = eval(res) if "[" in res else []

        label = mines[0] if len(mines)>0 else 0

        X.append([len(s)%10, len(c)%10, int(n)%10])
        y.append(label)

    if len(X) > 10:
        model.fit(X,y)

def ml_predict(server, client, nonce):
    return model.predict([[len(server)%10, len(client)%10, nonce%10]])[0]

# ================== ACCURACY ENGINE ==================
def accuracy_score(predicted, real):
    if len(real) == 0:
        return 0

    hit = len(set(predicted[:5]) & set(real[:5]))
    return hit / 5

# ================== QUANT AI ==================
def quant_ai(server, client, nonce):
    risk = risk_model(server, client, nonce)
    ml = ml_predict(server, client, nonce)

    score = []

    for i in range(25):
        val = (1-risk[i])*0.7
        if i == ml:
            val += 0.2
        score.append((i,val))

    return sorted(score, key=lambda x: x[1], reverse=True), risk

# ================== INPUT ==================
server = st.text_input("Server Seed")
client = st.text_input("Client Seed")
nonce = st.number_input("Nonce",1)

# ================== LOAD HISTORY ==================
history = load_history()

# ================== TRAIN ==================
train_model(history)

# ================== RUN ==================
if st.button("🚀 RUN AI + LEARN + ACCURACY"):

    mines = mines_core(server,client,nonce)
    ranked, risk = quant_ai(server,client,nonce)
    diamonds = top5_diamonds(risk)

    # save history
    save_history(server,client,nonce,mines)

    # accuracy estimation (self-check style)
    acc = accuracy_score(diamonds, mines)

    cosmos = cosmos_signal(server,client,nonce)

    # ================== OUTPUT ==================
    st.subheader("💣 MINES RESULT")
    st.write(mines)

    st.subheader("💎 DIAMONDS (TOP 5)")
    st.write(diamonds)

    st.subheader("📊 QUANT RANKING")
    st.write(ranked[:10])

    st.subheader("🌌 COSMOS SIGNAL")
    st.write(cosmos)

    st.subheader("📈 ACCURACY ESTIMATION")
    st.write(f"{acc*100:.2f}%")

    st.subheader("⚠️ RISK MAP")
    st.bar_chart(risk)

# ================== HISTORY ==================
st.markdown("---")
st.subheader("🧠 LEARNING HISTORY")

for h in history[-10:]:
    st.write(h)
