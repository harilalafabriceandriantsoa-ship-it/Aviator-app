import streamlit as st
import hashlib
import random
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V1000 GOD MODE", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>  
.stApp {background: linear-gradient(135deg,#0f0f0f,#1c1c1c);color:#00ffcc;}  
h1,h2,h3{text-align:center;color:#00ffcc;}  
.stButton>button {  
    background: linear-gradient(90deg,#00ffcc,#0066ff);  
    color:white;border-radius:10px;height:45px; width:100%;
}  
.grid {  
    display:grid;  
    grid-template-columns:repeat(5,60px);  
    gap:10px;justify-content:center;margin-top:20px;  
}  
.cell {  
    width:60px;height:60px;  
    display:flex;align-items:center;justify-content:center;  
    border-radius:10px;font-size:22px;  
}  
.safe {background:#00ffcc;color:#000;}  
.risk {background:#ff0033;color:#fff;}  
.best {background:#ffff00;color:#000;font-weight:bold;}  
.empty {background:#222;border:1px solid #444;}  
</style>  """, unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "memory" not in st.session_state: st.session_state.memory = []
if "balance" not in st.session_state: st.session_state.balance = 1000
if "login" not in st.session_state: st.session_state.login = False
if "last_result" not in st.session_state: st.session_state.last_result = "WIN"

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐 HUBRIS SECURE ACCESS")
    pwd = st.text_input("Password", type="password")
    if st.button("ENTER"):  
        if pwd == "2026":  
            st.session_state.login = True  
            st.rerun()  
        else: st.error("Wrong password")  
    st.stop()

# ---------------- UTILS ----------------
def verify_hash(server, client, nonce):
    return hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()

def monte_carlo(server, client, nonce):
    scores = np.zeros(25)
    for i in range(200):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).digest()
        val = int.from_bytes(h[:2],"big") % 25
        scores[val]+=1
    return scores/200

def features(s,c,n):
    h = hashlib.sha256(f"{s}:{c}:{n}".encode()).hexdigest()
    return [int(h[i:i+2],16) for i in range(0,20,2)]

def train_model():
    if len(st.session_state.memory) < 10: return None
    X = [m[0] for m in st.session_state.memory]; y = [m[1] for m in st.session_state.memory]
    model = RandomForestClassifier(n_estimators=100); model.fit(X,y)
    return model

# ---------------- MINES AI (CUSTOM PREDICTIONS) ----------------
def mines_ai(server, client, nonce, mines_count):
    # Ny scan_depth sy ny multiplier dia miova arakaraka ny mines
    # Izany no mampisy fahasamihafana amin'ny prédiction 1, 2, 3
    depth_map = {1: 5, 2: 7, 3: 10}
    scan_depth = depth_map.get(mines_count, 5)
    
    weights = [0.95**i for i in range(scan_depth)]
    combined_scores = np.zeros(25)

    for offset in range(scan_depth):
        risk = monte_carlo(server, client, nonce + (offset * mines_count)) # Offset miova arakaraka ny mine
        combined_scores += (1-risk) * weights[offset]

    combined_scores /= sum(weights)

    # ML integration
    model = train_model()
    ml = np.zeros(25)
    if model:
        pred = model.predict([features(server,client,nonce)])[0]
        ml[pred] += 0.5 

    # Stability calculation
    variance = np.var(combined_scores)
    stability = 1 / (1 + variance * (mines_count * 2.0))

    # Final logic fusion
    final = combined_scores * 0.5 + ml * 0.3 + stability * 0.2
    rank = np.argsort(-final)

    # Fixe 5 Safe & 5 Risky
    safe = rank[:5].tolist()
    risky = rank[-5:].tolist()
    best = safe[:2]

    # Confidence calculation
    base_conf = np.mean(final[safe]) * 100
    if st.session_state.last_result == "LOSE": base_conf += 7
    
    confidence = round(base_conf - (mines_count * 4.5), 2)
    
    # Save to memory
    if len(st.session_state.memory) > 100: st.session_state.memory.pop(0)
    st.session_state.memory.append((features(server,client,nonce), int(safe[0])))

    return safe, risky, best, confidence

# ---------------- UI COMPONENTS ----------------
def draw_grid(safe, risky, best):
    html = "<div class='grid'>"
    for i in range(25):
        if i in best: html += "<div class='cell best'>⭐</div>"
        elif i in safe: html += "<div class='cell safe'>💎</div>"
        elif i in risky: html += "<div class='cell risk'>☠️</div>"
        else: html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- MAIN APP ----------------
st.title("🔥 HUBRIS V1000 GOD MODE")

tab1, tab2 = st.tabs(["💎 MINES SCANNER", "💬 AUTO-SUPPORT"])

with tab1:
    col1, col2 = st.columns(2)
    with col1: s_m = st.text_input("Server Seed", key="m1")
    with col2: c_m = st.text_input("Client Seed", key="m2")
    
    n_m = st.number_input("Nonce", 1, key="m3")
    mines_count = st.selectbox("Isan'ny Mines", [1, 2, 3])

    if st.button("EXECUTE SCAN"):
        if s_m and c_m:
            safe, risk, best, conf = mines_ai(s_m, c_m, n_m, mines_count)
            st.markdown(draw_grid(safe, risk, best), unsafe_allow_html=True)
            
            st.write(f"### 🎯 Confidence Score: {conf}%")
            st.info(f"Fanamarihana: Ny prédiction ho an'ny Mine {mines_count} dia namboarina manokana.")
        else:
            st.warning("Ampidiro ny Seeds azafady.")

with tab2:
    st.write(f"**Current Balance:** {st.session_state.balance}")
    msg = st.text_input("Posez votre question")
    if st.button("Send"):
        st.success("Analysis complete. System ready.")

st_autorefresh(interval=15000, limit=None)
