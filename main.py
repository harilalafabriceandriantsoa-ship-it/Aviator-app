import streamlit as st
import numpy as np
import hashlib
import sqlite3
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# ================== APP CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 AI CLEAN", layout="wide")
st.title("🚀 HUBRIS V700 CLEAN ARCHITECTURE AI SYSTEM")

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

def save_history(server, client, nonce, result):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?,?,?,?)",
              (server, client, nonce, str(result)))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history")
    data = c.fetchall()
    conn.close()
    return data

# ================== MINES CORE ==================
def mines_core(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    nums = [int(h[i:i+2], 16) % 25 for i in range(0, 50, 2)]

    seen = []
    for n in nums:
        if n not in seen:
            seen.append(n)
    return seen

# ================== COSMOS SIGNAL ==================
def cosmos_signal(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return np.array([int(h[i:i+2], 16) for i in range(0, 32, 2)]) / 255.0

# ================== RISK MODEL ==================
def risk_model(server, client, nonce):
    freq = np.zeros(25)

    for i in range(120):
        grid = mines_core(server, client, nonce + i)
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
        server, client, nonce, result = h

        try:
            mines = eval(result)
        except:
            mines = []

        label = mines[0] if len(mines) > 0 else 0

        X.append([len(server) % 10, len(client) % 10, int(nonce) % 10])
        y.append(label)

    if len(X) > 10:
        model.fit(X, y)

def ml_predict(server, client, nonce):
    return model.predict([[len(server) % 10,
                           len(client) % 10,
                           nonce % 10]])[0]

# ================== QUANT AI ==================
def quant_ai(server, client, nonce):
    risk = risk_model(server, client, nonce)
    ml = ml_predict(server, client, nonce)

    scores = []

    for i in range(25):
        score = (1 - risk[i]) * 0.7

        if i == ml:
            score += 0.2

        scores.append((i, score))

    return sorted(scores, key=lambda x: x[1], reverse=True), risk

# ================== ACCURACY ==================
def accuracy(predicted, real):
    if len(real) == 0:
        return 0

    hit = len(set(predicted[:5]) & set(real[:5]))
    return hit / 5

# ================== LOAD HISTORY ==================
history = load_history()
train_model(history)

# ================== INPUT ==================
server = st.text_input("Server Seed")
client = st.text_input("Client Seed")
nonce = st.number_input("Nonce", 1)

# ================== RUN SYSTEM ==================
if st.button("🚀 RUN HUBRIS AI"):

    mines = mines_core(server, client, nonce)
    ranked, risk = quant_ai(server, client, nonce)
    diamonds = top5_diamonds(risk)
    cosmos = cosmos_signal(server, client, nonce)

    save_history(server, client, nonce, mines)

    acc = accuracy(diamonds, mines)

    # ================== OUTPUT ==================
    st.subheader("💣 MINES RESULT")
    st.write(mines)

    st.subheader("💎 TOP 5 DIAMONDS")
    st.write(diamonds)

    st.subheader("📊 QUANT RANKING")
    st.write(ranked[:10])

    st.subheader("🌌 COSMOS SIGNAL")
    st.write(cosmos)

    st.subheader("📈 ACCURACY ESTIMATION")
    st.write(f"{acc * 100:.2f}%")

    st.subheader("⚠️ RISK MAP")
    st.bar_chart(risk)

# ================== HISTORY ==================
st.markdown("---")
st.subheader("🧠 LEARNING HISTORY (LAST 10)")

for h in history[-10:]:
    st.write(h)
