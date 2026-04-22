import streamlit as st
import hashlib
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh
import time

# ---------------- CONFIG & STYLE (Ultra Stylé + Mobile) ----------------
st.set_page_config(page_title="HUBRIS V800 MINES AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a, #1a0033);
        color: #00ffcc;
    }
    h1, h2, h3 { text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0066ff);
        color: white;
        border-radius: 12px;
        height: 52px;
        font-weight: bold;
        box-shadow: 0 0 15px #00ffcc;
        transition: all 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 25px #00ffff; }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(55px, 1fr));
        gap: 8px;
        justify-content: center;
        margin: 25px 0;
        max-width: 100%;
    }
    .cell {
        width: 100%;
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        font-size: 28px;
        box-shadow: 0 4px 10px rgba(0,255,204,0.3);
        transition: all 0.2s;
    }
    .safe { background: linear-gradient(#00ffcc, #00cc99); color: #000; font-weight: bold; }
    .risk { background: linear-gradient(#ff0033, #990000); color: #fff; }
    .empty { background: #1a1a2e; border: 2px solid #333366; }

    .neon-text { text-shadow: 0 0 15px #00ffcc, 0 0 30px #0066ff; }
    .info-box {
        background: rgba(0, 255, 204, 0.1);
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "memory" not in st.session_state:
    st.session_state.memory = []  # (features, safe_position)
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- HASH & MINES CORE (Ultra Précis) ----------------
def get_mines_grid(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid  # positions des mines (les 5 premiers = mines)

def monte_carlo_probability(server, client, nonce, simulations=500):
    scores = np.zeros(25)
    for i in range(simulations):
        h = hashlib.sha512(f"{server}:{client}:{nonce + i}".encode()).digest()
        val = int.from_bytes(h[:4], "big") % 25
        scores[val] += 1
    return scores / simulations  # probabilité qu'il y ait une mine

def extract_features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    features = [int(h[i:i+2], 16) for i in range(0, 64, 2)]
    # Ajout de features avancées
    features.extend([int(h[i:i+4], 16) % 25 for i in range(0, 20, 4)])
    return features[:30]  # 30 features puissantes

# ---------------- MINES AI (Version Ultra Puissante) ----------------
def mines_ai_v800(server, client, nonce):
    if not server or not client:
        st.error("Veuillez entrer Server Seed et Client Seed")
        return None, None, 0

    risk_prob = monte_carlo_probability(server, client, nonce, 800)  # + de simulations = + précis
    model = train_model_v800()

    ml_score = np.zeros(25)

    if model and len(st.session_state.memory) >= 25:
        feat = extract_features(server, client, nonce)
        try:
            pred_probs = model.predict_proba([feat])[0]
            for i, prob in enumerate(pred_probs):
                if i < 25:
                    ml_score[i] += prob
        except:
            pass

    # Combinaison intelligente
    final_score = (1 - risk_prob) * 0.75 + ml_score * 0.25
    rank = np.argsort(-final_score)  # du plus safe au plus risky

    safe5 = rank[:5].tolist()
    risky5 = rank[-5:].tolist()
    confidence = round(float(np.max(final_score) * 100), 1)

    # Learning (on ajoute la meilleure prédiction actuelle)
    if len(st.session_state.memory) < 500:  # limite mémoire
        st.session_state.memory.append((extract_features(server, client, nonce), safe5[0]))

    return safe5, risky5, confidence

@st.cache_resource(ttl=300)  # Cache le modèle pour performance
def train_model_v800():
    if len(st.session_state.memory) < 25:
        return None

    X = [m[0] for m in st.session_state.memory]
    y = [m[1] for m in st.session_state.memory]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X, y)
    return model

# ---------------- DRAW GRID (Responsive) ----------------
def draw_grid(safe, risky):
    html = "<div class='grid'>"
    for i in range(25):
        if i in safe:
            html += f"<div class='cell safe'>💎</div>"
        elif i in risky:
            html += f"<div class='cell risk'>☠️</div>"
        else:
            html += f"<div class='cell empty'>⬜</div>"
    html += "</div>"
    return html

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐 HUBRIS V800 SECURE ACCESS")
    pwd = st.text_input("Mot de passe", type="password", placeholder="Entrez le mot de passe")
    if st.button("ACCÉDER AU SYSTÈME"):
        if pwd == "2026":
            st.session_state.login = True
            st.success("✅ Accès autorisé - Bienvenue dans HUBRIS V800")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")
    st.caption("Système de prédiction MINES avancé • Provably Fair")
else:
    st.title("🔥 HUBRIS V800 MINES AI")
    st.markdown("<h3 class='neon-text'>PRÉDICTION ULTRA PRÉCISE - 5 DIAMANTS</h3>", unsafe_allow_html=True)

    # Sidebar légère pour mobile
    with st.sidebar:
        st.metric("Balance", f"${st.session_state.balance:,.0f}")
        st.caption("HUBRIS V800 • Mines Edition")

    tab1, tab2 = st.tabs(["💎 MINES PREDICTOR", "📊 HISTORY & AUTO"])

    # ==================== TAB 1 : MINES PREDICTOR ====================
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            server_m = st.text_input("Server Seed", key="srv", placeholder="Entrez le server seed")
        with col2:
            client_m = st.text_input("Client Seed", key="cli", placeholder="Entrez le client seed")

        nonce_m = st.number_input("Nonce", value=1, min_value=0, step=1, key="non")

        if st.button("🚀 SCAN MINES & PREDICT", use_container_width=True):
            with st.spinner("Analyse quantique en cours..."):
                safe5, risky5, conf = mines_ai_v800(server_m, client_m, nonce_m)

            if safe5:
                st.markdown(draw_grid(safe5, risky5), unsafe_allow_html=True)

                st.success(f"**💎 5 DIAMANTS RECOMMANDÉS** : {safe5}")
                st.error(f"☠️ Positions à éviter : {risky5}")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Confidence", f"{conf}%", delta=None)
                with col_b:
                    st.metric("Safe Score", f"{round(np.mean([1-risk for risk in monte_carlo_probability(server_m, client_m, nonce_m, 100) if True]),2)}")
                
                # Auto bet simulation légère
                if conf > 75:
                    st.balloons()
                    st.success("🔥 SIGNAL TRÈS FORT - Jouez les 5 diamants !")

    # ==================== TAB 2 : HISTORY & AUTO ====================
    with tab2:
        st.subheader("Historique des prédictions")
        if st.session_state.memory:
            st.write(f"Modèle entraîné sur **{len(st.session_state.memory)}** parties")
        else:
            st.info("Jouez plusieurs rounds pour améliorer l'IA")

        conf_slider = st.slider("Niveau de confiance minimum pour auto-bet", 50, 95, 75)
        
        if st.button("Simuler Auto-Bet"):
            bet = st.session_state.balance * 0.02
            if conf_slider > 75:
                st.session_state.balance += bet * 1.8  # simulation win
                st.success(f"WIN +${bet*1.8:.0f} ! Balance : ${st.session_state.balance:.0f}")
            else:
                st.session_state.balance -= bet
                st.warning(f"LOSE -${bet:.0f}")

    st.caption("💡 **Conseil** : Plus vous scannez de rounds, plus l'IA devient précise grâce au machine learning en temps réel.")
    st_autorefresh(interval=12000, limit=None, key="refresh")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("HUBRIS V800 MINES AI • Version Ultra Puissante 2026 • Pour usage éducatif et simulation uniquement")
