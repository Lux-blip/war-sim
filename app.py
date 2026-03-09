import streamlit as st
import random
from datetime import date
import time

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# ── Theme ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0b0f1a !important; color: #d1d5db !important; }
    h1, h2, h3 { color: #f3f4f6 !important; font-weight: 700 !important; }
    .card { background: #17212f; border: 1px solid #334155; border-radius: 14px; padding: 1.6rem; margin: 1.2rem 0; box-shadow: 0 6px 16px rgba(0,0,0,0.35); }
    .metric-box { background: #111827; padding: 1.1rem; border-radius: 10px; text-align: center; border: 1px solid #374151; }
    .event-box { background: #1f2937; padding: 1rem 1.4rem; border-left: 5px solid #ca8a04; border-radius: 8px; margin: 1rem 0; }
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; }
    .headline { font-size: 1.4rem; font-weight: 600; color: #ef4444; margin: 1rem 0; text-align: center; }
    .stButton > button[kind="primary"] {
        background: #991b1b !important; color: white !important;
        font-size: 1.15rem !important; padding: 0.9rem 2.2rem !important;
        border-radius: 10px !important; transition: all 0.25s ease;
    }
    .stButton > button[kind="primary"]:hover {
        background: #b91c1c !important; transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(153,27,27,0.45);
    }
    hr { border-color: #374151 !important; margin: 2.2rem 0; }
    .title-glow { text-shadow: 0 0 12px #991b1b; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-glow'>ECHOES OF WAR</h1>", unsafe_allow_html=True)
st.caption("Grand Strategy War Simulator • Choose Side • Dynamic Maps • Turn-Based • Alternate History")

# ── Session State ──
defaults = {
    'active': False,
    'era': None,
    'side': None,
    'battle_idx': 0,
    'phase': 0,
    'manpower': 100,
    'supplies': 100,
    'morale': 100,
    'score': 50,
    'log': [],
    'achievements': set(),
    'difficulty': "Normal",
    'weather': "Clear",
    'terrain': "Open",
    'last_battle_state': None
}

for k, v in defaults.items():
    if f'war_{k}' not in st.session_state:
        st.session_state[f'war_{k}'] = v

# ── Campaigns ──
campaigns = {
    "World War I": {
        "sides": ["Allies (Entente)", "Central Powers"],
        "battles": [
            {"name": "First Marne 1914", "base_cas": 263000,
             "phases": [
                 {"desc": "German advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "Allied counter", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "German retreat", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"}
             ]},
            {"name": "Verdun 1916", "base_cas": 714000,
             "phases": [
                 {"desc": "German assault", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French defense", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French recovery", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"}
             ]}
        ]
    },
    "World War II": {
        "sides": ["Allies", "Axis"],
        "battles": [
            {"name": "Stalingrad 1942–43", "base_cas": 1800000,
             "phases": [
                 {"desc": "German advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "Soviet defense", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "Encirclement", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"}
             ]},
            {"name": "D-Day 1944", "base_cas": 225000,
             "phases": [
                 {"desc": "Beach landings", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Breakout", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Inland advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"}
             ]}
        ]
    },
    "Cold War": {
        "sides": ["Western Bloc", "Communist Bloc"],
        "battles": [
            {"name": "Korean Inchon 1950", "base_cas": 178000,
             "phases": [
                 {"desc": "Landing", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "UN advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "Chinese entry", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"}
             ]}
        ]
    }
}

difficulties = {"Easy": 0.75, "Normal": 1.0, "Hard": 1.35, "Brutal": 1.80}

weathers = ["Clear", "Rain", "Mud", "Snow", "Fog"]
terrains = ["Open", "Urban", "Mountain", "Forest", "Beachhead"]

# ── Sidebar ──
with st.sidebar:
    st.header("Campaign Control")
    era = st.selectbox("War Era", list(campaigns.keys()))
    diff = st.selectbox("Difficulty", list(difficulties.keys()), index=1)

    if st.button("START CAMPAIGN", type="primary"):
        st.session_state.war_active = True
        st.session_state.war_era = era
        st.session_state.war_battle_idx = 0
        st.session_state.war_phase = 0
        st.session_state.war_side = None
        st.session_state.war_manpower = 100
        st.session_state.war_supplies = 100
        st.session_state.war_morale = 100
        st.session_state.war_score = 50
        st.session_state.war_log = []
        st.session_state.war_achievements = set()
        st.session_state.war_difficulty = diff
        st.session_state.war_weather = random.choice(weathers)
        st.session_state.war_terrain = random.choice(terrains)
        st.rerun()

    if st.session_state.war_active:
        if st.button("RESET CAMPAIGN"):
            st.session_state.war_active = False
            st.rerun()

# ── Game ──
if not st.session_state.war_active:
    st.info("Choose era & difficulty → START CAMPAIGN → pick side")
else:
    data = campaigns[st.session_state.war_era]
    battles = data["battles"]
    battle = battles[st.session_state.war_battle_idx]

    if st.session_state.war_side is None:
        st.subheader(f"Choose Your Side – {st.session_state.war_era}")
        side = st.radio("Command which side?", data["sides"])
        if st.button("CONFIRM & BEGIN", type="primary"):
            st.session_state.war_side = side
            st.rerun()
        st.stop()

    # Phase map update
    phase_maps = battle.get("phases", [{"desc": "Battlefield", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"}])
    phase = min(st.session_state.war_phase, len(phase_maps)-1)
    current_map = phase_maps[phase]["map"]
    phase_desc = phase_maps[phase]["desc"]

    st.header(f"{battle['name']} – Phase {phase+1}/3")
    st.caption(f"{phase_desc} • Weather: {st.session_state.war_weather} • Terrain: {st.session_state.war_terrain}")
    st.image(current_map, caption="Current Frontline", use_column_width=True, clamp=True)

    st.write(f"**Commanding:** {st.session_state.war_side}")

    cols = st.columns(4)
    cols[0].metric("Manpower", f"{st.session_state.war_manpower}%")
    cols[1].metric("Supplies", f"{st.session_state.war_supplies}%")
    cols[2].metric("Morale", f"{st.session_state.war_morale}%")
    cols[3].metric("History Score", f"{st.session_state.war_score}/100")

    # Orders
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {phase+1} Orders")

    inf = st.slider("Infantry %", 20, 80, 50)
    sup = st.slider("Support %", 10, 60, 35)
    agg = st.slider("Aggression", 1, 10, 5)
    tacs = st.multiselect("Tactics", ["Bombard", "Flank", "Air", "Night", "Defend", "Counter"], default=["Bombard"], max_selections=3)

    if st.button("COMMIT PHASE", type="primary"):
        dmod = difficulties[st.session_state.war_difficulty]
        base = 0.48
        infm = (inf - 50)/100 * 0.32
        supm = (sup - 35)/100 * 0.38
        aggm = (agg - 5)/5 * 0.28
        tacb = len(tacs) * 0.07 + (0.15 if "Flank" in tacs else 0) + (0.12 if "Air" in tacs else 0)

        weather_mod = {"Clear": 0, "Rain": -0.08, "Mud": -0.15, "Snow": -0.12, "Fog": -0.10}[st.session_state.war_weather]
        terrain_mod = {"Open": 0.05, "Urban": -0.08, "Mountain": -0.12, "Forest": -0.06, "Beachhead": -0.10}[st.session_state.war_terrain]

        success = min(0.96, max(0.06, base + infm + supm + aggm + tacb + weather_mod + terrain_mod + random.uniform(-0.18, 0.18) * dmod))

        mp_l = int(12 - success * 9)
        sup_l = int(10 - success * 8)
        mor_d = int((success - 0.5) * 14)

        st.session_state.war_manpower = max(8, st.session_state.war_manpower - mp_l)
        st.session_state.war_supplies = max(8, st.session_state.war_supplies - sup_l)
        st.session_state.war_morale = max(10, min(100, st.session_state.war_morale + mor_d))
        st.session_state.war_score += int((success - 0.5) * 8)

        events = ["Rain slows advance.", "Enemy ambush.", "Heroic charge!", "Air strike success.", "Supply shortage.", "Breakthrough!", "Morale collapse!", "Intelligence coup."]
        st.markdown(f'<div class="event-box">**Phase Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

        st.session_state.war_phase += 1
        if st.session_state.war_phase >= 3:
            st.session_state.war_phase = 0
            if st.session_state.war_battle_idx < len(battles) - 1:
                st.session_state.war_battle_idx += 1
                # Update map & weather for next battle
                st.session_state.war_weather = random.choice(["Clear", "Rain", "Mud", "Snow", "Fog"])
                st.session_state.war_terrain = random.choice(["Open", "Urban", "Mountain", "Forest", "Beachhead"])
            else:
                st.session_state.show_end = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # End screen
    if st.session_state.get("show_end", False):
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        score = st.session_state.war_score
        endings = {
            range(85,101): "Total Triumph – history significantly altered.",
            range(65,85): "Victory – objectives met at high cost.",
            range(45,65): "Pyrrhic success – war prolonged.",
            range(30,45): "Stalemate – neither side wins decisively.",
            range(0,30): "Defeat – enemy gains upper hand."
        }
        for r, text in endings.items():
            if score in r:
                st.markdown(f"**Final Score: {score}/100**  \n{text}")
                break

        if st.session_state.war_achievements:
            st.markdown("**Achievements:**")
            for a in st.session_state.war_achievements:
                st.markdown(f"- {a}")

        st.markdown("**Campaign Log**")
        for entry in st.session_state.war_log:
            st.markdown(f"- {entry}")

        if st.button("RETURN TO MENU"):
            for k in ['active','era','side','battle_idx','phase','manpower','supplies','morale','score','log','achievements']:
                st.session_state[f'war_{k}'] = False if k == 'active' else 0 if 'idx' in k or 'phase' in k else 100 if k in ['manpower','supplies','morale'] else 50 if k == 'score' else set() if k == 'achievements' else []
            st.session_state.show_end = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Turn-Based • Dynamic Maps • Side Choice")
