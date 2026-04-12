import streamlit as st
import hashlib
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="MINES AI V5 GOD", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES V5 GOD ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")
else:

    st.title("💎 MINES AI V5 GOD MODE ULTIMATE")

    # ---------------- MEMORY / DATASET BOT ----------------
    if "data" not in st.session_state:
        st.session_state.data = []

    if "stats" not in st.session_state:
        st.session_state.stats = {"win": 0, "loss": 0}

    # ---------------- FEATURE ENGINE ----------------
    def features(server, client, nonce):
        h1 = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).digest()
        h2 = hashlib.sha512(f"{client}:{nonce}:{server}".encode()).digest()
        return np.array(list(h1[:8]) + list(h2[:8]), dtype=np.float32)

    # ---------------- SEQUENCE MEMORY ----------------
    def sequence(nonce):
        return np.array([nonce + i for i in range(8)], dtype=np.float32)

    # ---------------- TRANSFORMER STYLE MODEL ----------------
    class TransformerLike(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(24, 128)
            self.fc2 = nn.Linear(128, 128)
            self.attn = nn.Linear(128, 128)
            self.fc3 = nn.Linear(128, 25)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            a = torch.softmax(self.attn(x), dim=1)
            x = x * a
            x = torch.relu(self.fc2(x))
            return torch.softmax(self.fc3(x), dim=1)

    def get_model():
        if "model" not in st.session_state:
            st.session_state.model = TransformerLike()
            st.session_state.opt = optim.Adam(st.session_state.model.parameters(), lr=0.001)
        return st.session_state.model, st.session_state.opt

    # ---------------- MONTE CARLO ----------------
    def monte_carlo(server, client, nonce):
        arr = np.zeros(25)
        for i in range(400):
            h = hashlib.sha256(f"{server}:{client}:{nonce*i}".encode()).digest()
            arr[h[0] % 25] += 1
        return arr / np.sum(arr)

    # ---------------- HEURISTIC ENGINE ----------------
    def heuristics(prob):
        penalty = np.zeros(25)

        for i in range(25):
            if i % 5 == 0:
                penalty[i] += 0.02
            if prob[i] < 0.02:
                penalty[i] += 0.03

        return prob - penalty

    # ---------------- CONFIDENCE ----------------
    def confidence(prob):
        prob = np.clip(prob, 1e-9, 1)
        ent = -np.sum(prob * np.log(prob))
        return round((1 - ent / np.log(25)) * 100, 2)

    # ---------------- TRAIN ----------------
    def train():
        if len(st.session_state.data) < 80:
            return

        model, opt = get_model()

        batch = st.session_state.data[-300:]

        X = torch.tensor(np.array([i[0] for i in batch]), dtype=torch.float32)
        Y = torch.tensor(np.array([i[1] for i in batch]), dtype=torch.long)

        out = model(X)
        loss = nn.CrossEntropyLoss()(out, Y)

        opt.zero_grad()
        loss.backward()
        opt.step()

    # ---------------- PREDICT ENGINE ----------------
    def predict(server, client, nonce, mines_count):

        mc = monte_carlo(server, client, nonce)

        model, _ = get_model()

        seq = sequence(nonce)
        f = features(server, client, nonce)

        inp = torch.tensor(np.concatenate([f, seq]), dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            ml = model(inp).numpy()[0]

        # fusion
        final = 0.55 * mc + 0.45 * ml

        # heuristic boost
        final = heuristics(final)
        final = final / np.sum(final)

        rank = np.argsort(-final)

        # ---------------- SAFE / RISKY STYLE (PRESERVED) ----------------
        safe = list(map(int, rank[:5]))
        risky = list(map(int, rank[-5:]))

        conf = confidence(final)

        # ---------------- DATASET BOT ----------------
        label = int(np.argmax(mc))
        st.session_state.data.append((inp.numpy().flatten(), label))

        train()

        return safe, risky, conf, final

    # ---------------- CHART ----------------
    def chart(prob):
        fig = go.Figure()
        fig.add_trace(go.Bar(y=prob))
        fig.update_layout(title="📊 Risk Distribution", height=300)
        return fig

    # ---------------- UI ----------------
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", value=1)

    mines_count = st.selectbox("MINES MODE", [1, 2, 3])

    if st.button("SCAN MINES V5 GOD"):

        safe, risky, conf, prob = predict(server, client, nonce, mines_count)

        # GRID UI (UNCHANGED STYLE)
        html = "<div style='display:grid;grid-template-columns:repeat(5,60px);gap:10px;'>"
        for i in range(25):
            if i in safe:
                html += "<div style='background:#00ff99;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>💎</div>"
            elif i in risky:
                html += "<div style='background:#ff0033;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>☠️</div>"
            else:
                html += "<div style='background:#222;height:60px;border:1px solid #444;'></div>"
        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

        st.success(f"SAFE 💎: {safe}")
        st.error(f"RISK ☠️: {risky}")
        st.info(f"CONFIDENCE: {conf}%")

        st.plotly_chart(chart(prob), use_container_width=True)

        # ---------------- LIVE DASHBOARD ----------------
        win_rate = st.session_state.stats["win"] / (st.session_state.stats["win"] + st.session_state.stats["loss"] + 1e-9)

        if conf > 60:
            st.session_state.stats["win"] += 1
        else:
            st.session_state.stats["loss"] += 1

        st.markdown("## 📈 LIVE DASHBOARD")
        st.write(st.session_state.stats)
        st.info(f"WIN RATE: {win_rate:.2f}")
