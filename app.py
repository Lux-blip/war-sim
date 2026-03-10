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
    .newspaper { background: #f5e8c7; color: #1a1a1a; padding: 1.5rem; border: 4px solid #333; font-family: serif; margin: 1rem 0; }
    .headline { font-size: 1.5rem; font-weight: 700; color: #b91c1c; text-align: center; margin-bottom: 0.5rem; }
    .stButton > button[kind="primary"] {
        background: #b91c1c !important; color: white !important;
        font-size: 1.2rem !important; padding: 14px 40px !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Dynamic Maps with Soldiers • Weather • Newspaper Headlines • Choose Your Side")

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
    st.session_state.front_line = 0.5
if 'weather' not in st.session_state:
    st.session_state.weather = "Clear"

# Campaigns
campaigns = {
    "World War I": {"sides": ["Allies", "Central Powers"], "battles": [{"name": "Marne", "base_cas": 263000}, {"name": "Verdun", "base_cas": 714000}, {"name": "Somme", "base_cas": 623000}]},
    "World War II": {"sides": ["Allies", "Axis"], "battles": [{"name": "Stalingrad", "base_cas": 1800000}, {"name": "D-Day", "base_cas": 225000}]},
    "Cold War": {"sides": ["Western Bloc", "Communist Bloc"], "battles": [{"name": "Inchon 1950", "base_cas": 178000}]}
}

weathers = ["Clear", "Rain", "Mud", "Snow", "Fog"]

def generate_map(front_line, phase, manpower, weather):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#0a0e17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.axis('off')

    # Terrain
    ax.add_patch(plt.Rectangle((0,0), 1, 0.5, color='#4a7043', alpha=0.7))

    # Front line
    x = np.linspace(0, 1, 100)
    y = 0.25 + 0.05 * np.sin(x * 15 + phase * 3)
    ax.plot(x, y, color='white', linewidth=5)

    # Your soldiers (blue)
    num_your = max(4, int(manpower / 8))
    for i in range(num_your):
        ax.scatter(front_line - 0.12 + (i%6)*0.04, 0.18 + random.uniform(-0.04,0.04), color='#1e90ff', marker='^', s=220, edgecolor='white')

    # Enemy soldiers (red)
    num_enemy = max(4, int((200 - manpower) / 8))
    for i in range(num_enemy):
        ax.scatter(front_line + 0.12 - (i%6)*0.04, 0.32 + random.uniform(-0.04,0.04), color='#ff3333', marker='v', s=220, edgecolor='white')

    ax.text(0.05, 0.45, f"YOUR FORCES ({st.session_state.side})", color='#1e90ff', fontsize=11, weight='bold')
    ax.text(0.75, 0.45, "ENEMY FORCES", color='#ff3333', fontsize=11, weight='bold')

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
        st.session_state.phase = 0
        st.session_state.side = None
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.session_state.front_line = 0.5
        st.session_state.weather = random.choice(weathers)
        st.rerun()

    if st.session_state.campaign_active and st.button("RESET"):
        st.session_state.campaign_active = False
        st.rerun()

# Game
if not st.session_state.campaign_active:
    st.info("Select era → START → choose side")
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

    # Current map
    st.header(f"{battle['name']} – Phase {st.session_state.phase + 1}/3")
    st.caption(f"Weather: **{st.session_state.weather}**")
    map_buf = generate_map(st.session_state.front_line, st.session_state.phase, st.session_state.manpower, st.session_state.weather)
    st.image(map_buf, caption="Live Battlefield with Soldiers", use_column_width=True)

    st.write(f"**Commanding:** {st.session_state.side}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Phase {st.session_state.phase + 1} Orders")

    inf = st.slider("Infantry %", 20, 80, 50)
    sup = st.slider("Support %", 10, 60, 35)
    agg = st.slider("Aggression", 1, 10, 5)

    if st.button("COMMIT PHASE", type="primary"):
        # Weather effect
        weather_mod = {"Clear": 0, "Rain": -0.08, "Mud": -0.15, "Snow": -0.12, "Fog": -0.10}[st.session_state.weather]
        success = min(0.95, max(0.08, 0.48 + (inf/50*0.3) + (sup/35*0.35) + (agg/5*0.25) + random.uniform(-0.15, 0.15) + weather_mod))

        mp_loss = int(12 - success * 9)
        sup_loss = int(10 - success * 8)
        mor_chg = int((success - 0.5) * 14)

        st.session_state.manpower = max(8, st.session_state.manpower - mp_loss)
        st.session_state.supplies = max(8, st.session_state.supplies - sup_loss)
        st.session_state.morale = max(10, min(100, st.session_state.morale + mor_chg))
        st.session_state.history_score += int((success - 0.5) * 8)

        st.session_state.front_line += (success - 0.5) * 0.18
        st.session_state.front_line = max(0.1, min(0.9, st.session_state.front_line))

        # Newspaper headline
        if success > 0.75:
            headline = f"GLORIOUS ADVANCE! {st.session_state.side.upper()} SMASHES ENEMY LINES"
        elif success > 0.5:
            headline = f"HEROIC STAND – {st.session_state.side.upper()} HOLDS THE LINE"
        else:
            headline = f"HEAVY LOSSES – {st.session_state.side.upper()} FORCED TO RETREAT"

        st.markdown(f'<div class="newspaper"><div class="headline">{headline}</div>'
                    f'<p>Phase {st.session_state.phase+1} of {battle["name"]}. Casualties heavy but spirit unbroken. '
                    f'Our brave troops under {st.session_state.side} command continue the fight for freedom.</p></div>', 
                    unsafe_allow_html=True)

        st.session_state.phase += 1
        if st.session_state.phase >= 3:
            st.session_state.phase = 0
            if st.session_state.battle_index < len(battles) - 1:
                st.session_state.battle_index += 1
                st.session_state.weather = random.choice(weathers)
                st.session_state.front_line = 0.5
            else:
                st.session_state.show_end = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_end", False):
        st.balloons()
        st.success("CAMPAIGN COMPLETE")
        score = st.session_state.history_score
        if score > 85: st.write("**Legendary Victory** – You changed history!")
        elif score > 60: st.write("**Victory** – Hard fought and won.")
        elif score > 40: st.write("**Stalemate**")
        else: st.write("**Defeat**")

        if st.button("RETURN TO MENU"):
            st.session_state.campaign_active = False
            st.rerun()

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Weather + Newspapers + Live Soldier Maps")
