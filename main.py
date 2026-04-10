# ================== IMPORTS ==================
import streamlit as st
import sqlite3
import numpy as np
import hashlib
import random
import matplotlib.pyplot as plt

# ================== CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 GOD MODE", layout="wide")

# ================== DB ==================
def init_db():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        user TEXT,
        msg TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================== AUTH ==================
def login(user, pw):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pw))
    return c.fetchone()

def register(user,pw):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)",(user,pw))
    conn.commit()
    conn.close()

# ================== CHAT ==================
def send_msg(user,msg):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages VALUES (?,?)",(user,msg))
    conn.commit()
    conn.close()

def get_msgs():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    return c.fetchall()

# ================== COSMOS ==================
def cosmos(seed):
    h = hashlib.sha512(seed.encode()).hexdigest()
    return np.array([int(h[i:i+2],16) for i in range(0,32,2)]) / 255

# ================== MINES ==================
def mines(seed):
    h = hashlib.sha256(seed.encode()).hexdigest()
    nums = [int(h[i:i+2],16)%25 for i in range(0,50,2)]

    seen = []
    for n in nums:
        if n not in seen:
            seen.append(n)
    return seen

# ================== RISK ==================
def risk(seed):
    h = hashlib.sha256(seed.encode()).hexdigest()
    return np.array([int(h[i:i+2],16)%100 for i in range(0,50,2)]) / 100

# ================== RL MEMORY ==================
class RLMemory:
    def __init__(self):
        self.q = np.zeros(25)

    def update(self, idxs):
        for i in idxs:
            self.q[i] += 1

memory = RLMemory()

# ================== FUSION AI ==================
def fusion(seed):

    r = risk(seed)
    c = cosmos(seed)
    m = mines(seed)

    score = {}

    for i in range(25):
        score[i] = (
            (1 - r[i % len(r)]) * 0.5 +
            c[i % len(c)] * 0.3 +
            memory.q[i] * 0.2
        )

    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return ranked, r, m

# ================== CHAT AI ==================
def chat_ai(msg):
    msg = msg.lower()

    if "risk" in msg:
        return "⚠️ Risk is probability-based (hash simulation)"
    if "cosmos" in msg:
        return "🌌 COSMOS = entropy signal generator"
    if "mine" in msg:
        return "💣 Mines generated using SHA256 randomness"
    if "best" in msg:
        return "🔥 Fusion AI ranks best safe zones"

    return random.choice([
        "🤖 Processing request...",
        "📊 Running AI model...",
        "🧠 Updating system..."
    ])

# ================== SESSION ==================
if "user" not in st.session_state:
    st.session_state.user = None

# ================== UI ==================
st.title("🚀 HUBRIS V700 — GOD MODE FULL STACK")

# ================== LOGIN ==================
st.subheader("🔐 LOGIN SYSTEM")

user = st.text_input("Username")
pw = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("LOGIN"):
        if login(user,pw):
            st.session_state.user = user
            st.success("Logged in")
        else:
            st.error("Wrong credentials")

with col2:
    if st.button("REGISTER"):
        register(user,pw)
        st.success("User created")

# ================== MAIN SYSTEM ==================
if st.session_state.user:

    st.markdown("---")
    st.subheader("🧠 HUBRIS AI ENGINE")

    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", 1)

    seed = f"{server}:{client}:{nonce}"

    if st.button("🚀 RUN AI") and server:

        ranked, r, m = fusion(seed)

        st.subheader("💎 TOP ZONES")
        st.write(ranked[:5])

        st.subheader("💣 MINES")
        st.write(m)

        st.subheader("⚠️ RISK MAP")
        st.write(r)

        fig, ax = plt.subplots()
        ax.bar(range(len(r)), r)
        st.pyplot(fig)

        # RL update
        memory.update([i[0] for i in ranked[:5]])

    # ================== CHAT ==================
    st.markdown("---")
    st.subheader("💬 CHAT SYSTEM")

    msg = st.text_input("Message")

    if st.button("SEND"):
        send_msg(st.session_state.user, msg)

    for u,m in get_msgs():
        st.write(f"{u}: {m}")

    # ================== AI CHAT ==================
    st.markdown("---")
    st.subheader("🤖 AI ASSISTANT")

    ask = st.text_input("Ask AI")

    if st.button("ASK"):
        st.success(chat_ai(ask))
