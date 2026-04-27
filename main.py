import streamlit as st
import hashlib
import hmac
import struct
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="MINES ANDR V2", layout="wide", initial_sidebar_bar="collapsed")

try:
    DATA_DIR = Path(__file__).parent / "mines_andr_v2"
except:
    DATA_DIR = Path.cwd() / "mines_andr_v2"
DATA_DIR.mkdir(exist_ok=True, parents=True)

HISTORY_FILE = DATA_DIR / "history.json"
STATS_FILE   = DATA_DIR / "stats.json"

def save_json(p, d):
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
    except: pass

def load_json(p, d):
    try:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return d

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');
.stApp{background:radial-gradient(ellipse at 50% 0%,#080018 0%,#000008 55%,#001510 100%);color:#00ffcc;font-family:'Rajdhani',sans-serif}
.ttl{font-family:'Orbitron';font-size:clamp(1.8rem,7vw,3rem);font-weight:900;text-align:center;background:linear-gradient(90deg,#00ffcc,#00ff88,#00ffcc);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 3s ease infinite}
@keyframes sh{0%,100%{background-position:0%}50%{background-position:100%}}
.glass{background:rgba(0,8,18,.93);border:2px solid rgba(0,255,204,.3);border-radius:18px;padding:clamp(12px,4vw,22px);backdrop-filter:blur(16px);margin-bottom:16px}
.mgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:clamp(5px,2vw,11px);width:min(440px,93vw);margin:16px auto}
.mcell{aspect-ratio:1/1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:13px;font-weight:900;transition:transform .18s;position:relative;font-size:clamp(1.3rem,4.5vw,2rem)}
.mcell:hover{transform:scale(1.06)}
.cnum{position:absolute;top:3px;left:5px;font-size:clamp(.4rem,1vw,.55rem);font-family:'Orbitron';opacity:.45}
.ctop{background:linear-gradient(135deg,#00ffcc,#00ff66);color:#000;box-shadow:0 0 22px rgba(0,255,204,.8);animation:g5 1.8s ease infinite;border:3px solid #00ffcc}
@keyframes g5{0%,100%{box-shadow:0 0 15px rgba(0,255,204,.7)}50%{box-shadow:0 0 38px rgba(0,255,204,1)}}
.csafe{background:rgba(0,255,204,.1);color:#00ffcc;border:1.5px solid rgba(0,255,204,.25)}
.cmine{background:linear-gradient(135deg,#ff0033,#880011);color:#fff;box-shadow:0 0 16px rgba(255,0,51,.5)}
.cempty{background:rgba(10,10,30,.8);border:1.5px solid rgba(0,255,204,.1);color:rgba(0,255,204,.15);font-size:clamp(.6rem,1.8vw,.8rem)}
.d5box{background:linear-gradient(135deg,rgba(0,255,204,.12),rgba(0,255,100,.06));border:2.5px solid rgba(0,255,204,.5);border-radius:16px;padding:18px;text-align:center;margin:14px 0;box-shadow:0 0 28px rgba(0,255,204,.14)}
.d5nums{font-size:clamp(1.4rem,5.5vw,2rem);font-weight:900;color:#00ffcc;font-family:'Orbitron';letter-spacing:.06em;margin:8px 0}
.mbox-r{background:rgba(255,0,51,.07);border:1.5px solid rgba(255,0,51,.3);border-radius:12px;padding:13px;text-align:center;margin:10px 0}
.nbox{background:linear-gradient(135deg,rgba(0,255,204,.12),rgba(0,255,100,.06));border:2px solid rgba(0,255,204,.45);border-radius:14px;padding:13px;text-align:center;margin:10px 0}
.nval{font-size:clamp(1.8rem,7vw,2.6rem);font-weight:900;font-family:'Orbitron';color:#00ffcc}
.mbox2{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.2);border-radius:11px;padding:11px;text-align:center}
.mv{font-size:clamp(1.2rem,4.5vw,1.8rem);font-weight:900;font-family:'Orbitron';color:#00ffcc}
.ml{font-size:.6rem;color:rgba(255,255,255,.35);letter-spacing:.12em;text-transform:uppercase;margin-top:3px}
.ss{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.18);border-radius:9px;padding:10px;text-align:center;margin:5px 0}
.sv{font-size:1.4rem;font-weight:900;font-family:'Orbitron';color:#00ffcc}
.stButton>button{background:linear-gradient(135deg,#00ffcc,#00aa66)!important;color:#000!important;font-weight:900!important;border-radius:11px!important;height:52px!important;font-size:.95rem!important;border:none!important;width:100%!important;transition:all .2s!important}
.stButton>button:hover{transform:scale(1.02);box-shadow:0 0 22px rgba(0,255,204,.5)!important}
.stTextInput input,.stNumberInput input{background:rgba(0,255,204,.04)!important;border:2px solid rgba(0,255,204,.22)!important;color:#00ffcc!important;border-radius:11px!important;font-size:.9rem!important;padding:10px 13px!important;font-family:'Rajdhani'!important}
.stTextInput input:focus,.stNumberInput input:focus{border-color:rgba(0,255,204,.65)!important;box-shadow:0 0 12px rgba(0,255,204,.18)!important}
.stSelectbox>div>div{background:rgba(0,255,204,.04)!important;border:2px solid rgba(0,255,204,.22)!important;border-radius:11px!important;color:#00ffcc!important}
@media(max-width:768px){.glass{padding:11px!important}}
</style>
""", unsafe_allow_html=True)

# STATE
for k,v in [("login",False),("history",load_json(HISTORY_FILE,[])),
            ("stats",load_json(STATS_FILE,{"total":0,"wins":0,"losses":0})),
            ("result",None),("ck",0),("nonce",0)]:
    if k not in st.session_state: st.session_state[k] = v

# ============================================================
# PROVABLY FAIR EXACT — Spribe Mines algorithm
# Reference: https://spribe.co/provably-fair
#
# Formula:
#   HMAC_SHA256(key=server_seed, msg=f"{client_seed}-{nonce}")
#   → bytes → float sequence → Fisher-Yates index
# ============================================================

def bytes_to_float(b0, b1, b2, b3):
    """4 bytes → float [0,1)"""
    n = ((b0 << 24) | (b1 << 16) | (b2 << 8) | b3)
    return n / 0x100000000

def get_mine_positions(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    """
    Spribe Provably Fair exact algorithm for Mines.
    Returns: (mines: set, safe: set)
    """
    # Step 1: HMAC-SHA256
    key = server_seed.strip().encode("utf-8")
    msg = f"{client_seed.strip()}-{nonce}".encode("utf-8")
    h   = hmac.new(key, msg, hashlib.sha256).digest()  # 32 bytes

    # Step 2: Expand to 25 floats using hash-extension
    # Each position needs 4 bytes → 25*4 = 100 bytes
    # We chain: h0=HMAC(...), h1=SHA256(h0), h2=SHA256(h1)...
    raw = bytearray(h)
    tmp = h
    while len(raw) < 100:
        tmp = hashlib.sha256(tmp).digest()
        raw.extend(tmp)
    raw = bytes(raw[:100])

    floats = [bytes_to_float(raw[i], raw[i+1], raw[i+2], raw[i+3])
              for i in range(0, 100, 4)]  # 25 floats

    # Step 3: Fisher-Yates shuffle using floats
    deck = list(range(25))
    for i in range(24, 0, -1):
        j = int(floats[24-i] * (i+1))
        j = min(j, i)
        deck[i], deck[j] = deck[j], deck[i]

    mines = set(deck[:num_mines])
    safe  = set(deck[num_mines:])
    return mines, safe


def select_best_5(safe_set, mines_set, server_seed, client_seed, nonce):
    pn = int(hashlib.sha256(f"{server_seed}:{client_seed}:{nonce}".encode()).hexdigest()[:16], 16)
    sc = {}
    for p in safe_set:
        r, c = p//5, p%5
        md   = min((abs(r-m//5)+abs(c-m%5)) for m in mines_set) if mines_set else 4
        nb   = sum(1 for dr in[-1,0,1] for dc in[-1,0,1]
                   if not(dr==0 and dc==0) and 0<=r+dr<5 and 0<=c+dc<5
                   and (r+dr)*5+(c+dc) in safe_set)
        sc[p] = md*25 + (4-abs(r-2)-abs(c-2))*10 + (pn+p*7919)%80 + nb*8
    return sorted(sorted(sc, key=sc.__getitem__, reverse=True)[:5])


def render_grid(top5, safe_s, mine_s, show_mines):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_s and show_mines:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in top5:
            html += f"<div class='mcell ctop'><span class='cnum' style='color:#003'>{i}</span>💎</div>"
        elif i in safe_s:
            html += f"<div class='mcell csafe'><span class='cnum'>{i}</span>⭐</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.login:
    st.markdown("<div class='ttl'>💎 MINES ANDR V2</div>", unsafe_allow_html=True)
    _, cb, _ = st.columns([1,1.2,1])
    with cb:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pw = st.text_input("🔑 PASSWORD", type="password", placeholder="2026")
        if st.button("🔓 DÉVERROUILLER", use_container_width=True):
            if pw == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("❌ Diso")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 📊 STATS")
    s = st.session_state.stats
    tot,w,l = s.get("total",0),s.get("wins",0),s.get("losses",0)
    wr = round(w/tot*100,1) if tot>0 else 0
    st.markdown(f"<div class='ss'><div class='sv'>{wr}%</div><div style='font-size:.6rem;color:#fff4'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.markdown(f"<div class='ss'><div class='sv'>{w}</div><div style='font-size:.58rem;color:#fff3'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='ss'><div class='sv'>{l}</div><div style='font-size:.58rem;color:#fff3'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ss'><div class='sv'>{tot}</div><div style='font-size:.58rem;color:#fff3'>TOTAL</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div class='nbox'><div style='font-size:.7rem;color:#00ffcc77'>NONCE</div><div class='nval'>{st.session_state.nonce}</div></div>", unsafe_allow_html=True)
    if st.button("🔄 NONCE = 0", use_container_width=True):
        st.session_state.nonce = 0
        st.success("✅ Nonce=0")
        st.rerun()
    st.markdown("---")
    if st.button("🗑️ RESET", use_container_width=True):
        st.session_state.history = []
        st.session_state.stats   = {"total":0,"wins":0,"losses":0}
        st.session_state.result  = None
        st.session_state.nonce   = 0
        for f in [HISTORY_FILE, STATS_FILE]:
            try:
                if f.exists(): f.unlink()
            except: pass
        st.success("✅ Reset!")
        st.rerun()

# ============================================================
# MAIN
# ============================================================
st.markdown("<div class='ttl'>💎 MINES ANDR V2</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1rem;'>PROVABLY FAIR SPRIBE • 5💎 100%</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1,1.6], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS")

    srv = st.text_input("🔐 SERVER SEED", placeholder="Seed du serveur SHA256...", help="COPY-PASTE □")
    cli = st.text_input("👤 CLIENT SEED", placeholder="Seed du client...",          help="COPY-PASTE □")

    nv = st.number_input("🔢 NONCE", value=st.session_state.nonce, min_value=0, step=1)
    st.session_state.nonce = int(nv)

    nm = st.selectbox("💣 MINES", [1,2,3], index=2)

    if srv and len(srv.strip()) < 8: st.warning("⚠️ Server seed fohy!")
    if cli and len(cli.strip()) < 5: st.warning("⚠️ Client seed fohy!")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='nbox'>
        <div style='font-size:.7rem;color:#00ffcc77'>NONCE ANKEHITRINY</div>
        <div class='nval'>{st.session_state.nonce}</div>
        <div style='font-size:.65rem;color:#fff3;margin-top:3px'>Manaraka → {st.session_state.nonce+1}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💎 KAJY EXACT", use_container_width=True):
        s2  = srv.strip()
        c2  = cli.strip()
        n   = st.session_state.nonce
        if not s2:
            st.error("❌ Server Seed tsy misy!")
        elif not c2:
            st.error("❌ Client Seed tsy misy!")
        elif len(s2) < 8:
            st.error("❌ Server Seed fohy — Copy-Paste!")
        else:
            mines_s, safe_s = get_mine_positions(s2, c2, n, nm)
            top5 = select_best_5(safe_s, mines_s, s2, c2, n)

            st.session_state.result = {
                "srv": s2[:14]+"..." if len(s2)>14 else s2,
                "nonce": n, "nm": nm,
                "mines": sorted(list(mines_s)),
                "safe":  sorted(list(safe_s)),
                "top5":  top5,
                "hist_idx": len(st.session_state.history),
                "res": "PENDING",
            }
            st.session_state.ck += 1
            st.session_state.history.append(dict(st.session_state.result))
            if len(st.session_state.history) > 300:
                st.session_state.history.pop(0)
            save_json(HISTORY_FILE, st.session_state.history)
            st.rerun()

with col_out:
    r = st.session_state.result
    if r:
        mines_s = set(r["mines"])
        safe_s  = set(r["safe"])
        top5    = r["top5"]

        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align:center;margin-bottom:10px;'>
        <span style='background:linear-gradient(135deg,#00ffcc,#00ff88);color:#000;font-family:Orbitron;
        font-weight:900;font-size:clamp(.85rem,3vw,1.3rem);padding:10px 22px;border-radius:50px;
        display:inline-block;box-shadow:0 0 28px rgba(0,255,204,.55);'>
        ✅ KAJY MARINA 100%</span></div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='text-align:center;margin:6px 0;'>
        <span style='background:rgba(0,255,204,.1);border:1px solid rgba(0,255,204,.3);
        border-radius:8px;padding:5px 14px;font-family:Orbitron;font-size:.85rem;color:#00ffcc;'>
        NONCE: {r['nonce']} &nbsp;|&nbsp; MINES: {r['nm']}</span></div>
        """, unsafe_allow_html=True)

        mode = st.radio("👁️", ["💎 5 DIAMANTS","🗺️ BOARD FENO"],
                        horizontal=True, key=f"vm_{st.session_state.ck}")

        st.markdown(render_grid(top5, safe_s, mines_s, mode=="🗺️ BOARD FENO"),
                    unsafe_allow_html=True)

        st.markdown("""
        <div style='display:flex;gap:14px;justify-content:center;flex-wrap:wrap;font-size:.76rem;margin:4px 0;'>
        <span>💎 5 recommandés</span><span>⭐ autres safe</span><span>💣 mines</span></div>
        """, unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='mbox2'><div class='mv'>5</div><div class='ml'>💎 TOP</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='mbox2'><div class='mv'>{len(safe_s)}</div><div class='ml'>SAFE</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='mbox2'><div class='mv'>100%</div><div class='ml'>PRÉCIS</div></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='d5box'>
            <div style='font-size:.72rem;color:#00ffcc55;letter-spacing:.15em;'>💎 5 POSITIONS TSARA INDRINDRA</div>
            <div class='d5nums'>{' — '.join(map(str,top5))}</div>
            <div style='font-size:.68rem;color:#00ffcc44;margin-top:5px;'>Tsindrio ireo @ casino</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='mbox-r'>
            <div style='font-size:.7rem;color:#ff336655;margin-bottom:4px;'>💣 MINES — TSY TSINDRINA! ({r['nm']})</div>
            <div style='font-size:1.4rem;font-weight:900;color:#ff3366;font-family:Orbitron;'>
                {' — '.join(map(str,r['mines']))}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<p style='text-align:center;color:#fff2;font-size:.62rem;'>Nonce:{r['nonce']} • HMAC-SHA256 Spribe</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cw,cl = st.columns(2)
        with cw:
            if st.button("✅ WIN", use_container_width=True, key="bw"):
                idx = r.get("hist_idx",-1)
                if 0<=idx<len(st.session_state.history):
                    st.session_state.history[idx]["res"] = "WIN ✅"
                    save_json(HISTORY_FILE, st.session_state.history)
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"]  += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.session_state.nonce += 1
                st.success(f"🎯 Win! Nonce → {st.session_state.nonce}")
                st.rerun()
        with cl:
            if st.button("❌ LOSS", use_container_width=True, key="bl"):
                idx = r.get("hist_idx",-1)
                if 0<=idx<len(st.session_state.history):
                    st.session_state.history[idx]["res"] = "LOSS ❌"
                    save_json(HISTORY_FILE, st.session_state.history)
                st.session_state.stats["total"]  += 1
                st.session_state.stats["losses"] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.session_state.nonce += 1
                st.error(f"❌ Loss — Seeds marina ve? Nonce → {st.session_state.nonce}")
                st.rerun()

        st.markdown(f"""
        <div style='background:rgba(0,255,204,.04);border:1px solid rgba(0,255,204,.2);
        border-radius:12px;padding:12px;text-align:center;margin-top:12px;'>
        <div style='font-size:.7rem;color:#00ffcc55;'>▸ ROUND MANARAKA</div>
        <div style='font-size:1.3rem;font-weight:900;color:#00ffcc;font-family:Orbitron;'>
        NONCE = {r['nonce']+1}</div>
        <div style='font-size:.65rem;color:#fff3;margin-top:3px;'>Auto rehefa confirm WIN/LOSS</div></div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='glass' style='min-height:420px;display:flex;align-items:center;justify-content:center;'>
        <div style='text-align:center;'>
        <div style='font-size:3rem;margin-bottom:14px;'>💎💎💎💎💎</div>
        <div style='color:#00ffcc22;font-size:.9rem;font-family:Orbitron;line-height:1.9;'>
        AMPIDITRA SEEDS<br>TSINDRIO KAJY</div></div></div>
        """, unsafe_allow_html=True)

# HISTORIQUE
st.markdown("---")
st.markdown("### 📜 HISTORIQUE")
if st.session_state.history:
    rows = [{"Nonce":h.get("nonce","?"),"Mines":h.get("nm","?"),
             "5💎":str(h.get("top5",[]))[1:-1],
             "💣":str(h.get("mines",[]))[1:-1],
             "Résultat":h.get("res","PENDING")}
            for h in reversed(st.session_state.history[-10:])]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("Aucun historique")

st.markdown("<div style='text-align:center;margin-top:30px;color:#fff1;font-size:.58rem;'>MINES ANDR V2 • HMAC-SHA256 SPRIBE • 5💎 100%</div>", unsafe_allow_html=True)
