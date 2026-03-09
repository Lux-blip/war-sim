import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# ── Theme ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin: 1rem 0; }
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; }
    .stButton > button[kind="primary"] {
        background: #b91c1c !important; color: white !important;
        font-size: 1.15rem !important; padding: 0.9rem 2.5rem !important;
        border-radius: 10px !important;
    }
    hr { border-color: #334155 !important; margin: 2rem 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Historical War Simulator • Choose Your Side • Maps Update Every Phase")

# ── Session state ──
keys = ['active', 'era', 'side', 'battle_idx', 'phase', 'manpower', 'supplies', 'morale', 'score']
for k in keys:
    if f'war_{k}' not in st.session_state:
        st.session_state[f'war_{k}'] = False if k == 'active' else 0 if 'idx' in k or 'phase' in k else 100 if k in ['manpower','supplies','morale'] else 50 if k == 'score' else None

# ── Campaigns with side-specific maps per phase ──
campaigns = {
    "World War I": {
        "sides": ["Allies (Entente)", "Central Powers"],
        "battles": [
            {"name": "Marne 1914", "base_cas": 263000,
             "phases": [
                 {"desc": "German advance", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "Allied counterattack begins", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"},
                 {"desc": "German retreat", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg"}
             ]},
            {"name": "Verdun 1916", "base_cas": 714000,
             "phases": [
                 {"desc": "German opening assault", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French defense line", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"},
                 {"desc": "French counter-offensive", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png"}
             ]}
            # Add more battles here if you want...
        ]
    },
    "World War II": {
        "sides": ["Allies", "Axis"],
        "battles": [
            {"name": "Stalingrad 1942–43", "base_cas": 1800000,
             "phases": [
                 {"desc": "German advance into city", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "Soviet house-to-house defense", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"},
                 {"desc": "Soviet encirclement", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png"}
             ]},
            {"name": "D-Day 1944", "base_cas": 225000,
             "phases": [
                 {"desc": "Initial beach landings", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Breakout from beaches", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"},
                 {"desc": "Allied advance inland", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png"}
             ]}
        ]
    },
    "Cold War": {
        "sides": ["Western Bloc / UN", "Communist Bloc"],
        "battles": [
            {"name": "Korean War – Inchon 1950", "base_cas": 178000,
             "phases": [
                 {"desc": "Amphibious landing", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "UN advance north", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"},
                 {"desc": "Chinese intervention", "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png"}
             ]}
        ]
    }
}

# ── Sidebar ──
with st.sidebar:
    st.header("Campaign Control")
    era = st.selectbox("War Era", list(campaigns.keys()))

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
        st.rerun()

    if st.session_state.war_active and st.button("RESET CAMPAIGN"):
        st.session_state.war_active = False
        st.rerun()

# ── Main game ──
if not st.session_state.war_active:
    st.info("Select era → click START CAMPAIGN → choose your side")
else:
    data = campaigns[st.session_state.war_era]
    battles = data["battles"]
    battle = battles[st.session_state.war_battle_idx]

    # Choose side only once
    if st.session_state.war_side is None:
        st.subheader(f"Choose Your Side – {st.session_state.war_era}")
        side = st.radio("Which side will you command?", data["sides"])
        if st.button("CONFIRM SIDE & BEGIN", type="primary"):
            st.session_state.war_side = side
            st.rerun()
        st.stop()

    # Current battle & phase
    phase = st.session_state.war_phase
    phase_maps = battle["phases"]
    current_map = phase_maps[phase]["map"]
    phase_desc = phase_maps[phase]["desc"]

    st.header(f"{battle['name']} – Phase {phase + 1}/3")
    st.caption(phase_desc)
    st.image(current_map, caption=f"Frontline Situation – Phase {phase + 1}", use_column_width=True, clamp=True)

    st.write(f"You are commanding: **{st.session_state.war_side}**")

    # Resources
    cols = st.columns(3)
    cols[0].metric("Manpower", f"{st.session_state.war_manpower}%")
    cols[1].metric("Supplies", f"{st.session_state.war_supplies}%")
    cols[2].metric("Morale", f"{st.session_state.war_morale}%")

    # Orders
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {phase + 1} Orders")

    inf = st.slider("Infantry / Ground Forces %", 20, 80, 50)
    sup = st.slider("Support (Arty/Air/Naval) %", 10, 60, 35)
    agg = st.slider("Aggression Level", 1, 10, 5)

    if st.button("COMMIT ORDERS – EXECUTE PHASE", type="primary"):
        success = min(0.95, max(0.08, 0.48 + (inf/50*0.3) + (sup/35*0.35) + (agg/5*0.25) + random.uniform(-0.15, 0.15)))

        mp_loss = int(12 - success * 9)
        sup_loss = int(10 - success * 8)
        mor_chg = int((success - 0.5) * 14)

        st.session_state.war_manpower = max(8, st.session_state.war_manpower - mp_loss)
        st.session_state.war_supplies = max(8, st.session_state.war_supplies - sup_loss)
        st.session_state.war_morale = max(10, min(100, st.session_state.war_morale + mor_chg))
        st.session_state.war_score += int((success - 0.5) * 8)

        events = ["Rain slows advance.", "Enemy ambush.", "Heroic charge!", "Air strike success.", "Supply shortage.", "Breakthrough!"]
        st.markdown(f'<div class="event-box">**Phase Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

        st.session_state.war_phase += 1
        if st.session_state.war_phase >= 3:
            st.session_state.war_phase = 0
            if st.session_state.war_battle_idx < len(battles) - 1:
                st.session_state.war_battle_idx += 1
            else:
                st.session_state.show_end = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Campaign end
    if st.session_state.get("show_end", False):
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        score = st.session_state.war_score
        if score > 85:
            st.write("**Legendary Victory** – history rewritten")
        elif score > 60:
            st.write("**Victory** – objectives achieved")
        elif score > 40:
            st.write("**Stalemate**")
        else:
            st.write("**Defeat**")

        if st.button("RETURN TO MENU"):
            for k in ['active','era','side','battle_idx','phase','manpower','supplies','morale','score']:
                st.session_state[f'war_{k}'] = False if k == 'active' else 0 if 'idx' in k or 'phase' in k else 100 if k in ['manpower','supplies','morale'] else 50 if k == 'score' else None
            st.session_state.show_end = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR")
