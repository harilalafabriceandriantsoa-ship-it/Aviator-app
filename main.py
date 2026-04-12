import streamlit as st
import hashlib
import hmac
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Provably Fair Analyzer", layout="wide")

st.title("🔐 PROVABLY FAIR ANALYZER TOOL")

# ---------------- INPUT ----------------
server_seed = st.text_input("Server Seed (revealed)")
client_seed = st.text_input("Client Seed")
nonce_start = st.number_input("Nonce Start", value=0)
nonce_end = st.number_input("Nonce End", value=20)

# ---------------- HASH ENGINE ----------------
def get_hash(server_seed, client_seed, nonce):
    msg = f"{client_seed}:{nonce}".encode()
    key = server_seed.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

# ---------------- BOARD GENERATION (25 tiles) ----------------
def generate_board(hash_hex):
    arr = []
    for i in range(0, 50, 2):
        val = int(hash_hex[i:i+2], 16)
        arr.append(val % 25)
    return arr

# ---------------- ANALYSIS ----------------
def analyze(server_seed, client_seed, start, end):
    results = np.zeros(25)

    history = []

    for nonce in range(start, end + 1):
        h = get_hash(server_seed, client_seed, nonce)
        board = generate_board(h)

        for b in board:
            results[b] += 1

        history.append(board)

    results = results / np.sum(results)
    return results, history

# ---------------- RENDER GRID ----------------
def draw_grid(prob):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(range(25)),
        y=prob
    ))

    fig.update_layout(
        title="📊 Tile Probability Distribution (From Seeds)",
        xaxis_title="Tile Index (0-24)",
        yaxis_title="Frequency",
        height=400
    )

    return fig

# ---------------- EXECUTE ----------------
if st.button("ANALYZE FAIRNESS"):

    if server_seed and client_seed:

        prob, history = analyze(server_seed, client_seed, nonce_start, nonce_end)

        st.plotly_chart(draw_grid(prob), use_container_width=True)

        st.subheader("📦 Normalized Distribution")
        st.write(prob)

        st.subheader("🔁 Sample Generated Boards")
        st.write(history[:5])

        # entropy check
        entropy = -np.sum(prob * np.log(prob + 1e-9))
        st.info(f"📉 Entropy Score: {entropy:.4f}")

        uniform = np.ones(25) / 25
        deviation = np.sum(np.abs(prob - uniform))
        st.info(f"📊 Deviation from uniform randomness: {deviation:.4f}")

    else:
        st.error("Please enter both seeds")
