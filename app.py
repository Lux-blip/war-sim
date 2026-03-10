import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import io

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# Theme
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
    hr { border-color: #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Dynamic In-Game Maps • Turn-Based • Choose Your Side • Real Historical Battles")

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
if 'front_line' not in st.session_state:
    st.session_state.front_line = 0.5  # 0.0 = enemy controls all, 1.0 = you control all

# Campaigns (simplified for map drawing)
campaigns = {
    "World War I": {
        "sides": ["Allies (Entente)", "Central Powers"],
        "battles": [
            {"name": "First Marne 1914", "base_cas": 263000},
            {"name": "Verdun 1916", "base_cas": 714000},
            {"name": "Somme 1916", "base_cas": 623000}
        ]
    },
    "World War II": {
        "sides": ["Allies", "Axis"],
        "battles": [
            {"name": "Stalingrad 1942–43", "base_cas": 1800000},
            {"name": "D-Day 1944", "base_cas": 225000}
        ]
    },
    "Cold War": {
        "sides": ["Western Bloc / UN", "Communist Bloc"],
        "battles": [
            {"name": "Korean Inchon 1950", "base_cas": 178000}
        ]
    }
}

# Simple in-game map generator
def generate_battle_map(front_line=0.5, phase=0, terrain="Open"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#0a0e17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.axis('off')

    # Background terrain
    if terrain == "Open":
        ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#4a7043', alpha=0.7))
    elif terrain == "Urban":
        ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#5c5c5c', alpha=0.7))
    elif terrain == "Mud":
        ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#3d2b1f', alpha=0.8))

    # Front line
    x = np.linspace(0, 1, 100)
    y = 0.25 + 0.05 * np.sin(x * 20 + phase * 2)  # wavy line
    ax.plot(x, y, color='white', linewidth=4, alpha=0.8)
    ax.fill_between(x, y, 0, color='#991b1b' if st.session_state.side == "Axis" else '#1e40af', alpha=0.6)
    ax.fill_between(x, y, 0.5, color='#1e40af' if st.session_state.side == "Axis" else '#991b1b', alpha=0.6)

    # Markers
    ax.plot(front_line, 0.25, marker='o', markersize=20, color='yellow', markeredgecolor='black')
    ax.text(front_line, 0.3, "Front Line", color='white', ha='center', fontsize=12)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    buf.seek(0)
    plt.close(fig)
    return buf

# Sidebar
with st.sidebar:
    st.header("Campaign Control")
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
        st.session_state.front_line = 0.5
        st.rerun()

    if st.session_state.campaign_active:
        if st.button("RESET CAMPAIGN"):
            st.session_state.campaign_active = False
            st.session_state.side = None
            st.rerun()

# Main game
if not st.session_state.campaign_active:
    st.info("Select era → START CAMPAIGN → choose side")
else:
    era_data = campaigns[st.session_state.era]
    battles = era_data["battles"]
    battle = battles[st.session_state.battle_index]

    # Choose side
    if st.session_state.side is None:
        st.subheader(f"Choose Your Side – {st.session_state.era}")
        side = st.radio("Which side?", era_data["sides"])
        if st.button("CONFIRM SIDE & BEGIN", type="primary"):
            st.session_state.side = side
            st.rerun()
        st.stop()

    # Current phase map (generated in-game)
    st.header(f"{battle['name']} – Phase {st.session_state.phase + 1}/3")
    map_buf = generate_battle_map(st.session_state.front_line, st.session_state.phase)
    st.image(map_buf, caption=f"Front Line – Phase {st.session_state.phase + 1}", use_column_width=True)

    st.write(f"**Commanding:** {st.session_state.side}")

    # Resources
    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    # Orders
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {st.session_state.phase + 1} Orders")

    inf = st.slider("Infantry / Ground %", 20, 80, 50)
    sup = st.slider("Support %", 10, 60, 35)
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

        # Update front line
        st.session_state.front_line += (success - 0.5) * 0.15
        st.session_state.front_line = max(0.1, min(0.9, st.session_state.front_line))

        events = ["Rain slows advance.", "Enemy ambush.", "Heroic charge!", "Air strike success.", "Supply shortage.", "Breakthrough!"]
        st.markdown(f'<div class="event-box">**Phase Report:** {random.choice(events)}</div>', unsafe_allow_html=True)

        st.session_state.phase += 1
        if st.session_state.phase >= 3:
            st.session_state.phase = 0
            if st.session_state.battle_index < len(battles) - 1:
                st.session_state.battle_index += 1
                st.session_state.front_line = 0.5  # Reset for new battle
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
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • In-Game Generated Maps")
