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

.stButton>button {
    background: linear-gradient(90deg,#00ffcc,#0066ff);
    color:white;border-radius:10px;height:45px;
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
.safe {background:#00ffcc;color:#000;box-shadow:0 0 15px #00ffcc;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- COSMOS ----------------
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos_precise(server, client, nonce):
    total_hash = 100  # Plus de hash pour précision
    decs = [int(hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).hexdigest()[-8:],16) or 1 for i in range(total_hash)]
    
    # Générer jumps automatiques uniques pour 4 tours
    jumps = []
    used_nonces = set()
    idx = 0
    while len(jumps)<4:
        jump = max(2, ((decs[idx]%7)+(decs[idx]%11)+(decs[idx]%13))//2)
        t_nonce = nonce + jump
        if t_nonce not in used_nonces:
            jumps.append(jump)
            used_nonces.add(t_nonce)
        idx += 1
        if idx >= len(decs):
            idx = 0
    
    tours=[]
    for i,jump in enumerate(jumps):
        t_nonce = nonce + jump
        # Prendre 15 hash autour de la position
        start = i*10
        end = start + 15
        t_decs = decs[start:end] if end <= len(decs) else decs[start:]
        t_results = [(4294967295*0.97)/d for d in t_decs]
        min_val = round(min(t_results),2)
        mean_val = round(statistics.mean(t_results),2)
        max_val = round(max(t_results),2)
        var = statistics.pvariance(t_results)
        acc = round(max(0,100 - var),2)
        t_crash = round((4294967295*0.97)/decs[i],2)
        tours.append({
            "tour": i+1,
            "nonce": t_nonce,
            "crash": t_crash,
            "min": min_val,
            "mean": mean_val,
            "max": max_val,
            "acc": acc
        })
    
    signal = "🟢 PLAY 🎯" if all(t['acc']>55 for t in tours) else "🔴 SKIP ❌"
    return tours, signal

# ---------------- MINES ----------------
def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

def mines_hubris(server, client, nonce, mines_count):
    freq = {}
    runs = 15 + mines_count * 5
    for i in range(runs):
        grid = mines_core(server, client, nonce+i)
        mines = grid[:mines_count]
        for m in mines:
            freq[m] = freq.get(m,0)+1
    ranking = sorted(range(25), key=lambda x: freq.get(x,0))
    safe5 = ranking[:5]
    risky = ranking[-5:]
    confidence = round(100 - sum(freq.get(x,0) for x in safe5),2)
    return safe5, risky, confidence

def draw_grid(safe):
    html = "<div class='grid'>"
    for i in range(25):
        html += "<div class='cell safe'>💎</div>" if i in safe else "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS ACCESS")
    pwd = st.text_input("Code", type="password")
    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Code diso")
else:
    st.title("🔥 HUBRIS GOD MODE V550")
    tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💎 MINES", "📘 GUIDE"])
    
    # -------- COSMOS --------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)
        
        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                with st.spinner("Scanning Cosmos... 🎯"):
                    tours, signal = cosmos_precise(server,client,nonce)
                    st.markdown(f"<h2 style='text-align:center;color:#00ffcc'>{signal}</h2>", unsafe_allow_html=True)
                    cols = st.columns(4)
                    for t, col in zip(tours, cols):
                        with col:
                            st.markdown(f"""
                            <div style='background:#111;color:#00ffcc;padding:10px;border-radius:10px;text-align:center;border:1px solid #00ffcc;'>
                                <h3>🎯 Tour {t['tour']}</h3>
                                <p>Nonce: {t['nonce']}</p>
                                <p>Crash: {t['crash']}x</p>
                                <p>🎯 MIN: {t['min']} | 🎯 MEAN: {t['mean']} | 🎯 MAX: {t['max']}</p>
                                <p>🎯 Accuracy: {t['acc']}%</p>
                            </div>
                            """, unsafe_allow_html=True)
    
    # -------- MINES --------
    with tab2:
        server_m = st.text_input("Server Seed", key="m1")
        client_m = st.text_input("Client Seed", key="m2")
        nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")
        mines_count = st.slider("Nombre de mines", 1, 3, 3)
        
        if st.button("SCAN MINES"):
            if not server_m or not client_m:
                st.error("Seed required")
            else:
                with st.spinner("Scanning Mines..."):
                    safe, risky, conf = mines_hubris(server_m, client_m, nonce_m, mines_count)
                    st.markdown(draw_grid(safe), unsafe_allow_html=True)
                    st.success(f"💎 SAFE 5: {safe}")
                    st.error(f"⚠️ RISKY: {risky}")
                    st.info(f"CONFIDENCE: {conf}%")
    
    # -------- GUIDE --------
    with tab3:
        st.markdown("""
### 📘 GUIDE UTILISATEUR

### 🌌 COSMOS
- ✔️ Variable jumps automatique
- ✔️ MIN / MEAN / MAX crash isaky ny tour 🎯
- ✔️ Accuracy isaky ny tour 🎯
- ✔️ Signal = PLAY raha tours rehetra > 55%
- ✔️ Milalao ireo tours 1→4 🎯

---

### 💎 MINES
- ✔️ Sélection: 1 à 3 mines
- ✔️ Ny système dia mamoaka **5 SAFE 💎**
- ✔️ Safidio **2 ou 3 cases max**

---

### 🎯 STRATEGIE
- 💰 Bet = 1% bankroll
- ❌ Stop après 3 pertes
- 🔁 Reset nonce

---

### ⚠️ IMPORTANT
- Tsy misy algo 100% win
- Ity dia manampy **hampihena loss**
""")
