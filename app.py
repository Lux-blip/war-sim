import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# ── Mature military theme (dark & immersive) ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .metric-box { background: #111827; padding: 16px; border-radius: 10px; text-align: center; }
    .event-box { background: #1f2937; padding: 1rem 1.4rem; border-left: 5px solid #ca8a04; border-radius: 8px; margin: 1rem 0; }
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); }
    .stButton > button[kind="primary"] {
        background: #b91c1c !important; color: white !important;
        font-size: 1.2rem !important; padding: 14px 40px !important;
        border-radius: 12px !important;
    }
    hr { border-color: #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Full Historical Campaign Simulator • Choose Your Nation • Battle Maps • Turn-Based (3 Phases per Battle)")

# ── Session state with safe defaults ──
if 'war_active' not in st.session_state:
    st.session_state.war_active = False
if 'war_era' not in st.session_state:
    st.session_state.war_era = None
if 'war_side' not in st.session_state:
    st.session_state.war_side = None
if 'war_battle_idx' not in st.session_state:
    st.session_state.war_battle_idx = 0
if 'war_turn_phase' not in st.session_state:
    st.session_state.war_turn_phase = 0
if 'war_manpower' not in st.session_state:
    st.session_state.war_manpower = 100
if 'war_supplies' not in st.session_state:
    st.session_state.war_supplies = 100
if 'war_morale' not in st.session_state:
    st.session_state.war_morale = 100
if 'war_score' not in st.session_state:
    st.session_state.war_score = 50
if 'war_log' not in st.session_state:
    st.session_state.war_log = []
if 'war_achievements' not in st.session_state:
    st.session_state.war_achievements = set()
if 'war_difficulty' not in st.session_state:
    st.session_state.war_difficulty = "Normal"

# ── Full campaigns with real battle maps & nation choices ──
campaign_data = {
    "World War I – Western Front": {
        "sides": ["Allies (Britain/France)", "Central Powers (Germany)"],
        "battles": [
            {"name": "First Battle of the Marne (1914)", "desc": "Stop the German advance", "base_cas": 263000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
            {"name": "Battle of Verdun (1916)", "desc": "The meat grinder", "base_cas": 714000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
            {"name": "Battle of the Somme (1916)", "desc": "Bloodiest day in British history", "base_cas": 623000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Map_of_the_Battle_of_the_Somme%2C_1916.svg/800px-Map_of_the_Battle_of_the_Somme%2C_1916.svg.png"},
            {"name": "Passchendaele (1917)", "desc": "Mud and attrition", "base_cas": 457000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Passchendaele_map.jpg/800px-Passchendaele_map.jpg"},
            {"name": "German Spring Offensive (1918)", "desc": "Germany’s last push", "base_cas": 988000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Spring_Offensive_Map.jpg/800px-Spring_Offensive_Map.jpg"},
            {"name": "Hundred Days Offensive (1918)", "desc": "Final Allied victory", "base_cas": 265000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Hundred_Days_Offensive_map.svg/800px-Hundred_Days_Offensive_map.svg.png"}
        ]
    },
    "World War II – European Theater": {
        "sides": ["Allies (USA/UK)", "Axis (Germany)"],
        "battles": [
            {"name": "Battle of Britain (1940)", "desc": "RAF vs Luftwaffe", "base_cas": 43000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Battle_of_Britain_map.svg/800px-Battle_of_Britain_map.svg.png"},
            {"name": "Battle of Stalingrad (1942–43)", "desc": "Turning point of the East", "base_cas": 1800000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
            {"name": "Kursk (1943)", "desc": "Largest tank battle ever", "base_cas": 860000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Battle_of_Kursk_map.svg/800px-Battle_of_Kursk_map.svg.png"},
            {"name": "D-Day Normandy (1944)", "desc": "Invasion of Europe", "base_cas": 225000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
            {"name": "Battle of the Bulge (1944)", "desc": "Hitler’s last gamble", "base_cas": 195000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Battle_of_the_Bulge_map.svg/800px-Battle_of_the_Bulge_map.svg.png"},
            {"name": "Battle of Berlin (1945)", "desc": "Fall of the Third Reich", "base_cas": 410000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Battle_of_Berlin_map.svg/800px-Battle_of_Berlin_map.svg.png"}
        ]
    },
    "Cold War Hotspots": {
        "sides": ["UN / USA-led Coalition", "Communist Forces"],
        "battles": [
            {"name": "Korean War – Inchon (1950)", "desc": "MacArthur’s gamble", "base_cas": 178000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
            {"name": "Vietnam – Tet Offensive (1968)", "desc": "Psychological turning point", "base_cas": 145000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Tet_Offensive_map.svg/800px-Tet_Offensive_map.svg.png"},
            {"name": "Yom Kippur War (1973)", "desc": "Arab surprise attack", "base_cas": 21000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Yom_Kippur_War_map.svg/800px-Yom_Kippur_War_map.svg.png"},
            {"name": "Soviet Afghanistan (1985–86)", "desc": "Soviet quagmire", "base_cas": 28000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Afghan_War_map_1979.svg/800px-Afghan_War_map_1979.svg.png"},
            {"name": "Falklands War (1982)", "desc": "British expedition", "base_cas": 1400,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Falklands_map.svg/800px-Falklands_map.svg.png"},
            {"name": "Gulf War Ground Phase (1991)", "desc": "100-hour liberation", "base_cas": 35000,
             "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Desert_Storm_map.svg/800px-Desert_Storm_map.svg.png"}
        ]
    }
}

difficulties = {"Easy": 0.75, "Normal": 1.0, "Hard": 1.35, "Brutal": 1.80}

# ── Sidebar controls ──
with st.sidebar:
    st.header("Campaign Setup")
    era_choice = st.selectbox("Select War Era", list(campaign_data.keys()))
    
    if st.button("START CAMPAIGN", type="primary"):
        st.session_state.war_active = True
        st.session_state.war_era = era_choice
        st.session_state.war_battle_idx = 0
        st.session_state.war_turn_phase = 0
        st.session_state.war_manpower = 100
        st.session_state.war_supplies = 100
        st.session_state.war_morale = 100
        st.session_state.war_score = 50
        st.session_state.war_log = []
        st.session_state.war_achievements = set()
        st.session_state.war_difficulty = "Normal"
        st.rerun()

    if st.session_state.war_active:
        if st.button("RESET & NEW CAMPAIGN"):
            for k in ['active','era','battle_idx','turn_phase','manpower','supplies','morale','score','log','achievements']:
                st.session_state[f'war_{k}'] = False if k == 'active' else 0 if 'idx' in k or 'phase' in k else 100 if k in ['manpower','supplies','morale'] else 50 if k == 'score' else []
            st.rerun()

# ── Main game ──
if not st.session_state.war_active:
    st.info("Choose era above → click START CAMPAIGN → then pick your nation")
else:
    era_data = campaign_data[st.session_state.war_era]
    battles = era_data["battles"]
    battle = battles[st.session_state.war_battle_idx]

    # Side / Nation selection (only once at start of campaign)
    if st.session_state.war_side is None:
        st.subheader("Choose Your Side / Nation")
        side_choice = st.radio("Which side will you command?", era_data["sides"], key="sidepick")
        if st.button("CONFIRM NATION & BEGIN", type="primary"):
            st.session_state.war_side = side_choice
            st.rerun()
        st.stop()

    # Battle header with MAP
    st.header(f"{st.session_state.war_era} – {battle['name']}")
    st.progress(st.session_state.war_battle_idx / len(battles))
    st.image(battle["map"], caption="Battlefield Map", use_column_width=True, clamp=True)

    st.caption(battle["desc"])
    st.write(f"**You are commanding: {st.session_state.war_side}**")

    # Resources
    cols = st.columns(4)
    cols[0].metric("Manpower", f"{st.session_state.war_manpower}%")
    cols[1].metric("Supplies", f"{st.session_state.war_supplies}%")
    cols[2].metric("Morale", f"{st.session_state.war_morale}%")
    cols[3].metric("History Score", f"{st.session_state.war_score}/100")

    # TURN-BASED SYSTEM – 3 phases per battle
    phase_names = ["1. Planning Phase", "2. Maneuver Phase", "3. Assault Phase"]
    current_phase = st.session_state.war_turn_phase

    st.markdown(f"**{phase_names[current_phase]}**")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        inf = st.slider("Infantry & Ground Commitment (%)", 20, 85, 50, 5)
        sup = st.slider("Support (Artillery/Air/Naval) (%)", 10, 65, 35, 5)
        agg = st.slider("Aggression Level", 1, 10, 5, 1)
        tacs = st.multiselect("Tactics for this phase", 
                              ["Heavy Bombardment", "Armored Flank", "Air Supremacy", "Night Infiltration", "Defensive Reserves", "Rapid Pursuit"],
                              default=["Heavy Bombardment"], max_selections=3)

        if st.button("COMMIT THIS PHASE", type="primary"):
            dmod = difficulties[st.session_state.war_difficulty]
            base = 0.48
            infm = (inf - 50)/100 * 0.32
            supm = (sup - 35)/
