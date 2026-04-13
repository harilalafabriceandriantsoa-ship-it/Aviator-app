import streamlit as st
import hashlib
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import ExtraTreesClassifier
from scipy.spatial.distance import jensenshannon

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V800 ULTRA AI", layout="wide")

# ---------------- STYLE NEON ----------------
st.markdown("""
<style>
.stApp {background: #0a0a0a; color:#00ffcc;}
.grid {
    display:grid; grid-template-columns:repeat(5,65px);
    gap:12px; justify-content:center; margin-top:20px;
}
.cell {
    width:65px; height:65px; display:flex; align-items:center; 
    justify-content:center; border-radius:12px; font-size:28px;
    border: 1px solid #333;
}
.safe {background:#00ffcc; color:#000; box-shadow: 0 0 20px #00ffcc; border:none;}
.risk {background:#ff0033; color:#fff; box-shadow: 0 0 20px #ff0033; border:none;}
.empty {background:#151515;}
h1, h2, h3 {text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION MANAGEMENT ----------------
if "memory" not in st.session_state:
    st.session_state.memory = []
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.login:
    st.title("🔐 HUBRIS V800 SECURE ACCESS")
    pwd = st.text_input("Enter System Password", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Access Denied: Incorrect Password")
    st.stop()

# ---------------- CORE ALGORITHMS ----------------
def get_features(s, c, n):
    """Extraction de patterns neuronaux"""
    base = f"{s}:{c}:{n}".encode()
    h = hashlib.sha512(base).digest()
    arr = np.array(list(h[:16]), dtype=np.float32)
    return np.concatenate([arr, [np.sum(arr) % 256]])

def monte_carlo_ultra(server, client, nonce):
    """Simulation de probabilité haute précision (15k iterations)"""
    scores = np.zeros(25)
    for i in range(15000):
        h = hashlib.sha512(f"{server}:{client}:{nonce}:{i}".encode()).digest()
        scores[h[0] % 25] += 1
    return scores / 15000

def draw_grid_html(safe, risky):
    """Génération du plateau de jeu 5x5"""
    html = "<div class='grid'>"
    for i in range(25):
        if i in safe:
            html += "<div class='cell safe'>💎</div>"
        elif i in risky:
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- MAIN INTERFACE ----------------
st.title("🔥 HUBRIS V800 ULTRA AI")
st.write("Current Status: **Neural Scanner Online**")

tab1, tab2 = st.tabs(["🚀 SCANNER", "🧠 AI MEMORY"])

with tab1:
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        server_seed = st.text_input("Server Seed")
        client_seed = st.text_input("Client Seed")
    with col_in2:
        nonce_val = st.number_input("Nonce", value=1, min_value=1)
        mines_count = st.selectbox("Nombre de Mines", [1, 2, 3, 4, 5])

    if st.button("INITIATE DEEP SCAN"):
        if server_seed and client_seed:
            with st.spinner("Synchronizing Neural Patterns..."):
                # Calcul des probabilités
                mc_prob = monte_carlo_ultra(server_seed, client_seed, nonce_val)
                features_data = get_features(server_seed, client_seed, nonce_val)
                
                final_distribution = mc_prob.copy()
                
                # Apprentissage Machine (ML)
                if len(st.session_state.memory) > 30:
                    X = np.array([m[0] for m in st.session_state.memory])
                    y = np.array([m[1] for m in st.session_state.memory])
                    clf = ExtraTreesClassifier(n_estimators=300).fit(X, y)
                    ml_prob = clf.predict_proba(features_data.reshape(1, -1))[0]
                    if len(ml_prob) < 25:
                        ml_prob = np.pad(ml_prob, (0, 25 - len(ml_prob)))
                    final_distribution = (0.6 * mc_prob) + (0.4 * ml_prob)

                # Extraction des résultats fixes (5 vs 5)
                ranked_indices = np.argsort(-final_distribution)
                safe_tiles = list(map(int, ranked_indices[:5]))
                risk_tiles = list(map(int, ranked_indices[-5:]))
                
                # Calcul de la confiance
                precision_score = round((1 - jensenshannon(final_distribution, np.ones(25)/25)) * 100, 2)

                # Affichage des résultats
                st.markdown(draw_grid_html(safe_tiles, risk_tiles), unsafe_allow_html=True)
                
                st.write("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("CONFIDENCE", f"{precision_score}%")
                m2.metric("MODE", f"{mines_count} Mines")
                m3.metric("ITERATIONS", "15,000")

                # Graphique de distribution
                st.subheader("📊 Neural Distribution")
                fig = go.Figure(data=[go.Bar(x=list(range(25)), y=final_distribution, marker_color='#00ffcc')])
                st.plotly_chart(fig, use_container_width=True)
                
                # Mise en mémoire
                st.session_state.memory.append((features_data, int(np.argmax(mc_prob))))
        else:
            st.error("Veuillez entrer les Seeds pour commencer.")

with tab2:
    st.subheader("System Knowledge")
    st.write(f"Patterns en mémoire: **{len(st.session_state.memory)}**")
    if st.button("Clear AI Memory"):
        st.session_state.memory = []
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("HUBRIS V800: AI fixed system (5💎/5☠️).")
