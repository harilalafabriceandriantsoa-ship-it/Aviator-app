# ================== IMPORT ==================
import streamlit as st
import hashlib
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="HUBRIS V700 AI", layout="wide")

# ================== ULTRA FUTURISTIC UI ==================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #050816, #000000);
    color: #e5e7eb;
    font-family: 'Segoe UI';
}

h1 {
    text-align: center;
    font-size: 42px !important;
    color: #00f5ff !important;
    text-shadow: 0px 0px 25px #00f5ff;
}

h3 {
    text-align: center;
    color: #a5b4fc !important;
}

.block-container {
    padding: 2rem 3rem;
}

div.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.stButton>button {
    background: linear-gradient(135deg, #00f5ff, #7c3aed);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.07);
}

input {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid #00f5ff !important;
    border-radius: 10px !important;
    color: white !important;
}

.grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
}

.cell {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
}

.futuristic-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid #00f5ff;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
}

.center {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.markdown("""
<h1>🚀 HUBRIS V700</h1>
<h3>🌌 COSMOS • RISK • RL • CHATBOT • FUSION AI</h3>
""", unsafe_allow_html=True)

# ================== CORE MINES ==================
def mines_core(server, client, nonce):
    base = f"{server}:{client}:{nonce}"
    hash_val = hashlib.sha256(base.encode()).hexdigest()

    numbers = []
    for i in range(0, 50, 2):
        num = int(hash_val[i:i+2], 16)
        numbers.append(num % 25)

    seen = []
    for n in numbers:
        if n not in seen:
            seen.append(n)
    return seen


# ================== HEATMAP ==================
def mines_heatmap(server, client, nonce, mines_count, rounds=30):
    freq = {i:0 for i in range(25)}

    for i in range(rounds):
        grid = mines_core(server, client, nonce+i)
        mines = grid[:mines_count]
        for m in mines:
            freq[m] += 1

    return freq


def draw_heatmap(freq):
    html = "<div class='grid'>"
    max_val = max(freq.values()) if freq else 1

    for i in range(25):
        val = freq.get(i, 0)
        intensity = val / max_val if max_val else 0

        if intensity > 0.7:
            color = "#ff3333"
        elif intensity > 0.4:
            color = "#ffaa00"
        else:
            color = "#00ffcc"

        html += f"<div class='cell' style='background:{color}'>{val}</div>"

    html += "</div>"
    return html


# ================== RL AGENT ==================
class RLAgent:
    def __init__(self):
        self.q = np.zeros(25)

    def update(self, safe_cells, reward=1):
        for s in safe_cells:
            self.q[s] += reward

    def act(self, risk_prob):
        scores = {}
        for i in range(25):
            scores[i] = (1 - risk_prob[i]) + self.q[i]

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


if "agent" not in st.session_state:
    st.session_state.agent = RLAgent()


# ================== CHATBOT ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def ai_chatbot(user_input):
    user_input = user_input.lower()

    if "safe" in user_input:
        return "💎 Check risk map + lowest probability zones"
    if "cosmos" in user_input:
        return "🌌 COSMOS = volatility signal only"
    if "mine" in user_input:
        return "⚠️ Mines are RNG-based, no exact prediction"
    if "train" in user_input:
        return "🧠 Training improves RL memory only"
    if "best" in user_input:
        return "🔥 Use Fusion AI ranking"

    return random.choice([
        "🤖 Analyzing probability space...",
        "📊 Running Monte Carlo simulation...",
        "🧠 Updating RL memory..."
    ])


# ================== COSMOS ==================
def cosmos_signal(server, client, nonce):
    base = f"{server}:{client}:{nonce}"
    h = hashlib.sha512(base.encode()).hexdigest()

    vec = [int(h[i:i+2], 16) for i in range(0, 32, 2)]
    return np.array(vec) / 255.0


# ================== RISK MODEL ==================
def risk_model(server, client, nonce, mines_count, rounds=300):
    freq = np.zeros(25)

    for i in range(rounds):
        grid = mines_core(server, client, nonce + i)
        mines = grid[:mines_count]

        for m in mines:
            freq[m] += 1

    return freq / rounds


# ================== LIVE GRAPH ==================
def show_live_graph(risk):
    fig, ax = plt.subplots()
    ax.bar(range(25), risk)
    ax.set_title("📊 LIVE RISK MAP")
    st.pyplot(fig)


# ================== AUTO LEARNING ==================
def auto_learn_loop(risk):
    agent = st.session_state.agent
    safe_cells = np.argsort(risk)[:8]
    agent.update(safe_cells, reward=0.5)


# ================== FUSION AI ==================
def fusion_ai(server, client, nonce, mines_count):
    cosmos = cosmos_signal(server, client, nonce)
    risk = risk_model(server, client, nonce, mines_count)

    agent = st.session_state.agent

    blended = {}

    for i in range(25):
        blended[i] = (1 - risk[i]) * 0.6 + cosmos[i % len(cosmos)] * 0.2 + agent.q[i] * 0.2

    ranked = sorted(blended.items(), key=lambda x: x[1], reverse=True)

    return ranked, risk


# ================== TABS ==================
tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💎 MINES AI", "📘 GUIDE"])


# ================== COSMOS TAB ==================
with tab1:
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", min_value=1, value=1)

    if st.button("SCAN COSMOS"):
        h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
        decimal = int(h[-8:], 16)
        result = max(1.0, (4294967295 / decimal) * 0.97)

        st.markdown(f"""
        <div class="futuristic-box center">
            <h3>🌌 COSMOS RESULT</h3>
            <h1>{round(result,2)}</h1>
        </div>
        """, unsafe_allow_html=True)


# ================== MINES TAB ==================
with tab2:
    server_m = st.text_input("Server Seed (mines)")
    client_m = st.text_input("Client Seed (mines)")
    nonce_m = st.number_input("Nonce (mines)", min_value=1, value=1)
    mines_count = st.slider("Mines", 1, 3, 3)

    st.markdown("""
    <div class="futuristic-box center">
        <h3>⚡ SYSTEM STATUS</h3>
        <p>🧠 AI ACTIVE</p>
        <p>🌌 COSMOS ONLINE</p>
        <p>📊 RISK RUNNING</p>
        <p>🤖 RL LEARNING</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🧠 TRAIN AI"):
        risk = risk_model(server_m, client_m, nonce_m, mines_count)
        safe_cells = np.argsort(risk)[:10]
        st.session_state.agent.update(safe_cells)
        st.success("AI TRAINED")

    if st.button("🚀 RUN FUSION AI"):
        ranked, risk = fusion_ai(server_m, client_m, nonce_m, mines_count)

        st.markdown("""
        <div class="futuristic-box">
            <h3>💎 TOP SAFE ZONES</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write(ranked[:5])

        st.markdown("""
        <div class="futuristic-box">
            <h3>⚠️ RISK MAP</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write(risk)

        show_live_graph(risk)
        auto_learn_loop(risk)

    st.markdown("---")

    if st.button("📊 HEATMAP"):
        freq = mines_heatmap(server_m, client_m, nonce_m, mines_count)
        st.markdown(draw_heatmap(freq), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 💬 AI CHATBOT")
    user_msg = st.text_input("Ask AI")

    if st.button("SEND"):
        response = ai_chatbot(user_msg)
        st.session_state.chat_history.append((user_msg, response))

    for q, a in st.session_state.chat_history[-5:]:
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI:** {a}")


# ================== GUIDE ==================
with tab3:
    st.markdown("""
## 📘 HUBRIS V700 GUIDE

### 🌌 COSMOS
- Volatility signal only

### 💎 RISK MODEL
- Monte Carlo probability

### 🤖 RL SYSTEM
- Memory learning only

### 🔥 FUSION AI
- COSMOS + RISK + RL

### 💬 CHATBOT
- Assistant system (no real prediction)

### 📊 GRAPH
- Live risk visualization

⚠️ Not a predictor — decision support AI system
""")
