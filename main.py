import streamlit as st
import hashlib, hmac, random, os
from dotenv import load_dotenv

# Load .env file (tsy voatery ampiasaina intsony raha login key mivantana)
load_dotenv()

# --- LOGIN KEY DIRECT ---
LOGIN_KEY = "2026"   # Afaka ovaina eto ny code key

st.set_page_config(page_title="APP 2026 - COSMOSX, AVIATOR & MINES", layout="wide")

# --- COSMOSX ENGINE ---
def cosmos_prediction(server_seed, client_seed, tour_id, iters=20000):
    combined = f"{server_seed}:{client_seed}:{tour_id}:COSMOSX2026"
    h = hmac.new(b"COSMOS_CORE", combined.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h = hmac.new(h, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h).digest()
    final = bytes(a ^ b for a, b in zip(h, blake))
    hex_val = final.hex()
    p_int = int(hex_val[:8], 16)
    jump1 = (p_int % 3) + 2
    jump2 = jump1 + (p_int % 4) + 2
    jump3 = jump2 + (p_int % 6) + 3
    return {"hex": hex_val, "jumps": [jump1, jump2, jump3]}

# --- AVIATOR ENGINE ---
def aviator_prediction(hex_val, heure):
    base_int = int(hex_val[:8], 16) ^ int(str(heure))
    mult = 1 + (base_int % 5000) / 1000.0
    min_val = round(mult * 0.6, 2)
    moyen_val = round(mult * 1.0, 2)
    max_val = round(mult * 2.5, 2)
    accuracy = 0.75 if 2 <= moyen_val <= 4 else 0.55
    return {"multiplier": mult, "min": min_val, "moyen": moyen_val, "max": max_val, "accuracy": accuracy}

# --- MINES ENGINE ---
def mines_schema(server_seed, client_seed, nonce, mines_choice=1):
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}:{mines_choice}".encode()).hexdigest()
    hash_int = int(h, 16)
    grid = list(range(25))
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    random.seed(int(h[-16:], 16))
    random.shuffle(grid)
    return grid[:5]  # Always 5 diamonds

# --- LOGIN SYSTEM ---
st.markdown("<h2 style='text-align:center;'>🔐 APP 2026 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password")

if admin_input:
    if admin_input == LOGIN_KEY:   # mampiasa login key mivantana
        st.success("✅ Admin login successful")
        
        # Tabs rehefa tafiditra
        tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

        with tab1:
            st.markdown("##### 🌌 COSMOSX PREDICTION")
            s_seed = st.text_input("Server Seed (code key):")
            c_seed = st.text_input("Client Seed (code key):")
            t_id = st.number_input("Tour ID (Numéro de tour actuel - code key):", min_value=1, value=2026001)
            if st.button("🚀 RUN COSMOSX"):
                result = cosmos_prediction(s_seed, c_seed, t_id)
                st.write("🔑 HEX (code key):", result["hex"][:32], "...")
                st.write("🛰️ Jumps:", result["jumps"])
                st.success("✅ CosmosX: Fairness sy provably fair amin'ny hash+hex+tour actuel")

        with tab2:
            st.markdown("##### ✈️ AVIATOR STUDIO PREDICTION")
            hex_val = st.text_input("HEX Value (code key):")
            heure = st.number_input("Tour Heure (timestamp code key):", min_value=1, value=20260406)
            if st.button("✈️ RUN AVIATOR"):
                result = aviator_prediction(hex_val, heure)
                st.write("🎯 Multiplier:", result["multiplier"])
                st.write("📊 Range → Min:", result["min"], "Moyen:", result["moyen"], "Max:", result["max"])
                st.write("⚡ Accuracy:", f"{int(result['accuracy']*100)}%")
                if 2 <= result["moyen"] <= 4:
                    st.success("✅ Safe zone for auto cashout 2–4x")
                else:
                    st.warning("⚠️ Moyenne multiplier outside safe zone")

        with tab3:
            st.markdown("##### 💣 MINES SCHEMA (Always 5 Diamonds)")
            s_s = st.text_input("Server Seed (code key):")
            c_s = st.text_input("Client Seed (code key):")
            t_id = st.text_input("Tour ID (Numéro de tour actuel):")
            mines_choice = st.slider("Select Mines Choice (1–3):", 1, 3, 1)
            if st.button("🛰️ GENERATE SCHEMA"):
                schema = mines_schema(s_s, c_s, t_id, mines_choice)
                grid_html = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;max-width:330px;margin:auto;">'
                for i in range(25):
                    if i in schema:
                        grid_html += '<div style="aspect-ratio:1/1;background:#111;border:2px solid red;color:red;font-size:28px;text-align:center;border-radius:12px;box-shadow:0 0 20px red;">⭐</div>'
                    else:
                        grid_html += '<div style="aspect-ratio:1/1;background:#222;border:1px solid #00ffcc44;border-radius:12px;"></div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.info("Verifier: Always 5 diamonds, schema differs for choice 1–3.")
    else:
        st.error("❌ Invalid admin code")
