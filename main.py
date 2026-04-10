import streamlit as st
import numpy as np
import hashlib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# ================== UI CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 QUANT AI", layout="wide")

st.title("🚀 HUBRIS V700 PRO QUANT AI + DIAMOND DASHBOARD")

# ================== MINES CORE (PRESERVED) ==================
def mines_core(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()

    nums = [int(h[i:i+2], 16) % 25 for i in range(0, 50, 2)]

    seen = []
    for n in nums:
        if n not in seen:
            seen.append(n)
    return seen

# ================== COSMOS SIGNAL (NO SCHEMA) ==================
def cosmos_base(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return np.array([int(h[i:i+2], 16) for i in range(0, 32, 2)]) / 255

# ================== COSMOS TOUR 1 ==================
def cosmos_tour1(server, client, nonce):
    return cosmos_base(server, client, nonce)

# ================== COSMOS TOUR 2 ==================
def cosmos_tour2(server, client, nonce):
    b = cosmos_base(server, client, nonce)
    return (b[:-1] + b[1:]) / 2

# ================== COSMOS TOUR 3 ==================
def cosmos_tour3(server, client, nonce):
    b = cosmos_base(server, client, nonce)

    return {
        "mean": float(np.mean(b)),
        "std": float(np.std(b)),
        "stability": float(1 - np.std(b))
    }

# ================== RISK MODEL ==================
def risk_model(server, client, nonce):
    freq = np.zeros(25)

    for i in range(120):
        grid = mines_core(server, client, nonce + i)
        for g in grid:
            freq[g] += 1

    return freq / np.max(freq)

# ================== DIAMOND ENGINE ==================
def top5_diamonds(risk):
    return np.argsort(risk)[:5]

# ================== ML MODEL ==================
model = RandomForestClassifier(n_estimators=80)

def train_model():
    X, y = [], []

    for i in range(250):
        s, c, n = str(i), str(i*2), i

        m = mines_core(s, c, n)
        label = m[0] if len(m) > 0 else 0

        X.append([len(s)%10, len(c)%10, n%10])
        y.append(label)

    model.fit(X, y)

def ml_predict(server, client, nonce):
    return model.predict([[len(server)%10, len(client)%10, nonce%10]])[0]

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

# ================== INPUT ==================
server = st.text_input("Server Seed")
client = st.text_input("Client Seed")
nonce = st.number_input("Nonce", 1)

# ================== ACTIONS ==================
col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 TRAIN AI"):
        train_model()
        st.success("MODEL TRAINED")

with col2:
    run = st.button("🚀 RUN FULL ANALYTICS")

# ================== OUTPUT ==================
if run:

    mines = mines_core(server, client, nonce)
    ranked, risk = quant_ai(server, client, nonce)

    diamonds = top5_diamonds(risk)

    t1 = cosmos_tour1(server, client, nonce)
    t2 = cosmos_tour2(server, client, nonce)
    t3 = cosmos_tour3(server, client, nonce)

    # ================== MINES ==================
    st.subheader("💣 MINES SCHEMA")
    st.write(mines)

    # ================== DIAMONDS ==================
    st.subheader("💎 TOP 5 DIAMONDS")
    st.markdown(
        f"💎 {diamonds[0]} | 💎 {diamonds[1]} | 💎 {diamonds[2]} | 💎 {diamonds[3]} | 💎 {diamonds[4]}"
    )

    # ================== QUANT RANKING ==================
    st.subheader("📊 QUANT RANKING (TOP 10)")
    st.write(ranked[:10])

    # ================== COSMOS ==================
    st.subheader("🌌 COSMOS TOUR 1")
    st.write(t1)

    st.subheader("🌌 COSMOS TOUR 2")
    st.write(t2)

    st.subheader("🌌 COSMOS TOUR 3")
    st.json(t3)

    # ================== RISK ==================
    st.subheader("⚠️ RISK MAP")
    st.bar_chart(risk)

    fig, ax = plt.subplots()
    ax.bar(range(25), risk)
    st.pyplot(fig)
