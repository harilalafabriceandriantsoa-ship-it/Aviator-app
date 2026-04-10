import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("hubris_v900.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    input TEXT,
    output TEXT
)
""")
conn.commit()

def save_record(t, inp, out):
    cursor.execute("INSERT INTO history (type,input,output) VALUES (?,?,?)",
                   (t, str(inp), str(out)))
    conn.commit()

def load_history():
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    return cursor.fetchall()

# ================= COSMOS ENGINE =================
def cosmos_engine(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

    values = [int(h[i:i+2],16) for i in range(0,32,2)]
    trend = np.mean(values)
    volatility = np.var(values)

    signal = "🔴 SKIP"
    if trend > 120 and volatility < 500:
        signal = "🟢 PLAY"

    return {
        "trend": float(trend),
        "volatility": float(volatility),
        "signal": signal
    }

# ================= MINES ENGINE =================
def mines_engine(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16],"big")

    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)

    mines = grid[:3]
    safe = grid[3:]

    risk_map = np.zeros(25)
    for i in mines:
        risk_map[i] = 1

    confidence = float((1 - np.mean(risk_map)) * 100)

    return {
        "safe": safe[:5],
        "risk": mines,
        "confidence": confidence
    }

# ================= FUSION AI =================
def fusion(cosmos, mines):
    if cosmos["signal"] == "🟢 PLAY" and mines["confidence"] > 60:
        return "🟢 STRONG ENTRY"
    elif cosmos["signal"] == "🟢 PLAY":
        return "🟡 WEAK ENTRY"
    else:
        return "🔴 NO TRADE"

# ================= STREAMLIT UI =================
st.set_page_config(page_title="HUBRIS V900", layout="wide")

st.title("🚀 HUBRIS V900 ULTIMATE ENGINE")

tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💎 MINES", "📊 HISTORY"])

# ================= COSMOS TAB =================
with tab1:
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", value=1)

    if st.button("RUN COSMOS"):
        result = cosmos_engine(server, client, nonce)
        save_record("COSMOS", f"{server}-{client}-{nonce}", result)
        st.json(result)

# ================= MINES TAB =================
with tab2:
    s = st.text_input("Server (Mines)")
    c = st.text_input("Client (Mines)")
    n = st.number_input("Nonce Mines", value=1)

    if st.button("RUN MINES"):
        m = mines_engine(s,c,n)
        save_record("MINES", f"{s}-{c}-{n}", m)
        st.json(m)

    if st.button("FUSION AI"):
        cosmos = cosmos_engine(s,c,n)
        mines = mines_engine(s,c,n)

        decision = fusion(cosmos, mines)

        save_record("FUSION", f"{s}-{c}-{n}", decision)

        st.success(decision)

# ================= HISTORY TAB =================
with tab3:
    st.subheader("📊 AI LEARNING HISTORY")
    data = load_history()

    for row in data[:50]:
        st.write(row)
