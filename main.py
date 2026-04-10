import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3
import datetime

# ================= DATABASE =================
conn = sqlite3.connect("hubris_v1000.db", check_same_thread=False)
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

# CHAT
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    role TEXT,
    message TEXT,
    reply TEXT,
    time TEXT
)
""")

# HISTORY AI
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    input TEXT,
    output TEXT
)
""")

conn.commit()

# ================= DEFAULT ADMIN =================
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users VALUES ('admin','admin','admin')")
    conn.commit()

# ================= LOGIN =================
def login(user, pwd):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
    return cursor.fetchone()

# ================= COSMOS =================
def cosmos_engine(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    values = [int(h[i:i+2],16) for i in range(0,32,2)]

    trend = np.mean(values)
    var = np.var(values)

    signal = "SKIP"
    if trend > 120 and var < 500:
        signal = "PLAY"

    return {"trend":trend,"var":var,"signal":signal}

# ================= MINES =================
def mines_engine(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16],"big")

    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)

    mines = grid[:3]
    safe = grid[3:]

    risk = np.zeros(25)
    for m in mines:
        risk[m] = 1

    confidence = float((1 - np.mean(risk)) * 100)

    return {"safe":safe[:5],"risk":mines,"confidence":confidence}

# ================= FUSION =================
def fusion(cosmos, mines):
    if cosmos["signal"] == "PLAY" and mines["confidence"] > 60:
        return "🟢 STRONG ENTRY"
    return "🔴 NO TRADE"

# ================= CHAT SYSTEM =================
def send_message(user, role, msg):
    cursor.execute(
        "INSERT INTO chat(username,role,message,reply,time) VALUES (?,?,?,?,?)",
        (user,role,msg,"",str(datetime.datetime.now()))
    )
    conn.commit()

def reply_message(chat_id, reply):
    cursor.execute("UPDATE chat SET reply=? WHERE id=?", (reply,chat_id))
    conn.commit()

def get_chat():
    cursor.execute("SELECT * FROM chat ORDER BY id DESC")
    return cursor.fetchall()

# ================= UI =================
st.set_page_config("HUBRIS V1000", layout="wide")

st.title("🚀 HUBRIS V1000 CHAT + AI PLATFORM")

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# ================= LOGIN PAGE =================
if st.session_state.user is None:

    st.subheader("🔐 LOGIN")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        res = login(user,pwd)
        if res:
            st.session_state.user = user
            st.session_state.role = res[2]
            st.rerun()
        else:
            st.error("Login failed")

    st.stop()

# ================= MAIN APP =================
st.sidebar.success(f"User: {st.session_state.user}")
st.sidebar.info(f"Role: {st.session_state.role}")

tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💎 MINES", "💬 CHAT"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server")
    c = st.text_input("Client")
    n = st.number_input("Nonce",1)

    if st.button("RUN COSMOS"):
        res = cosmos_engine(s,c,n)
        st.json(res)

        cursor.execute("INSERT INTO history(type,input,output) VALUES (?,?,?)",
                       ("COSMOS",f"{s}-{c}-{n}",str(res)))
        conn.commit()

# ================= MINES =================
with tab2:
    s = st.text_input("Server M")
    c = st.text_input("Client M")
    n = st.number_input("Nonce M",1)

    if st.button("RUN MINES"):
        res = mines_engine(s,c,n)
        st.json(res)

    if st.button("FUSION"):
        cos = cosmos_engine(s,c,n)
        mino = mines_engine(s,c,n)
        st.success(fusion(cos,mino))

# ================= CHAT =================
with tab3:
    st.subheader("💬 CHAT SYSTEM")

    msg = st.text_input("Write message")

    if st.button("SEND"):
        send_message(st.session_state.user, st.session_state.role, msg)
        st.success("Sent")

    st.markdown("---")
    st.write("### Messages")

    chats = get_chat()

    for c in chats[:20]:
        st.write(f"👤 {c[1]} ({c[2]}): {c[3]}")
        if c[2] == "user" and st.session_state.role == "admin":
            rep = st.text_input(f"Reply {c[0]}", key=str(c[0]))
            if st.button(f"Send Reply {c[0]}"):
                reply_message(c[0], rep)
                st.rerun()
        if c[4]:
            st.info(f"↳ Admin: {c[4]}")
