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
    .map-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); width: 100%; margin: 1rem 0; }
    .stButton > button { background: #b91c1c !important; color: white !important; font-size: 1.1rem !important; padding: 14px 20px !important; border-radius: 10px !important; width: 100%; margin: 6px 0; }
    .stButton > button:hover { background: #ef4444 !important; }
    .newspaper { background: #f5e8c7; color: #1a1a1a; padding: 1.5rem; border: 4px solid #333; font-family: serif; margin: 1rem 0; }
    .headline { font-size: 1.45rem; font-weight: 700; color: #b91c1c; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Turn-Based • 5 Diverse Actions • Live Soldier Maps • Weather on Map • Newspapers")

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
if 'player_health' not in st.session_state:
    st.session_state.player_health = 100
if 'enemy_health' not in st.session_state:
    st.session_state.enemy_health = 100
if 'enemy_health_revealed' not in st.session_state:
    st.session_state.enemy_health_revealed = False
if 'weakpoints_active' not in st.session_state:
    st.session_state.weakpoints_active = False
if 'log' not in st.session_state:
    st.session_state.log = []

campaigns = {
    "World War I": {"sides": ["Allies", "Central Powers"], "battles": [{"name": "Marne", "base_cas": 263000}, {"name": "Verdun", "base_cas": 714000}, {"name": "Somme", "base_cas": 623000}]},
    "World War II": {"sides": ["Allies", "Axis"], "battles": [{"name": "Stalingrad", "base_cas": 1800000}, {"name": "D-Day", "base_cas": 225000}]},
    "Cold War": {"sides": ["Western Bloc", "Communist Bloc"], "battles": [{"name": "Inchon 1950", "base_cas": 178000}]}
}

weathers = ["Clear", "Rain", "Mud", "Snow", "Fog"]

def generate_map(front_line, manpower, weather):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#0a0e17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.axis('off')

    # Weather background
    weather_colors = {"Clear": "#4a7043", "Rain": "#2b5d7a", "Mud": "#3d2b1f", "Snow": "#d0d4d8", "Fog": "#6b7a8a"}
    ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color=weather_colors[weather], alpha=0.85))

    # Front line
    x = np.linspace(0, 1, 100)
    y = 0.25 + 0.05 * np.sin(x * 12)
    ax.plot(x, y, color='white', linewidth=5)

    # Your soldiers (blue)
    num_your = max(4, int(manpower / 8))
    for i in range(num_your):
        ax.scatter(front_line - 0.15 + (i % 5) * 0.06, 0.18 + random.uniform(-0.05, 0.05), color='#1e90ff', marker='^', s=220, edgecolor='white')

    # Enemy soldiers (red)
    num_enemy = max(4, int((200 - manpower) / 8))
    for i in range(num_enemy):
        ax.scatter(front_line + 0.15 - (i % 5) * 0.06, 0.32 + random.uniform(-0.05, 0.05), color='#ff3333', marker='v', s=220, edgecolor='white')

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
        st.session_state.player_health = 100
        st.session_state.enemy_health = 100
        st.session_state.enemy_health_revealed = False
        st.session_state.weakpoints_active = False
        st.session_state.log = []
        st.rerun()

    if st.session_state.campaign_active and st.button("RESET"):
        st.session_state.campaign_active = False
        st.rerun()

# Main game
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
    map_buf = generate_map(st.session_state.front_line, st.session_state.manpower, st.session_state.weather)
    st.image(map_buf, caption="Live Battlefield with Soldiers", use_column_width=True)

    st.write(f"**You command:** {st.session_state.side}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Your Health", f"{st.session_state.player_health}%")
    if st.session_state.enemy_health_revealed:
        col2.metric("Enemy Health", f"{st.session_state.enemy_health}%")
    else:
        col2.metric("Enemy Health", "???")
    col3.metric("Manpower", f"{st.session_state.manpower}%")
    col4.metric("Morale", f"{st.session_state.morale}%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Choose Your Action This Turn")

    colA, colB = st.columns(2)

    with colA:
        if st.button("🔍 Scout Ahead"):
            roll = random.random()
            if roll < 0.001:  # 1/1000 critical scout
                st.session_state.enemy_health_revealed = True
                st.success("CRITICAL SCOUT SUCCESS! Enemy health revealed!")
            elif roll < 0.4:
                st.session_state.weakpoints_active = True
                st.success("Weak points found! Next attack deals +50% damage!")
            else:
                st.info("Scouts report minor intel.")
            st.session_state.history_score += 8
            st.session_state.log.append("Scouted ahead")

        if st.button("⚔️ Direct Assault"):
            damage = 18
            if st.session_state.weakpoints_active:
                damage = int(damage * 1.5)
                st.session_state.weakpoints_active = False
            st.session_state.enemy_health = max(0, st.session_state.enemy_health - damage)
            st.session_state.manpower -= 12
            st.info("Direct assault launched!")
            st.session_state.log.append("Direct assault")

        if st.button("🔄 Flanking Maneuver"):
            st.session_state.front_line += 0.15
            st.info("Flanking successful!")
            st.session_state.log.append("Flanking maneuver")

    with colB:
        if st.button("💥 Artillery Bombardment"):
            damage = 14
            if st.session_state.weakpoints_active:
                damage = int(damage * 1.5)
                st.session_state.weakpoints_active = False
            st.session_state.enemy_health = max(0, st.session_state.enemy_health - damage)
            st.session_state.supplies -= 10
            st.info("Artillery strike!")
            st.session_state.log.append("Artillery bombardment")

        if st.button("✈️ Air Support Strike"):
            damage = 22
            if st.session_state.weakpoints_active:
                damage = int(damage * 1.5)
                st.session_state.weakpoints_active = False
            st.session_state.enemy_health = max(0, st.session_state.enemy_health - damage)
            st.session_state.supplies -= 15
            st.info("Air support called in!")
            st.session_state.log.append("Air support strike")

    st.markdown('</div>', unsafe_allow_html=True)

    # End battle if health reaches zero
    if st.session_state.player_health <= 0 or st.session_state.enemy_health <= 0:
        st.balloons()
        st.success("BATTLE COMPLETE")
        if st.session_state.enemy_health <= 0:
            st.write("**VICTORY!** Enemy defeated.")
        else:
            st.write("**DEFEAT.** Your forces were overwhelmed.")
        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • 5 Actions per Turn • Live Maps")
