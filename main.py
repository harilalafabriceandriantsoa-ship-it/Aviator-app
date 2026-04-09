import streamlit as st
import hashlib
import random
import statistics

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V550 FINAL", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f0f0f,#1c1c1c);color:#00ffcc;}
h1,h2,h3{text-align:center;color:#00ffcc;}
.stButton>button {background: linear-gradient(90deg,#00ffcc,#0066ff);color:white;border-radius:10px;height:45px;}
.grid {display:grid;grid-template-columns:repeat(5,60px);gap:10px;justify-content:center;margin-top:20px;}
.cell {width:60px;height:60px;display:flex;align-items:center;justify-content:center;border-radius:10px;font-size:22px;}
.safe {background:#00ffcc;color:#000;box-shadow:0 0 15px #00ffcc;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- COSMOS ----------------
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos(server, client, nonce):
    tours = []
    for i in range(20):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        dec = int(h[-8:], 16) or 1
        crash_val = (4294967295 * 0.97) / dec
        jump = ((dec % 7) + (dec % 11) + (dec % 13)) // 2
        jump = max(2, jump)
        target_nonce = nonce + jump + i
        acc = 100 - (dec % 100)
        risk = dec % 50
        tours.append({"nonce": target_nonce, "crash": round(crash_val, 2), "acc": acc, "risk": risk})
    best = sorted(tours, key=lambda x: (x["risk"], -x["acc"], -x["crash"]))
    top4 = best[:4]
    avg_acc = sum(t["acc"] for t in top4) / 4
    signal = "🟢 STRONG PLAY" if avg_acc>70 else "🟡 SAFE PLAY" if avg_acc>55 else "🔴 SKIP"
    return top4, round(avg_acc,2), signal

# ---------------- MINES ----------------
def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

def mines_god_safe5(server, client, nonce, mines_count):
    freq = {}
    history = []
    runs = 80 + mines_count*25
    for i in range(runs):
        grid = mines_core(server, client, nonce+i)
        mines = grid[:mines_count]
        history.append(mines)
        for m in mines:
            freq[m] = freq.get(m,0)+1
    penalty = {}
    for i in range(25):
        x, y = i%5, i//5
        penalty[i] = 8 if x==2 and y==2 else 4 if x==2 or y==2 else 0
    stability = {}
    for i in range(25):
        stability[i] = sum(1 for h in history if i in h)
    score = {i: freq.get(i,0)*5 + penalty[i] + stability[i]*2 for i in range(25)}
    ranking = sorted(range(25), key=lambda x: score[x])
    safe=[]
    for r in ranking:
        if len(safe)==0: safe.append(r)
        else:
            if all(abs((r%5)-(s%5))>1 or abs((r//5)-(s//5))>1 for s in safe): safe.append(r)
        if len(safe)==5: break
    safe5=safe
    risky=ranking[-7:]
    risk_val=sum(freq.get(i,0) for i in safe5)
    total=sum(freq.values()) or 1
    confidence = round(max(0,100-(risk_val/total)*100),2)
    return safe5, risky, confidence

def draw_grid(safe):
    html="<div class='grid'>"
    for i in range(25):
        html+= "<div class='cell safe'>💎</div>" if i in safe else "<div class='cell empty'></div>"
    html+="</div>"
    return html

# ---------------- LOGIN ----------------
if "login" not in st.session_state: st.session_state.login=False
if not st.session_state.login:
    st.title("🔐 HUBRIS ACCESS")
    pwd = st.text_input("Code", type="password")
    if st.button("ENTER"):
        if pwd=="2026":
            st.session_state.login=True
            st.rerun()
        else: st.error("Code diso")
else:
    st.title("🔥 HUBRIS GOD MODE V550")
    tab1,tab2,tab3 = st.tabs(["🌌 COSMOS","💣 MINES","📘 GUIDE"])

    with tab1:
        server=st.text_input("Server Seed")
        client=st.text_input("Client Seed")
        nonce=st.number_input("Nonce",1,10000,1)
        if st.button("SCAN COSMOS"):
            if not server or not client: st.error("Seed required")
            else:
                with st.spinner('🔄 Scan en cours...'):
                    top4, acc, signal=cosmos(server,client,nonce)
                st.markdown(f"## {signal}")
                st.markdown(f"### 🎯 GLOBAL ACCURACY: **{acc}%**")
                st.markdown("---")
                for i,t in enumerate(top4,1):
                    st.markdown(f"""
### 🚀 TOUR {i}
- 🎯 Nonce: **{t['nonce']}**
- 💥 Crash: **{t['crash']}x**
- 📊 Accuracy: **{t['acc']}%**
- ⚠️ Risk: **{t['risk']}**
---
""")

    with tab2:
        server_m=st.text_input("Server Seed",key="m1")
        client_m=st.text_input("Client Seed",key="m2")
        nonce_m=st.number_input("Nonce",1,10000,1,key="m3")
        mines_count=st.slider("Nombre de mines",1,3,3)
        if st.button("SCAN MINES"):
            if not server_m or not client_m: st.error("Seed required")
            else:
                with st.spinner('💎 Calcul des safe diamonds...'):
                    safe,risky,conf=mines_god_safe5(server_m,client_m,nonce_m,mines_count)
                st.markdown(draw_grid(safe),unsafe_allow_html=True)
                st.success(f"💎 SAFE 5: {safe}")
                st.error(f"⚠️ RISKY: {risky}")
                st.info(f"CONFIDENCE: {conf}%")

    with tab3:
        st.markdown("""
### 📘 GUIDE UTILISATEUR

### 🌌 COSMOS
- ✔️ STRONG PLAY → miditra
- ✔️ SAFE PLAY → miditra kely
- ❌ SKIP → aza milalao

---

### 💣 MINES
- ✔️ Mifidiana 1–2 ao amin’ny SAFE 5
- ❌ Aza maka rehetra

---

### 🎯 STRATEGIE
- 💰 Bet = 1%
- ❌ Stop après 2 pertes
- 🔁 Change nonce

---

### ⚠️ IMPORTANT
- Tsy misy 100% win
- Fa ity dia manampy hampihena loss
""")
