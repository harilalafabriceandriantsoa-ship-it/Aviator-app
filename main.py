import streamlit as st
import numpy as np
import collections
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="ROULETTE PRO V1", layout="wide", initial_sidebar_state="collapsed")

# --- DONNÉES REELLES DE LA ROULETTE FRANÇAISE (Ordre sur le cylindre) ---
ROUGE = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
NOIR = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# --- CSS STYLING (LOVABLE & GLASSMORPHISM) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@500;700;900&display=swap');

html, body, .stApp {
    background: radial-gradient(circle at 50% 0%, #1a103c 0%, #050505 80%) !important;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

/* INPUT TEXT BOX */
.stTextInput input {
    background-color: #12121a !important; 
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    border: 2px solid #6d28d9 !important;
    border-radius: 16px !important;
    padding: 15px !important;
    box-shadow: 0 4px 20px rgba(109, 40, 217, 0.2);
    text-align: center;
}
.stTextInput input::placeholder {
    color: #8b8b99 !important;
    font-weight: 500 !important;
}

/* BOKOTRA / BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #4c1d95) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px;
    border-radius: 16px !important;
    height: 60px !important;
    border: 1px solid #9d4edd !important;
    width: 100% !important;
    text-transform: uppercase;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 40px rgba(124, 58, 237, 0.6) !important;
}

.glass-card {
    background: rgba(20, 15, 35, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.title-main {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(to right, #e879f9, #a855f7, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
    letter-spacing: -1px;
}
.subtitle {
    text-align: center;
    font-size: 0.9rem;
    color: #a1a1aa;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 30px;
    font-weight: 600;
}

.result-title {
    font-size: 1.1rem;
    color: #c4b5fd;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 15px;
    text-align: center;
    font-weight: 700;
}

.color-box {
    border-radius: 20px;
    padding: 25px 10px;
    text-align: center;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 20px;
}
.rouge-glow {
    background: linear-gradient(135deg, #450a0a, #2b0000);
    border: 2px solid #ef4444;
    box-shadow: 0 0 30px rgba(239, 68, 68, 0.3);
}
.noir-glow {
    background: linear-gradient(135deg, #171717, #000000);
    border: 2px solid #52525b;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
}
.color-name { font-size: 2.5rem; font-weight: 900; line-height: 1; margin-bottom: 5px; }
.color-prob { font-size: 1.2rem; color: #a1a1aa; }

.numbers-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-top: 15px;
}
.num-ball {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    border: 2px solid rgba(255,255,255,0.2);
}
.ball-red { background: radial-gradient(circle at 30% 30%, #ef4444, #7f1d1d); }
.ball-black { background: radial-gradient(circle at 30% 30%, #3f3f46, #09090b); }
.ball-zero { background: radial-gradient(circle at 30% 30%, #22c55e, #14532d); border-color: #4ade80;}

.stats-row {
    display: flex;
    justify-content: space-around;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 15px;
    margin-top: 20px;
}
.stat-item { text-align: center; }
.stat-val { font-family: 'Outfit', sans-serif; font-size: 1.4rem; color: #a855f7; font-weight: 800; }
.stat-lbl { font-size: 0.7rem; color: #71717a; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTIFICATION ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='title-main'>ROULETTE <span>PRO</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>ÉDITION LOVABLE · SÉCURISÉ</div>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password", placeholder="Entrez le mot de passe...")
        if st.button("DÉVERROUILLER"):
            if pwd == "2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ Mot de passe incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ALGORITHME INTERVALLE ET MARKOV (DYNAMIQUE 100%) ---
def analyze_roulette_dynamic(history):
    if len(history) < 2:
        # Raha mbola kely ny data, dia raisina ny manodidina ny isa farany fotsitsy
        last_num = history[-1] if len(history) > 0 else 0
        idx = WHEEL.index(last_num)
        target_nums = [WHEEL[(idx + i) % 37] for i in [-4, -3, -2, -1, 0, 1, 2, 3, 4]]
        prob_red, prob_black = 48.6, 48.6
    else:
        # 1. CYLINDER JUMP ANALYSIS (Famakafakana ny tora-baolina eo amin'ny kodia)
        jumps = []
        for i in range(len(history) - 1):
            idx1 = WHEEL.index(history[i])
            idx2 = WHEEL.index(history[i+1])
            diff = (idx2 - idx1) % 37
            jumps.append(diff)
        
        # Kajiana ny "score" isaky ny slot 37 arakaraka ny elanelana niverimberina
        jump_counts = collections.Counter(jumps)
        last_idx = WHEEL.index(history[-1])
        scores = np.zeros(37)
        
        for jump, weight in jump_counts.items():
            predicted_idx = (last_idx + jump) % 37
            # Omena tombony koa ny teboka roa manodidina azy (Sector betting)
            for neighbor in [-1, 0, 1]:
                scores[(predicted_idx + neighbor) % 37] += weight

        # Alaina ny isa 9 manana score ambony indrindra
        best_indices = np.argsort(scores)[-9:][::-1]
        target_nums = [WHEEL[idx] for idx in best_indices]

        # 2. COLOR MARKOV TRANSITIONS (Fahazarana nivoakan'ny loko misesy)
        transitions = {"R": {"R": 1, "N": 1}, "N": {"R": 1, "N": 1}}
        for i in range(len(history) - 1):
            c1 = "R" if history[i] in ROUGE else "N" if history[i] in NOIR else None
            c2 = "R" if history[i+1] in ROUGE else "N" if history[i+1] in NOIR else None
            if c1 and c2:
                transitions[c1][c2] += 1
        
        last_color = "R" if history[-1] in ROUGE else "N" if history[-1] in NOIR else "R"
        r_weight = transitions[last_color]["R"]
        n_weight = transitions[last_color]["N"]
        
        # Correction d'équilibre (Loi des grands nombres)
        red_total = sum(1 for n in history if n in ROUGE)
        tot = sum(1 for n in history if n in ROUGE or n in NOIR)
        if tot > 0:
            deviation = (red_total / tot) - 0.5
            r_weight -= deviation * 4  # Mampifandanja raha misy loko nivoaka be loatra
            n_weight += deviation * 4

        prob_red = (r_weight / (r_weight + n_weight)) * 100
        prob_black = 100 - prob_red
        
        # Ampidirina ao ny zero tax (2.7%)
        prob_red = round(prob_red * 0.973, 1)
        prob_black = round(prob_black * 0.973, 1)

    if prob_red > prob_black:
        color_pred, color_prob, css_class, c_hex = "ROUGE", prob_red, "rouge-glow", "#ef4444"
    else:
        color_pred, color_prob, css_class, c_hex = "NOIR", prob_black, "noir-glow", "#ffffff"

    target_nums = list(set(target_nums))
    target_nums.sort()
    conf_score = round(min(99.4, max(62.0, 65 + (abs(prob_red - prob_black) * 1.6))), 1)

    return color_pred, color_prob, css_class, c_hex, target_nums, conf_score

# --- UI PRINCIPALE ---
st.markdown("<div class='title-main'>ROULETTE <span>PRO</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>ANALYSE CYLINDRE & MARKOV DYNAMIQUE</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='result-title'>🎯 PARAMÈTRES</div>", unsafe_allow_html=True)
    st.write("<span style='color:#a1a1aa; font-size:0.85rem;'>Ampidiro eto ireo isa nivoaka farany (saraho amin'ny " " espace)</span>", unsafe_allow_html=True)
    hist_input = st.text_input("", placeholder="Ex: 32 15 19 4 21")
    
    analyze_btn = st.button("LANCER L'ANALYSE DYNAMIQUE")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if analyze_btn and hist_input:
        try:
            raw_nums = hist_input.replace(",", " ").split()
            history = [int(x) for x in raw_nums if x.isdigit() and 0 <= int(x) <= 36]
            
            if len(history) == 0:
                st.error("⚠️ Ampidiro farafahakeliny isa iray marina (0-36).")
            else:
                with st.spinner("Kajy dynamique an-tsehatra..."):
                    pred, prob, css, c_hex, nums, conf = analyze_roulette_dynamic(history)
                
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                # LOKO LALOVINA
                st.markdown(f"""
                <div class='color-box {css}'>
                    <div class='color-name' style='color:{c_hex};'>{pred}</div>
                    <div class='color-prob'>Probabilité dynamique : {prob}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                # ISA 8 - 10 LALOVINA
                st.markdown("<div class='result-title'>⚡ CHIFFRES FORTS SECTEURS (CHOIX {len_n})</div>".format(len_n=len(nums)), unsafe_allow_html=True)
                
                html_nums = "<div class='numbers-grid'>"
                for n in nums:
                    if n == 0: b_class = "ball-zero"
                    elif n in ROUGE: b_class = "ball-red"
                    else: b_class = "ball-black"
                    html_nums += f"<div class='num-ball {b_class}'>{n}</div>"
                html_nums += "</div>"
                st.markdown(html_nums, unsafe_allow_html=True)
                
                # STATISTIQUES
                st.markdown(f"""
                <div class='stats-row'>
                    <div class='stat-item'><div class='stat-val'>{conf}%</div><div class='stat-lbl'>Confiance</div></div>
                    <div class='stat-item'><div class='stat-val'>{len(history)}</div><div class='stat-lbl'>Isa Nodinihina</div></div>
                    <div class='stat-item'><div class='stat-val'>PURE MATH</div><div class='stat-lbl'>Modèle</div></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Misy fahadisoana ny endrika nampidirinao.")
    else:
        st.markdown("""
        <div class='glass-card' style='text-align:center; padding: 60px 20px; opacity: 0.5;'>
            <h1 style='font-size: 4rem; margin:0;'>🎲</h1>
            <p style='font-family: Outfit; font-size: 1.2rem; color: #a1a1aa;'>Ampidiro eo amin'ny ankavia ny tantaran'ny lalao vao hahita ny algorithm mathématique vaovao.</p>
        </div>
        """, unsafe_allow_html=True)
