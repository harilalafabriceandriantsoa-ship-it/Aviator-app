# ================== IMPORTS ==================
import streamlit as st
import sqlite3
import numpy as np
import hashlib
import random
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 GOD MODE", layout="wide")

# ================== DB INIT ==================
def init_db():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        msg TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================== AUTH ==================
def login(u,p):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    return c.fetchone()

# ================== CHAT ==================
def send_msg(user,msg):
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (user,msg) VALUES (?,?)",(user,msg))
    conn.commit()
    conn.close()

def get_msgs():
    conn = sqlite3.connect("hubris.db")
    c = conn.cursor()
    c.execute("SELECT user,msg FROM messages")
    data = c.fetchall()
    conn.close()
    return data

# ================== AI CORE ==================
class RLAgent:
    def __init__(self):
        self.q = np.zeros(25)

    def update(self, idx):
        self.q[idx] += 1

agent = RLAgent()

def cosmos(seed):
    h = hashlib.sha512(seed.encode()).hexdigest()
    return np.array([int(h[i:i+2],16) for i in range(0,32,2)]) / 255

def risk(seed):
    h = hashlib.sha256(seed.encode()).hexdigest()
    return np.array([int(h[i:i+2],16)%100 for i in range(0,50,2)]) / 100

def fusion(seed):
    r = risk(seed)
    c = cosmos(seed)

    score = {}
    for i in range(25):
        score[i] = (1-r[i%len(r)])*0.5 + c[i%len(c)]*0.3 + agent.q[i]*0.2

    return sorted(score.items(), key=lambda x:x[1], reverse=True)

# ================== DEEP LEARNING ==================
SEQ_LEN = 10
FEATURES = 25

model = tf.keras.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(SEQ_LEN, FEATURES)),
    layers.LSTM(64),
    layers.Dense(FEATURES, activation="sigmoid")
])

model.compile(optimizer="adam", loss="mse")

def train_model():
    X = np.random.rand(200,SEQ_LEN,FEATURES)
    y = np.random.rand(200,FEATURES)
    model.fit(X,y,epochs=2,verbose=0)

def predict(seq):
    seq = np.resize(seq,(SEQ_LEN,FEATURES))
    return model.predict(seq.reshape(1,SEQ_LEN,FEATURES),verbose=0)[0]

# ================== UI ==================
st.title("🚀 HUBRIS V700 — GOD MODE AI SYSTEM")

# ================== LOGIN ==================
if "user" not in st.session_state:
    st.session_state.user = None

u = st.text_input("Username")
p = st.text_input("Password",type="password")

if st.button("LOGIN"):
    if login(u,p):
        st.session_state.user = u
        st.success("Logged in")
    else:
        st.error("Invalid credentials")

# ================== MAIN SYSTEM ==================
if st.session_state.user:

    st.subheader("💬 CHAT SYSTEM")

    msg = st.text_input("Message")

    if st.button("SEND"):
        send_msg(st.session_state.user,msg)

    for u,m in get_msgs():
        st.write(f"{u}: {m}")

    st.markdown("---")

    # ================== AI ==================
    st.subheader("🧠 AI FUSION ENGINE")

    seed = st.text_input("Seed input")

    if st.button("RUN AI"):
        res = fusion(seed)
        st.write("TOP RESULTS:", res[:5])

    st.markdown("---")

    # ================== DEEP LEARNING ==================
    st.subheader("📊 DEEP LEARNING ENGINE")

    if st.button("TRAIN MODEL"):
        train_model()
        st.success("Model trained")

    seq = np.random.rand(SEQ_LEN,FEATURES)

    if st.button("PREDICT"):
        st.write(predict(seq))

    st.markdown("---")

    # ================== VISUAL ==================
    st.subheader("📈 RISK GRAPH")

    if seed:
        r = risk(seed)

        fig, ax = plt.subplots()
        ax.bar(range(len(r)), r)
        st.pyplot(fig)
