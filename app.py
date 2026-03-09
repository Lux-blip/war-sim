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
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; margin: 1rem 0; }
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
st.caption("Historical Campaign Simulator • Dynamic Battle Maps • Choose Your Side")

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

# Campaigns with phase-specific maps
campaigns = {
    "World War I": {
        "sides": ["Allies (Entente)", "Central Powers"],
        "battles": [
            {"name": "First Battle of the Marne (1914)", "base_cas": 263000,
             "phases": [
                 {"desc": "German Schlieffen advance toward Paris", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "Allied counterattack begins – taxis of Paris rush to front", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "German retreat – Race to the Sea begins", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"}
             ]},
            {"name": "Battle of Verdun (1916)", "base_cas": 714000,
             "phases": [
                 {"desc": "German opening bombardment & assault", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French 'They shall not pass' defense", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French counter-offensive reclaims ground", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"}
             ]},
            {"name": "Battle of the Somme (1916)", "base_cas": 623000,
             "phases": [
                 {"desc": "British zero-hour assault – 1 July", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Map_of_the_Battle_of_the_Somme%2C_1916.svg/800px-Map_of_the_Battle_of_the_Somme%2C_1916.svg.png"},
                 {"desc": "Attrition & tank debut (Sept)", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Map_of_the_Battle_of_the_Somme%2C_1916.svg/800px-Map_of_the_Battle_of_the_Somme%2C_1916.svg.png"},
                 {"desc": "Battle ends – limited gains", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Map_of_the_Battle_of_the_Somme%2C_1916.svg/800px-Map_of_the_Battle_of_the_Somme%2C_1916.svg.png"}
             ]}
        ]
    },
    "World War II": {
        "sides": ["Allies", "Axis"],
        "battles": [
            {"name": "Stalingrad (1942–43)", "base_cas": 1800000,
             "phases": [
                 {"desc": "German 6th Army advances into city", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "Soviet house-to-house defense & Operation Uranus", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "6th Army encircled & destroyed", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"}
             ]},
            {"name": "D-Day Normandy (1944)", "base_cas": 225000,
             "phases": [
                 {"desc": "Omaha & Utah beaches – initial assault", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Breakout from hedgerows – Operation Cobra", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Allied advance toward Falaise Pocket", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"}
             ]}
        ]
    },
    "Cold War": {
        "sides": ["Western Bloc / UN", "Communist Bloc"],
        "battles": [
            {"name": "Korean War – Inchon & Escalation (1950)", "base_cas": 178000,
             "phases": [
                 {"desc": "MacArthur’s amphibious landing at Inchon", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "UN forces recapture Seoul & push north", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "Chinese People’s Volunteer Army enters – massive counteroffensive", 
                  "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"}
             ]}
        ]
    }
}

# Sidebar
with st.sidebar:
    st.header("Campaign Control")
    era = st.selectbox("Select War Era", list(campaigns.keys()))

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
        st.rerun()

    if st.session_state.campaign_active:
        if st.button("RESET CAMPAIGN"):
            st.session_state.campaign_active = False
            st.session_state.side = None
            st.rerun()

# Main game
if not st.session_state.campaign_active:
    st.info("Select era → START CAMPAIGN → choose your side")
else:
    era_data = campaigns[st.session_state.era]
    battles = era_data["battles"]
    battle = battles[st.session_state.battle_index]

    # Choose side once
    if st.session_state.side is None:
        st.subheader(f"Choose Your Side – {st.session_state.era}")
        side = st.radio("Which side will you command?", era_data["sides"])
        if st.button("CONFIRM SIDE & BEGIN", type="primary"):
            st.session_state.side = side
            st.rerun()
        st.stop()

    # Current phase & map
    phase_maps = battle.get("phases", [{"desc": "Battlefield Overview", "map": "https://via.placeholder.com/800x450?text=Battle+Map"}])
    phase = min(st.session_state.phase, len(phase_maps)-1)
    current_phase = phase_maps[phase]

    st.header(f"{battle['name']} – Phase {phase + 1}/3")
    st.caption(current_phase["desc"])
    st.image(current_phase["map"], caption=f"Front Line Situation – Phase {phase + 1}", use_column_width=True, clamp=True)

    st.write(f"**Commanding:** {st.session_state.side}")

    # Resources
    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    # Orders
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {phase + 1} Orders")

    inf = st.slider("Infantry / Ground Forces %", 20, 80, 50)
    sup = st.slider("Support (Arty/Air/Naval) %", 10, 60, 35)
    agg = st.slider("Aggression Level", 1, 10, 5)

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
        st.markdown(f'<div class="event-box">**Phase Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

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
            st.write("**Legendary Victory** – You rewrote history.")
        elif score > 60:
            st.write("**Hard-Fought Win** – Victory at great cost.")
        elif score > 40:
            st.write("**Stalemate** – War drags on.")
        else:
            st.write("**Defeat** – The enemy prevails.")

        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.session_state.side = None
            st.session_state.show_end = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Dynamic Battle Maps")
