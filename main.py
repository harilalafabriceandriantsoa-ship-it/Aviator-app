import streamlit as st
import hashlib
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="MINES AI", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 MINES ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong password")

else:
    st.title("💎 MINES AI SYSTEM")

    # ---------------- SESSION ----------------
    if "memory" not in st.session_state:
        st.session_state.memory = []

    # ---------------- MONTE CARLO ----------------
    def monte_carlo(server, client, nonce):
        scores = np.zeros(25)
        for i in range(200):
            h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).digest()
            val = int.from_bytes(h[:2],"big") % 25
            scores[val]+=1
        return scores/200

    # ---------------- FEATURES ----------------
    def features(s,c,n):
        h = hashlib.sha256(f"{s}:{c}:{n}".encode()).hexdigest()
        return [int(h[i:i+2],16) for i in range(0,20,2)]

    # ---------------- TRAIN ----------------
    def train_model():
        if len(st.session_state.memory) < 30:
            return None

        X = [m[0] for m in st.session_state.memory]
        y = [m[1] for m in st.session_state.memory]

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X,y)
        return model

    # ---------------- MINES AI ----------------
    def mines_ai(server, client, nonce, mines_count):
        risk = monte_carlo(server, client, nonce)
        model = train_model()

        ml = np.zeros(25)

        if model:
            pred = model.predict([features(server,client,nonce)])[0]
            ml[pred]+=1

        final = (1-risk)*0.7 + ml*0.3
        rank = np.argsort(-final)

        safe = list(map(int, rank[:5]))
        risky = list(map(int, rank[-(5+mines_count):]))

        confidence = round(float(np.max(final)*100 - mines_count*5),2)

        st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

        return safe, risky, confidence

    # ---------------- GRID ----------------
    def draw_grid(safe, risky):
        html = "<div style='display:grid;grid-template-columns:repeat(5,60px);gap:10px;justify-content:center;'>"
        for i in range(25):
            if i in safe:
                html += "<div style='background:#00ffcc;color:black;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>💎</div>"
            elif i in risky:
                html += "<div style='background:#ff0033;color:white;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>☠️</div>"
            else:
                html += "<div style='background:#222;height:60px;border:1px solid #444;'></div>"
        html += "</div>"
        return html

    # ---------------- UI ----------------
    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Nonce", value=1)

    mines_count = st.selectbox("Nombre de mines", [1,2,3])

    if st.button("SCAN MINES"):
        safe, risky, conf = mines_ai(server, client, nonce, mines_count)

        st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)
        st.success(f"SAFE 💎: {safe}")
        st.error(f"RISK ☠️: {risky}")
        st.info(f"CONFIDENCE: {conf}%")
