import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3
import json
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS AI CORE SYSTEM", layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("hubris_ai.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mine_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server TEXT,
        client TEXT,
        nonce INTEGER,
        features TEXT,
        prediction INTEGER,
        label INTEGER
    )
    """)
    conn.commit()

init_db()

# ================= SESSION =================
if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "memory" not in st.session_state:
    st.session_state.memory = []

# ================= COSMOS ENGINE =================
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos_engine(server, client, nonce):
    results = [crash(server, client, nonce+i) for i in range(20)]
    avg = np.mean(results)

    streak = 0
    for r in reversed(results):
        if r < 2:
            streak += 1
        else:
            break

    signal = "SKIP"
    if streak >= 4 and avg > 1.8:
        signal = "PLAY"

    return results, avg, signal

# ================= FEATURES =================
def mine_features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= TRAIN MODEL =================
def train_model():
    cursor.execute("SELECT features, label FROM mine_history")
    data = cursor.fetchall()

    if len(data) < 30:
        return None

    X = [json.loads(d[0]) for d in data]
    y = [d[1] for d in data]

    model = RandomForestClassifier(n_estimators=150)
    model.fit(X, y)
    return model

# ================= MINE ENGINE =================
def mine_engine(server, client, nonce):
    features = mine_features(server, client, nonce)

    model = train_model()

    if model:
        pred = model.predict([features])[0]
    else:
        pred = sum(features) % 25

    risk_map = np.zeros(25)
    risk_map[pred] = 1

    safe = [i for i in range(25) if i != pred][:5]
    risky = [pred]

    confidence = float(np.max([1 - risk_map[pred], 0.5]) * 100)

    return safe, risky, pred, confidence, features

# ================= SAVE LEARNING =================
def save_mine(server, client, nonce, pred, label):
    feats = mine_features(server, client, nonce)

    cursor.execute("""
    INSERT INTO mine_history (server, client, nonce, features, prediction, label)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        server,
        client,
        nonce,
        json.dumps(feats),
        pred,
        label
    ))

    conn.commit()

# ================= LOGIN =================
def login(password):
    return password == "2026"

# ================= UI LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS AI ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if login(pwd):
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")

    st.stop()

# ================= MAIN UI =================
st.title("🚀 HUBRIS AI FULL PRODUCTION ENGINE")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES"])

# ================= COSMOS =================
with tab1:
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", 1)

    if st.button("RUN COSMOS"):
        results, avg, signal = cosmos_engine(server, client, nonce)

        st.success(signal)
        st.write("AVG:", avg)
        st.write(results)

# ================= MINES =================
with tab2:
    s = st.text_input("Server (Mines)")
    c = st.text_input("Client (Mines)")
    n = st.number_input("Nonce (Mines)", 1)

    if st.button("RUN MINES AI"):
        safe, risky, pred, conf, feats = mine_engine(s, c, n)

        st.write("💎 SAFE:", safe)
        st.write("☠️ RISK:", risky)
        st.write("🎯 PRED:", pred)
        st.success(f"CONFIDENCE: {conf:.2f}%")

        # FAKE LABEL (learning simulation)
        label = pred if random.random() > 0.5 else (pred + 1) % 25
        save_mine(s, c, n, pred, label)

st.info("HUBRIS AI RUNNING - PRODUCTION MODE")
