import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# Dark military theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .metric-box { background: #111827; padding: 16px; border-radius: 10px; text-align: center; }
    .event-box { background: #1f2937; padding: 1rem 1.4rem; border-left: 5px solid #ca8a04; border-radius: 8px; margin: 1rem 0; }
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; }
    .stButton > button[kind="primary"] {
        background: #b91c1c !important;
        color: white !important;
        font-size: 1.2rem !important;
        padding: 14px 40px !important;
        border-radius: 12px !important;
    }
    hr { border-color: #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Historical Campaign Simulator • Choose Your Side • Maps Update Every Phase")

# Session state
if 'campaign_active' not in st.session_state:
    st.session_state.campaign_active = False
if 'era' not in st.session_state:
    st.session_state.era = None
if 'side' not in st.session_state:
    st.session_state.side = None
if 'battle_index' not in st.session_state:
    st.session_state.battle_index = 0
if 'phase' not in st.session_state:
    st.session_state.phase = 0
if 'manpower' not in st.session_state:
    st.session_state.manpower = 100
if 'supplies' not in st.session_state:
    st.session_state.supplies = 100
if 'morale' not in st.session_state:
    st.session_state.morale = 100
if 'history_score' not in st.session_state:
    st.session_state.history_score = 50
if 'log' not in st.session_state:
    st.session_state.log = []

# Campaigns with side-specific maps per phase
campaigns = {
    "World War I": {
        "sides": ["Allies (Entente)", "Central Powers"],
        "battles": [
            {"name": "First Marne 1914", "base_cas": 263000,
             "phases": [
                 {"desc": "German advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "Allied counterattack", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "German retreat", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"}
             ]},
            {"name": "Verdun 1916", "base_cas": 714000,
             "phases": [
                 {"desc": "German opening assault", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French defense", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French counter-offensive", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"}
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
                 {"desc": "Soviet encirclement", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"}
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
        "sides": ["Western Bloc / UN", "Communist Bloc"],
        "battles": [
            {"name": "Korean War – Inchon 1950", "base_cas": 178000,
             "phases": [
                 {"desc": "Amphibious landing", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "UN advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "Chinese intervention", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"}
             ]}
        ]
    }
}

# Sidebar
with st.sidebar:
    st.header("Campaign Setup")
    era = st.selectbox("Select Era", list(campaigns.keys()))

    if st.button("START CAMPAIGN", type="primary"):
        st.session_state.campaign_active = True
        st.session_state.era = era
        st.session_state.battle_index = 0
        st.session_state.phase = 0
        st.session_state.side = None
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.session_state.log = []
        st.rerun()

    if st.session_state.campaign_active:
        if st.button("RESET CAMPAIGN"):
            st.session_state.campaign_active = False
            st.rerun()

# Main game
if not st.session_state.campaign_active:
    st.info("Select an era and click START CAMPAIGN")
else:
    era_data = campaigns[st.session_state.era]
    battles = era_data["battles"]
    battle = battles[st.session_state.battle_index]

    # Choose side (once)
    if st.session_state.side is None:
        st.subheader(f"Choose Your Side – {st.session_state.era}")
        side = st.radio("Command which side?", era_data["sides"])
        if st.button("CONFIRM SIDE & BEGIN", type="primary"):
            st.session_state.side = side
            st.rerun()
        st.stop()

    # Current phase map & description
    phase_maps = battle.get("phases", [{"desc": "Battlefield", "map": "https://via.placeholder.com/800x450?text=Battle+Map"}])
    phase = min(st.session_state.phase, len(phase_maps) - 1)
    current_phase = phase_maps[phase]

    st.header(f"{battle['name']} – Phase {phase + 1}/3")
    st.caption(current_phase["desc"])
    st.image(current_phase["map"], caption=f"Front Line – Phase {phase + 1}", use_column_width=True)

    st.write(f"**You command:** {st.session_state.side}")

    # Resources
    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    # Orders
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {phase + 1} Orders")

    inf = st.slider("Infantry / Ground %", 20, 80, 50)
    sup = st.slider("Support (Arty/Air/Naval) %", 10, 60, 35)
    agg = st.slider("Aggression", 1, 10, 5)

    if st.button("COMMIT PHASE", type="primary"):
        success = min(0.95, max(0.08, 0.48 + (inf/50*0.3) + (sup/35*0.35) + (agg/5*0.25) + random.uniform(-0.15, 0.15)))

        mp_loss = int(12 - success * 9)
        sup_loss = int(10 - success * 8)
        mor_chg = int((success - 0.5) * 14)

        st.session_state.manpower = max(8, st.session_state.manpower - mp_loss)
        st.session_state.supplies = max(8, st.session_state.supplies - sup_loss)
        st.session_state.morale = max(10, min(100, st.session_state.morale + mor_chg))
        st.session_state.history_score += int((success - 0.5) * 8)

        events = ["Rain slows advance.", "Enemy ambush.", "Heroic charge!", "Air strike success.", "Supply shortage.", "Breakthrough!"]
        st.markdown(f'<div class="event-box">**Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

        st.session_state.phase += 1
        if st.session_state.phase >= 3:
            st.session_state.phase = 0
            if st.session_state.battle_index < len(battles) - 1:
                st.session_state.battle_index += 1
            else:
                st.session_state.show_end = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # End screen
    if st.session_state.get("show_end", False):
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        score = st.session_state.history_score
        if score > 85:
            st.write("**Legendary Victory** – history rewritten")
        elif score > 60:
            st.write("**Victory** – objectives achieved")
        elif score > 40:
            st.write("**Stalemate**")
        else:
            st.write("**Defeat**")

        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.session_state.side = None
            st.session_state.show_end = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR")
