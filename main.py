import streamlit as st
import hashlib
import random
import statistics

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS GOD MODE V500", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
    color: #00ffcc;
}
h1, h2, h3 {text-align:center;color:#00ffcc;}

.stButton>button {
    background: linear-gradient(90deg,#00ffcc,#0066ff);
    color:white;border-radius:10px;height:45px;
}

.grid {
    display:grid;
    grid-template-columns:repeat(5,60px);
    gap:10px;
    justify-content:center;
    margin-top:20px;
}
.cell {
    width:60px;height:60px;
    display:flex;align-items:center;justify-content:center;
    border-radius:10px;
    font-size:22px;
}
.safe {background:#00ffcc;color:#000;box-shadow:0 0 15px #00ffcc;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- COSMOS ENGINE ----------------

def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16)
    if dec == 0: dec = 1
    return round((4294967295 * 0.97) / dec, 2), dec

def extract_jump(dec):
    # jump tena avy amin’ny hash
    a = dec % 13
    b = (dec >> 8) % 17
    c = (dec >> 16) % 19
    return max(2, (a + b + c) // 3)

def cosmos_hubris(server, client, nonce):
    results = []
    decimals = []

    for i in range(12):
        r, d = crash(server, client, nonce + i)
        results.append(r)
        decimals.append(d)

    jumps = []
    for d in decimals[:4]:
        jumps.append(extract_jump(d))

    tours = [
        nonce + jumps[0],
        nonce + jumps[1] + 3,
        nonce + jumps[2] + 7,
        nonce + jumps[3] + 11
    ]

    mean = statistics.mean(results)
    var = statistics.pvariance(results)
    acc = round(max(0, 100 - var), 2)

    signal = "🟢 PLAY" if acc > 55 and mean > 2 else "🔴 SKIP"

    return {
        "results": results,
        "min": round(min(results),2),
        "max": round(max(results),2),
        "mean": round(mean,2),
        "acc": acc,
        "tours": tours,
        "signal": signal
    }

# ---------------- MINES ENGINE ----------------

def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

def mines_hubris(server, client, nonce):
    freq = {}

    # multi analyse
    for i in range(20):
        grid = mines_core(server, client, nonce + i)
        mines = grid[:3]
        for m in mines:
            freq[m] = freq.get(m, 0) + 1

    # SAFE = ireo tsy miseho matetika
    ranking = sorted(range(25), key=lambda x: freq.get(x, 0))

    safe5 = ranking[:5]  # 💎 FIXE 5 DIAMANT
    risky = ranking[-5:]

    confidence = round(100 - sum(freq.get(x,0) for x in safe5), 2)

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
    code = st.text_input("Code", type="password")
    if st.button("ENTER"):
        if code == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Diso")
else:

    st.title("🔥 HUBRIS GOD MODE V500")

    tab1, tab2 = st.tabs(["🌌 COSMOS", "💣 MINES"])

    # ---------------- COSMOS UI ----------------
    with tab1:
        st.subheader("COSMOS ULTRA")
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)

        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                data = cosmos_hubris(server, client, nonce)

                st.write("Résultats:", data["results"])
                st.success(f"Signal: {data['signal']}")
                st.info(f"MIN: {data['min']} | MEAN: {data['mean']} | MAX: {data['max']}")
                st.warning(f"ACCURACY: {data['acc']}%")

                st.write("🎯 TOURS À JOUER:")
                for t in data["tours"]:
                    r,_ = crash(server, client, t)
                    st.write(f"➡️ Tour {t} → {r}x")

    # ---------------- MINES UI ----------------
    with tab2:
        st.subheader("MINES HUBRIS 💎")

        server_m = st.text_input("Server Seed", key="m1")
        client_m = st.text_input("Client Seed", key="m2")
        nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")

        if st.button("SCAN MINES"):
            if not server_m or not client_m:
                st.error("Seed required")
            else:
                safe, risky, conf = mines_hubris(server_m, client_m, nonce_m)

                st.markdown(draw_grid(safe), unsafe_allow_html=True)

                st.success(f"💎 SAFE 5: {safe}")
                st.error(f"⚠️ RISKY: {risky}")
                st.info(f"CONFIDENCE: {conf}%")
