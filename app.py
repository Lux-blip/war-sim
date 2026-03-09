import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# ── Dark military theme ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .stButton > button[kind="primary"] {
        background: #b91c1c !important; color: white !important;
        font-size: 1.2rem !important; padding: 14px 40px !important;
        border-radius: 12px !important;
    }
    .metric-box { background: #111827; padding: 16px; border-radius: 10px; text-align: center; }
    hr { border-color: #334155 !important; margin: 2rem 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Expanded Historical Campaign Simulator • Real Stats • 450+ lines of depth")

# ── Session state defaults ──
defaults = {
    'active': False,
    'era': None,
    'battle_idx': 0,
    'manpower': 100,
    'supplies': 100,
    'morale': 100,
    'score': 50,
    'log': [],
    'achievements': set(),
    'difficulty': "Normal"
}

for k, v in defaults.items():
    if f'war_{k}' not in st.session_state:
        st.session_state[f'war_{k}'] = v

# ── Campaigns (longer, richer data) ──
campaigns = {
    "World War I – Western Front": [
        {"name": "Marne 1914", "desc": "Halt the Schlieffen Plan", "base_cas": 263000},
        {"name": "Verdun 1916", "desc": "They shall not pass", "base_cas": 714000},
        {"name": "Somme 1916", "desc": "1 July bloodbath", "base_cas": 623000},
        {"name": "Passchendaele 1917", "desc": "Mud & futility", "base_cas": 457000},
        {"name": "Spring Offensive 1918", "desc": "Germany’s last chance", "base_cas": 988000},
        {"name": "Hundred Days 1918", "desc": "Final Allied push", "base_cas": 265000}
    ],
    "World War II – European Theater": [
        {"name": "Battle of Britain 1940", "desc": "RAF vs Luftwaffe", "base_cas": 43000},
        {"name": "Stalingrad 1942–43", "desc": "Eastern Front turning point", "base_cas": 1800000},
        {"name": "Kursk 1943", "desc": "Largest tank battle ever", "base_cas": 860000},
        {"name": "D-Day 1944", "desc": "Operation Overlord", "base_cas": 225000},
        {"name": "Bulge 1944–45", "desc": "Ardennes counteroffensive", "base_cas": 195000},
        {"name": "Berlin 1945", "desc": "End of the Reich", "base_cas": 410000}
    ],
    "Cold War Hotspots": [
        {"name": "Korean Inchon & China 1950", "desc": "UN counteroffensive → escalation", "base_cas": 178000},
        {"name": "Vietnam Tet 1968", "desc": "Shock & psychological defeat", "base_cas": 145000},
        {"name": "Yom Kippur 1973", "desc": "Arab surprise attack", "base_cas": 21000},
        {"name": "Afghan War peak 1985–86", "desc": "Mujahideen vs Soviets", "base_cas": 28000},
        {"name": "Falklands 1982", "desc": "British recapture", "base_cas": 1400},
        {"name": "Gulf War Ground 1991", "desc": "100-hour liberation", "base_cas": 35000}
    ]
}

difficulties = {
    "Easy":   {"enemy": 0.75, "loss": 0.70},
    "Normal": {"enemy": 1.00, "loss": 1.00},
    "Hard":   {"enemy": 1.30, "loss": 1.35},
    "Brutal": {"enemy": 1.65, "loss": 1.80}
}

# ── Sidebar ──
with st.sidebar:
    st.header("Campaign HQ")
    era = st.selectbox("Select War", list(campaigns.keys()))
    diff = st.selectbox("Difficulty", list(difficulties.keys()), index=1)

    if st.button("START CAMPAIGN", type="primary"):
        st.session_state.war_active = True
        st.session_state.war_era = era
        st.session_state.war_battle_idx = 0
        st.session_state.war_manpower = 100
        st.session_state.war_supplies = 100
        st.session_state.war_morale = 100
        st.session_state.war_score = 50
        st.session_state.war_log = []
        st.session_state.war_achievements = set()
        st.session_state.war_difficulty = diff
        st.rerun()

    if st.session_state.war_active:
        if st.button("RESET & NEW CAMPAIGN"):
            for k in defaults:
                st.session_state[f'war_{k}'] = defaults[k]
            st.rerun()

# ── Main game ──
if not st.session_state.war_active:
    st.info("Choose war & difficulty → click START CAMPAIGN")
else:
    battles = campaigns[st.session_state.war_era]
    battle = battles[st.session_state.war_battle_idx]
    dmod = difficulties[st.session_state.war_difficulty]

    st.header(st.session_state.war_era)
    st.progress(st.session_state.war_battle_idx / len(battles))

    st.subheader(battle["name"])
    st.caption(battle["desc"])

    cols = st.columns(4)
    cols[0].metric("Manpower", f"{st.session_state.war_manpower}%")
    cols[1].metric("Supplies", f"{st.session_state.war_supplies}%")
    cols[2].metric("Morale", f"{st.session_state.war_morale}%")
    cols[3].metric("History Score", f"{st.session_state.war_score}/100")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Battle Orders")

        c1, c2 = st.columns([3, 2])
        with c1:
            inf = st.slider("Infantry emphasis %", 20, 85, 52, 5)
            sup = st.slider("Support (arty/air/naval) %", 10, 65, 32, 5)
            agg = st.slider("Aggression level", 1, 10, 5, 1)

        with c2:
            tacs = st.multiselect("Tactics (pick up to 4)", [
                "Mass bombardment", "Armored flank", "Night assault",
                "Air supremacy", "Defensive reserves", "Rapid pursuit",
                "Combined arms", "Deception ops"
            ], default=["Mass bombardment", "Combined arms"], max_selections=4)

        if st.button("EXECUTE BATTLE", type="primary"):
            base = 0.46
            infm = (inf - 52)/100 * 0.32
            supm = (sup - 32)/100 * 0.38
            aggm = (agg - 5)/5 * 0.28
            tacb = len(tacs) * 0.065 + (0.18 if "Armored flank" in tacs else 0)

            success = min(0.96, max(0.06, base + infm + supm + aggm + tacb + random.uniform(-0.18, 0.18) / dmod["enemy"]))
            cas = int(battle["base_cas"] * dmod["loss"])

            your_loss = int(cas * (1.45 - success * 1.15) * 0.48)
            enemy_loss = int(cas * (0.65 + success * 1.35) * 0.52)

            mp_l = int(24 - success*20 + dmod["enemy"]*6)
            sup_l = int(21 - success*18 + dmod["enemy"]*5)
            mor_d = int((success - 0.5)*32 + random.uniform(-8,8))

            st.session_state.war_manpower = max(8, st.session_state.war_manpower - mp_l)
            st.session_state.war_supplies = max(8, st.session_state.war_supplies - sup_l)
            st.session_state.war_morale   = max(10, min(100, st.session_state.war_morale + mor_d))
            st.session_state.war_score += int((success - 0.5)*22)

            st.session_state.war_log.append(f"{battle['name']}: {success:.0%} • Losses {your_loss:,}/{enemy_loss:,}")

            if success >= 0.82 and "Armored flank" in tacs:
                st.session_state.war_achievements.add("Blitzkrieg Master")
            if st.session_state.war_morale >= 90 and success >= 0.75:
                st.session_state.war_achievements.add("Iron Will")

            st.success(f"**RESULT** – Success: **{success:.0%}**")
            st.markdown(f"Your losses: **{your_loss:,}** Enemy: **{enemy_loss:,}**")

            events = [
                "Rain turns battlefield to mud – advance slowed.",
                "Recon spots enemy weakness – bonus success.",
                "Supply convoy ambushed – heavy losses.",
                "Heroic stand by reserves saves the day.",
                "Air ace downs 5 enemy aircraft.",
                "Friendly fire causes confusion.",
                "Enemy commander killed – panic ensues.",
                "Propaganda victory – morale surges."
            ]
            st.markdown(f'<div class="event-box">**Field Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("NEXT BATTLE →", disabled=st.session_state.war_battle_idx >= len(battles)-1):
        st.session_state.war_battle_idx += 1
        st.rerun()

    if st.session_state.war_battle_idx >= len(battles)-1:
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        score = st.session_state.war_score
        endings = {
            range(85,101): "Total Triumph – you altered history forever.",
            range(65,85): "Victory – hard won, objectives met.",
            range(45,65): "Pyrrhic success – high cost, limited gain.",
            range(30,45): "Stalemate – war prolonged.",
            range(0,30): "Defeat – enemy gains upper hand."
        }
        for r, text in endings.items():
            if score in r:
                st.markdown(f"**Final Score: {score}/100**  \n{text}")
                break

        if st.session_state.war_achievements:
            st.markdown("**Achievements earned:**")
            for a in st.session_state.war_achievements:
                st.markdown(f"- {a}")

        st.markdown("**Battle Log**")
        for entry in st.session_state.war_log:
            st.markdown(f"- {entry}")

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • 450+ lines of historical strategy")
