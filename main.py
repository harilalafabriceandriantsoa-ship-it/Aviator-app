import streamlit as st 
import hashlib
import random
import hmac
import json
import time
import pandas as pd
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="MINES V9000", layout="wide")

# --- DATA ---
DATA_DIR = Path.cwd() / "data"
DATA_DIR.mkdir(exist_ok=True)
HIST_F = DATA_DIR / "history.json"

def save_h(data):
    with open(HIST_F, "w") as f: json.dump(data, f)
def load_h():
    if HIST_F.exists():
        with open(HIST_F, "r") as f: return json.load(f)
    return []

# --- LOGIC ---
def _fy(seed_bytes, nm):
    seed_int = int.from_bytes(seed_bytes[:16], "big")
    rng = random.Random(seed_int)
    pos = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        pos[i], pos[j] = pos[j], pos[i]
    return set(pos[:nm]), set(pos[nm:])

def run_consensus(srv, cli, n, nm):
    key = srv.encode()
    msg = f"{cli}:{n}".encode()
    h = hmac.new(key, msg, hashlib.sha256).digest()
    m, s = _fy(h, nm)
    # Eto dia mampiasa consensus tsotra isika amin'izao
    return m, s, 4 

def get_top5(safe_s, mines_s, srv, cli, n):
    # Fomba fohy hisafidianana ny tsara indrindra
    return sorted(list(safe_s))[:5]

# --- UI ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>💎 MINES V9000</h1>", unsafe_allow_html=True)

if "nonce" not in st.session_state: st.session_state.nonce = 0
if "res" not in st.session_state: st.session_state.res = None

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📥 Paramètres")
    srv = st.text_input("Server Seed SHA256")
    cli = st.text_input("Client Seed")
    n_val = st.number_input("Nonce", value=st.session_state.nonce)
    st.session_state.nonce = int(n_val)
    nm = st.selectbox("Mines", [1, 2, 3], index=2)

    if st.button("💎 KAJY EXACT"):
        if srv and cli:
            m, s, mc = run_consensus(srv, cli, st.session_state.nonce, nm)
            t5 = get_top5(s, m, srv, cli, st.session_state.nonce)
            st.session_state.res = {"m": list(m), "s": list(s), "t5": t5, "n": st.session_state.nonce}
            st.rerun()

with col2:
    if st.session_state.res:
        res = st.session_state.res
        st.success(f"✅ Vita ny kajy! (Nonce: {res['n']})")
        
        # Grid tsotra
        grid_html = "<div style='display:grid; grid-template-columns: repeat(5,1fr); gap:5px;'>"
        for i in range(25):
            bg = "#111"
            txt = str(i)
            if i in res['t5']: bg, txt = "#00ffcc", "💎"
            grid_html += f"<div style='background:{bg}; aspect-ratio:1/1; display:flex; align-items:center; justify-content:center; border-radius:5px; color:#000; font-weight:bold;'>{txt}</div>"
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)
        
        st.write(f"**💎 TOP 5:** {res['t5']}")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ WIN"):
            st.session_state.nonce += 1
            st.session_state.res = None
            st.rerun()
        if c2.button("❌ LOSS"):
            st.session_state.nonce += 1
            st.session_state.res = None
            st.rerun()
    else:
        st.info("Andrasana ny seeds...")
