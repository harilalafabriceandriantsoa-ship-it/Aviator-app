# ================== IMPORTS ==================
import streamlit as st
import sqlite3
import hashlib
import numpy as np
import random
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

# ================== CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 PRO AI", layout="wide")

# ================== DB ==================
def init_db():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        user TEXT,
        message TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        features TEXT,
        label INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================== SECURITY ==================
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register(u,p,role="user"):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?,?,?)",
              (u, hash_pw(p), role))
    conn.commit()
    conn.close()

def login(u,p):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?",
              (u, hash_pw(p)))
    r = c.fetchone()
    conn.close()
    return r[0] if r else None

# ================== CHAT ==================
def send_msg(u,msg):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT INTO chat VALUES (?,?)",(u,msg))
    conn.commit()
    conn.close()

def get_msgs():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT * FROM chat")
    r = c.fetchall()
    conn.close()
    return r

# ================== MINES (PRESERVED) ==================
def mines_core(server, client, nonce):
    base = f"{server}:{client}:{nonce}"
    h = hashlib.sha256(base.encode()).hexdigest()

    nums = [int(h[i:i+2],16)%25 for i in range(0,50,2)]

    seen = []
    for n in nums:
        if n not in seen:
            seen.append(n)
    return seen

# ================== COSMOS (PRESERVED) ==================
def cosmos_signal(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return np.array([int(h[i:i+2],16) for i in range(0,32,2)]) / 255

# ================== ML MODEL ==================
model = RandomForestClassifier(n_estimators=50)

def train_model():
    # fake training dataset (simulation learning layer)
    X = []
    y = []

    for i in range(300):
        server = random.randint(1,100)
        client = random.randint(1,100)
        nonce = random.randint(1,100)

        m = mines_core(str(server),str(client),nonce)
        label = m[0] if len(m)>0 else 0

        X.append([
            server%10,
            client%10,
            nonce%10
        ])
        y.append(label)

    model.fit(X,y)

# ================== PREDICTION ==================
def ml_predict(server, client, nonce):
    x = [[server%10, client%10, nonce%10]]
    return model.predict(x)[0]

# ================== GPT STYLE AI ==================
def gpt_ai(msg):
    msg = msg.lower()

    if "mine" in msg:
        return "💣 Mines = hash-based deterministic generation"
    if "cosmos" in msg:
        return "🌌 Cosmos = entropy signal generator"
    if "ai" in msg:
        return "🤖 Fusion AI combines ML + heuristics"
    return "🧠 Processing advanced reasoning..."

# ================== SESSION ==================
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# ================== UI ==================
st.title("🚀 HUBRIS V700 PRO AI ENTERPRISE")

# ================== LOGIN ==================
u = st.text_input("Username")
p = st.text_input("Password", type="password")

col1,col2 = st.columns(2)

with col1:
    if st.button("LOGIN"):
        role = login(u,p)
        if role:
            st.session_state.user = u
            st.session_state.role = role
            st.success("Logged in")
        else:
            st.error("Invalid")

with col2:
    if st.button("REGISTER"):
        register(u,p)
        st.success("User created")

# ================== SYSTEM ==================
if st.session_state.user:

    st.markdown("---")

    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce",1)

    # TRAIN ML
    if st.button("🧠 TRAIN ML"):
        train_model()
        st.success("ML trained")

    # RUN AI
    if st.button("🚀 RUN AI SYSTEM"):

        mines = mines_core(server,client,nonce)
        cosmos = cosmos_signal(server,client,nonce)
        ml = ml_predict(int(len(server)), int(len(client)), nonce)

        st.subheader("💣 MINES")
        st.write(mines)

        st.subheader("🌌 COSMOS")
        st.write(cosmos)

        st.subheader("🤖 ML PREDICTION")
        st.write("Predicted index:", ml)

    # ================== CHAT ==================
    st.markdown("---")
    st.subheader("💬 CHAT (WhatsApp STYLE)")

    msg = st.text_input("Message")

    if st.button("SEND"):
        send_msg(st.session_state.user,msg)

    for u,m in get_msgs()[-20:]:
        st.write(f"🧑 {u}: {m}")

    # ================== GPT AI ==================
    st.markdown("---")
    st.subheader("🤖 GPT AI")

    ask = st.text_input("Ask AI")

    if st.button("ASK"):
        st.success(gpt_ai(ask))
