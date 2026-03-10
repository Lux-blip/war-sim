import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import io

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; margin: 1rem 0; }
    .stButton > button { background: #b91c1c !important; color: white !important; font-size: 1.1rem !important; padding: 14px 20px !important; border-radius: 10px !important; width: 100%; margin: 6px 0; }
    .stButton > button:hover { background: #ef4444 !important; }
    .newspaper { background: #f5e8c7; color: #1a1a1a; padding: 1.5rem; border: 4px solid #333; font-family: serif; margin: 1rem 0; }
    .headline { font-size: 1.45rem; font-weight: 700; color: #b91c1c; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Fully Turn-Based • 8 Diverse Actions • Dynamic Soldier Maps • Weather & Newspapers")

# Session state
if 'campaign_active' not in st.session_state:
    st.session_state.campaign_active = False
if 'era' not in st.session_state:
    st.session_state.era = None
if 'side' not in st.session_state:
    st.session_state.side = None
if 'battle_index' not in st.session_state:
    st.session_state.battle_index = 0
if 'manpower' not in st.session_state:
    st.session_state.manpower = 100
if 'supplies' not in st.session_state:
    st.session_state.supplies = 100
if 'morale' not in st.session_state:
    st.session_state.morale = 100
if 'history_score' not in st.session_state:
    st.session_state.history_score = 50
if 'front_line' not in st.session_state:
    st.session_state.front_line = 0.5
if 'weather' not in st.session_state:
    st.session_state.weather = "Clear"
if 'log' not in st.session_state:
    st.session_state.log = []

campaigns = {
    "World War I": {"sides": ["Allies", "Central Powers"], "battles": [{"name": "Marne", "base_cas": 263000}, {"name": "Verdun", "base_cas": 714000}, {"name": "Somme", "base_cas": 623000}]},
    "World War II": {"sides": ["Allies", "Axis"], "battles": [{"name": "Stalingrad", "base_cas": 1800000}, {"name": "D-Day", "base_cas": 225000}]},
    "Cold War": {"sides": ["Western Bloc", "Communist Bloc"], "battles": [{"name": "Inchon 1950", "base_cas": 178000}]}
}

weathers = ["Clear", "Rain", "Mud", "Snow", "Fog"]

def generate_map(front_line, manpower):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#0a0e17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#4a7043', alpha=0.7))
    x = np.linspace(0, 1, 100)
    y = 0.25 + 0.05 * np.sin(x * 12)
    ax.plot(x, y, color='white', linewidth=5)
    ax.fill_between(x, y, 0, color='#1e40af' if st.session_state.side == "Allies" else '#991b1b', alpha=0.6)

    # Your soldiers (blue)
    for i in range(max(4, int(manpower/8))):
        ax.scatter(front_line - 0.15 + (i%5)*0.06, 0.18 + random.uniform(-0.05,0.05), color='#1e90ff', marker='^', s=220, edgecolor='white')
    # Enemy soldiers (red)
    for i in range(max(4, int((200-manpower)/8))):
        ax.scatter(front_line + 0.15 - (i%5)*0.06, 0.32 + random.uniform(-0.05,0.05), color='#ff3333', marker='v', s=220, edgecolor='white')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#0a0e17')
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
        st.session_state.side = None
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.session_state.front_line = 0.5
        st.session_state.weather = random.choice(weathers)
        st.session_state.log = []
        st.rerun()

    if st.session_state.campaign_active and st.button("RESET"):
        st.session_state.campaign_active = False
        st.rerun()

if not st.session_state.campaign_active:
    st.info("Select era and click START CAMPAIGN")
else:
    battles = campaigns[st.session_state.era]["battles"]
    battle = battles[st.session_state.battle_index]

    if st.session_state.side is None:
        st.subheader(f"Choose Your Side – {st.session_state.era}")
        side = st.radio("Command which side?", campaigns[st.session_state.era]["sides"])
        if st.button("CONFIRM SIDE", type="primary"):
            st.session_state.side = side
            st.rerun()
        st.stop()

    st.header(f"{battle['name']} – Turn {st.session_state.battle_index + 1}")
    st.caption(f"Weather: **{st.session_state.weather}**")
    map_buf = generate_map(st.session_state.front_line, st.session_state.manpower)
    st.image(map_buf, caption="Live Battlefield with Soldiers", use_column_width=True)

    st.write(f"**You command:** {st.session_state.side}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Choose Your Action This Turn")

    colA, colB = st.columns(2)

    with colA:
        if st.button("🔍 Scout Ahead"):
            success = random.uniform(0.7, 0.95)
            st.session_state.history_score += 8
            st.session_state.morale += 5
            st.session_state.front_line += 0.05
            st.info("Scouts report enemy weak spots!")
        if st.button("⚔️ Direct Assault"):
            success = random.uniform(0.4, 0.85)
            st.session_state.manpower -= 12
            st.session_state.front_line += 0.12
            st.info("Brave charge – heavy fighting!")
        if st.button("🔄 Flanking Maneuver"):
            success = random.uniform(0.6, 0.9)
            st.session_state.front_line += 0.15
            st.info("Flank successful!")
        if st.button("💥 Artillery Bombardment"):
            success = random.uniform(0.65, 0.85)
            st.session_state.supplies -= 10
            st.info("Artillery rains down!")

    with colB:
        if st.button("🛡️ Defensive Entrenchment"):
            st.session_state.morale += 15
            st.session_state.manpower -= 5
            st.info("Troops dig in – morale rises.")
        if st.button("🏃 Rapid Advance"):
            success = random.uniform(0.5, 0.8)
            st.session_state.front_line += 0.18
            st.session_state.supplies -= 8
            st.info("We push forward!")
        if st.button("✈️ Air Support Strike"):
            success = random.uniform(0.75, 0.95)
            st.session_state.supplies -= 15
            st.info("Air support devastates enemy!")
        if st.button("📢 Propaganda Campaign"):
            st.session_state.morale += 20
            st.session_state.history_score += 10
            st.info("Morale boosted across the front!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Newspaper
    if st.session_state.phase > 0:  # dummy phase for headline trigger
        headline = random.choice([
            f"HEROIC {st.session_state.side.upper()} ADVANCE!",
            f"ENEMY LINES SHATTERED!",
            f"HEAVY FIGHTING AT {battle['name']}",
            f"OUR TROOPS STAND FIRM!"
        ])
        st.markdown(f'<div class="newspaper"><div class="headline">{headline}</div><p>Our brave forces under {st.session_state.side} command continue the fight for freedom.</p></div>', unsafe_allow_html=True)

    if st.session_state.get("show_end", False):
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • 8 Turn Actions • Live Soldier Maps")
