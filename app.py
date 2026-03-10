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
st.caption("Turn-Based • 5 Actions • Weather on Map • Hidden Enemy Health • Scout Weak Points")

# Session state
if 'campaign_active' not in st.session_state:
    st.session_state.campaign_active = False
if 'era' not in st.session_state:
    st.session_state.era = None
if 'side' not in st.session_state:
    st.session_state.side = None
if 'battle_index' not in st.session_state:
    st.session_state.battle_index = 0
if 'manpower' not in st.session_state:      # Player Health
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
if 'enemy_health' not in st.session_state:   # Hidden until critical scout
    st.session_state.enemy_health = 100
if 'weak_points_discovered' not in st.session_state:
    st.session_state.weak_points_discovered = False
if 'log' not in st.session_state:
    st.session_state.log = []

campaigns = {
    "World War I": {"sides": ["Allies", "Central Powers"], "battles": [{"name": "Marne", "base_cas": 263000}, {"name": "Verdun", "base_cas": 714000}, {"name": "Somme", "base_cas": 623000}]},
    "World War II": {"sides": ["Allies", "Axis"], "battles": [{"name": "Stalingrad", "base_cas": 1800000}, {"name": "D-Day", "base_cas": 225000}]},
    "Cold War": {"sides": ["Western Bloc", "Communist Bloc"], "battles": [{"name": "Inchon 1950", "base_cas": 178000}]}
}

weathers = ["Clear", "Rain", "Mud", "Snow", "Fog"]

def generate_map(front_line, manpower, weather, enemy_health_visible):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#0a0e17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.axis('off')

    # Base terrain
    ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#4a7043', alpha=0.7))

    # Weather visuals
    if weather == "Rain":
        for _ in range(80):
            x = random.uniform(0,1)
            ax.plot([x, x+0.02], [random.uniform(0,0.5), random.uniform(0.3,0.5)], color='#88ccff', alpha=0.6, linewidth=1)
    elif weather == "Snow":
        for _ in range(60):
            ax.scatter(random.uniform(0,1), random.uniform(0,0.5), color='white', s=8, alpha=0.8)
    elif weather == "Mud":
        ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#3d2b1f', alpha=0.6))
    elif weather == "Fog":
        ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='white', alpha=0.25))

    # Front line
    x = np.linspace(0, 1, 100)
    y = 0.25 + 0.05 * np.sin(x * 12)
    ax.plot(x, y, color='white', linewidth=5)

    # Your soldiers (blue)
    num_your = max(4, int(manpower/8))
    for i in range(num_your):
        ax.scatter(front_line - 0.15 + (i%5)*0.06, 0.18 + random.uniform(-0.05,0.05), color='#1e90ff', marker='^', s=220, edgecolor='white')

    # Enemy soldiers (red)
    num_enemy = max(4, int((200 - manpower)/8))
    for i in range(num_enemy):
        ax.scatter(front_line + 0.15 - (i%5)*0.06, 0.32 + random.uniform(-0.05,0.05), color='#ff3333', marker='v', s=220, edgecolor='white')

    # Enemy health bar (only if revealed)
    if enemy_health_visible:
        ax.add_patch(plt.Rectangle((0.75, 0.42), st.session_state.enemy_health/100*0.2, 0.04, color='#ff3333'))

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
        st.session_state.enemy_health = 100
        st.session_state.weak_points_discovered = False
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

    map_buf = generate_map(st.session_state.front_line, st.session_state.manpower, st.session_state.weather, st.session_state.enemy_health < 100)
    st.image(map_buf, caption="Live Battlefield with Soldiers", use_column_width=True)

    st.write(f"**You command:** {st.session_state.side}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Your Health", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    if st.session_state.enemy_health < 100:
        st.metric("Enemy Health (Revealed!)", f"{int(st.session_state.enemy_health)}%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Choose Your Action This Turn")

    colA, colB = st.columns(2)

    with colA:
        if st.button("🔍 Scout Ahead"):
            if random.random() < 0.001:  # 1/1000 critical success
                st.session_state.enemy_health = random.randint(40, 90)
                st.success("CRITICAL SCOUT! Enemy health revealed!")
            elif random.random() < 0.65:
                st.session_state.weak_points_discovered = True
                st.success("Weak points discovered! Next attack deals 50% more damage!")
            else:
                st.info("Scouts found nothing useful.")

        if st.button("⚔️ Direct Assault"):
            dmg = 18 if st.session_state.weak_points_discovered else 12
            st.session_state.enemy_health -= dmg
            st.session_state.manpower -= 10
            st.session_state.weak_points_discovered = False
            st.info("Direct assault launched!")

        if st.button("🔄 Flanking Maneuver"):
            dmg = 15 if st.session_state.weak_points_discovered else 10
            st.session_state.enemy_health -= dmg
            st.session_state.front_line += 0.12
            st.session_state.weak_points_discovered = False
            st.info("Flanking maneuver executed!")

    with colB:
        if st.button("💥 Artillery Bombardment"):
            dmg = 14 if st.session_state.weak_points_discovered else 9
            st.session_state.enemy_health -= dmg
            st.session_state.supplies -= 12
            st.session_state.weak_points_discovered = False
            st.info("Artillery barrage fired!")

        if st.button("🛡️ Defensive Entrenchment"):
            st.session_state.morale += 18
            st.session_state.manpower -= 6
            st.info("Troops entrenched – morale rising.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Newspaper
    if len(st.session_state.log) > 0:
        headline = random.choice([
            f"HEROIC {st.session_state.side.upper()} ADVANCE!",
            f"ENEMY LINES SHATTERED!",
            f"HEAVY FIGHTING AT {battle['name']}",
            f"OUR TROOPS STAND FIRM!"
        ])
        st.markdown(f'<div class="newspaper"><div class="headline">{headline}</div><p>Latest dispatch from the front.</p></div>', unsafe_allow_html=True)

    if st.session_state.enemy_health <= 0 or st.session_state.manpower <= 0:
        st.balloons()
        st.success("CAMPAIGN COMPLETE" if st.session_state.enemy_health <= 0 else "DEFEAT")
        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Weather on Map • 5 Turn Actions • Hidden Enemy Health")
