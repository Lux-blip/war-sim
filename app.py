import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# Dark military theme – mature look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
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
st.caption("Historical Campaign Simulator • Real Stats • WW1 • WW2 • Cold War")

# Initialize session state
if 'campaign_active' not in st.session_state:
    st.session_state.campaign_active = False
if 'era' not in st.session_state:
    st.session_state.era = None
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

# Full campaigns – 6–7 battles each
campaigns = {
    "World War I – The Great War": [
        {"name": "First Battle of the Marne (1914)", "desc": "Stop the German advance on Paris", "base_cas": 250000},
        {"name": "Battle of Verdun (1916)", "desc": "The meat grinder", "base_cas": 700000},
        {"name": "Battle of the Somme (1916)", "desc": "Bloodiest day in British history", "base_cas": 420000},
        {"name": "Passchendaele (1917)", "desc": "Mud and attrition", "base_cas": 400000},
        {"name": "German Spring Offensive (1918)", "desc": "Germany's last push", "base_cas": 850000},
        {"name": "Hundred Days Offensive (1918)", "desc": "Final Allied victory", "base_cas": 180000}
    ],
    "World War II – Global Conflict": [
        {"name": "Battle of Britain (1940)", "desc": "Air war for survival", "base_cas": 45000},
        {"name": "Battle of Stalingrad (1942–43)", "desc": "Eastern Front turning point", "base_cas": 1900000},
        {"name": "Battle of Midway (1942)", "desc": "Pacific carrier battle", "base_cas": 5000},
        {"name": "D-Day Normandy (1944)", "desc": "Largest amphibious invasion", "base_cas": 10300},
        {"name": "Battle of the Bulge (1944–45)", "desc": "Hitler’s last gamble", "base_cas": 190000},
        {"name": "Battle of Berlin (1945)", "desc": "Fall of the Third Reich", "base_cas": 350000}
    ],
    "Cold War – Proxy Wars": [
        {"name": "Korean War – Inchon (1950)", "desc": "MacArthur’s gamble", "base_cas": 3500},
        {"name": "Vietnam – Tet Offensive (1968)", "desc": "Surprise attack", "base_cas": 45000},
        {"name": "Soviet Afghanistan (1979–89)", "desc": "Soviet quagmire", "base_cas": 15000},
        {"name": "Falklands War (1982)", "desc": "British task force", "base_cas": 900},
        {"name": "Gulf War – Desert Storm (1991)", "desc": "High-tech blitz", "base_cas": 300},
        {"name": "Cuban Missile Crisis Alt (1962)", "desc": "Nuclear escalation", "base_cas": 500000}
    ]
}

# Sidebar
with st.sidebar:
    st.header("Campaign Control")
    selected_campaign = st.selectbox("Select War", list(campaigns.keys()))

    if st.button("START / RESTART CAMPAIGN", type="primary"):
        st.session_state.campaign_active = True
        st.session_state.era = selected_campaign
        st.session_state.battle_index = 0
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.rerun()

    if st.session_state.campaign_active:
        if st.button("RESET & START NEW"):
            st.session_state.campaign_active = False
            st.rerun()

# Main game
if not st.session_state.campaign_active:
    st.info("Select a campaign above and click START to begin.")
else:
    battles = campaigns[st.session_state.era]
    current = battles[st.session_state.battle_index]

    st.header(f"{st.session_state.era}")
    st.progress(st.session_state.battle_index / len(battles), text=f"Battle {st.session_state.battle_index + 1}/{len(battles)}")

    st.subheader(current["name"])
    st.write(current["desc"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Manpower", f"{st.session_state.manpower}%")
    col2.metric("Supplies", f"{st.session_state.supplies}%")
    col3.metric("Morale", f"{st.session_state.morale}%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Your Orders")

    inf = st.slider("Infantry Focus %", 20, 80, 50)
    sup = st.slider("Support (Artillery/Air/Naval) %", 10, 60, 35)
    agg = st.slider("Aggression Level (1–10)", 1, 10, 5)
    tacs = st.multiselect("Tactics", ["Bombardment", "Flank", "Air Strike", "Night Attack", "Defend", "Counter"], default=["Bombardment"])

    if st.button("EXECUTE BATTLE", type="primary"):
        success = min(0.95, max(0.08, 0.48 + (inf/50*0.3) + (sup/35*0.35) + (agg/5*0.25) + len(tacs)*0.07 + random.uniform(-0.15, 0.15)))
        casualties = int(current["base_cas"] * (1.4 - success))

        mp_loss = int(25 - success * 18)
        sup_loss = int(22 - success * 15)
        mor_chg = int(18 * (success - 0.5))

        st.session_state.manpower = max(10, st.session_state.manpower - mp_loss)
        st.session_state.supplies = max(10, st.session_state.supplies - sup_loss)
        st.session_state.morale = max(10, min(100, st.session_state.morale + mor_chg))
        st.session_state.history_score += int((success - 0.5) * 18)

        st.success(f"Battle Result • Success: **{success:.0%}** • Losses: **{casualties:,}**")

        events = [
            "Heavy rain slows advance.",
            "Enemy supply line cut.",
            "Heroic stand boosts morale.",
            "Intelligence leak hurts.",
            "Air support devastates.",
            "Friendly fire incident.",
            "Breakthrough achieved."
        ]
        st.info(random.choice(events))

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("NEXT BATTLE →"):
        if st.session_state.battle_index < len(battles) - 1:
            st.session_state.battle_index += 1
            st.rerun()
        else:
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

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Built with Streamlit")
