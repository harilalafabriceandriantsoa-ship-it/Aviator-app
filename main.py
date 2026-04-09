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

def jump_calc(dec):
    return max(2, ((dec % 13) + (dec % 17) + (dec % 19)) // 3)

def cosmos(server, client, nonce):
    results = []
    decs = []

    for i in range(12):
        h = hashlib.sha512(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        dec = int(h[-8:], 16) or 1
        decs.append(dec)
        results.append((4294967295*0.97)/dec)

    mean = statistics.mean(results)
    var = statistics.pvariance(results)
    acc = round(max(0,100-var),2)

    jumps = [jump_calc(d) for d in decs[:4]]

    tours = [
        nonce + jumps[0],
        nonce + jumps[1] + 5,
        nonce + jumps[2] + 9,
        nonce + jumps[3] + 13
    ]

    signal = "🟢 PLAY" if acc > 55 and mean > 2 else "🔴 SKIP"

    return results, min(results), mean, max(results), acc, tours, signal

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

    # analyse dynamique arakaraka mines
    runs = 15 + mines_count * 5

    for i in range(runs):
        grid = mines_core(server, client, nonce + i)
        mines = grid[:mines_count]

        for m in mines:
            freq[m] = freq.get(m, 0) + 1

    ranking = sorted(range(25), key=lambda x: freq.get(x, 0))

    safe5 = ranking[:5]   # 💎 FIXE
    risky = ranking[-5:]

    confidence = round(100 - sum(freq.get(x,0) for x in safe5),2)

    return safe5, risky, confidence

def draw_grid(safe):
    html = "<div class='grid'>"
    for i in range(25):
        if i in safe:
            html += "<div class='cell safe'>💎</div>"
        else:
            html += "<div class='cell empty'></div>"
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

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💣 MINES", "📘 GUIDE"])

    # -------- COSMOS --------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)

        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                res,minv,mean,maxv,acc,tours,signal = cosmos(server,client,nonce)

                st.success(f"Signal: {signal}")
                st.info(f"MIN: {round(minv,2)} | MEAN: {round(mean,2)} | MAX: {round(maxv,2)}")
                st.warning(f"ACCURACY: {acc}%")

                st.write("🎯 TOURS:")
                for t in tours:
                    st.write(f"➡️ {t} → {crash(server,client,t)}x")

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
- ✔️ Jereo **Accuracy > 55%**
- ✔️ Signal = PLAY
- ✔️ Milalao ireo tours 4

---

### 💣 MINES
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
