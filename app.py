# ECHOES OF WAR – Expanded historical campaign simulator
# ~520 lines – more content, polish, feedback, events, endings, visuals

import streamlit as st
import random
from datetime import date
import time

st.set_page_config(
    page_title="ECHOES OF WAR – Historical Campaign Simulator",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────
#                STYLING – DARK MILITARY THEME
# ────────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: #0b0f1a;
        color: #d1d5db;
    }
    h1, h2, h3 {
        color: #f3f4f6 !important;
        font-weight: 700;
    }
    .stButton > button[kind="primary"] {
        background: #991b1b !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2.2rem !important;
        font-size: 1.15rem !important;
        border-radius: 10px !important;
        transition: all 0.25s ease;
    }
    .stButton > button[kind="primary"]:hover {
        background: #b91c1c !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(153,27,27,0.45);
    }
    .card {
        background: #17212f;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.6rem;
        margin: 1.2rem 0;
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    }
    .metric-box {
        background: #111827;
        padding: 1.1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #374151;
    }
    .event-box {
        background: #1f2937;
        padding: 1rem 1.4rem;
        border-left: 5px solid #ca8a04;
        border-radius: 8px;
        margin: 1rem 0;
    }
    hr {
        border-color: #374151;
        margin: 2.2rem 0;
    }
    .title-glow {
        text-shadow: 0 0 12px #991b1b;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#                   SESSION STATE
# ────────────────────────────────────────────────
defaults = {
    'campaign_active': False,
    'era': None,
    'battle_index': 0,
    'manpower': 100,
    'supplies': 100,
    'morale': 100,
    'history_score': 50,
    'turn_log': [],
    'achievements': set(),
    'difficulty': "Normal"
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ────────────────────────────────────────────────
#                   CAMPAIGNS & DATA
# ────────────────────────────────────────────────
campaigns = {
    "World War I – Western Front 1914–1918": [
        {"name": "First Marne (Sep 1914)", "desc": "Halt the Schlieffen Plan", "base_cas": 263000, "era_cas_mod": 1.0},
        {"name": "Verdun (Feb–Dec 1916)", "desc": "They shall not pass", "base_cas": 714000, "era_cas_mod": 1.15},
        {"name": "Somme (Jul–Nov 1916)", "desc": "1 July – worst day in British history", "base_cas": 623000, "era_cas_mod": 1.20},
        {"name": "Passchendaele (Jul–Nov 1917)", "desc": "Rain, mud, futility", "base_cas": 457000, "era_cas_mod": 1.10},
        {"name": "Spring Offensive (Mar–Jul 1918)", "desc": "Germany’s last gamble", "base_cas": 988000, "era_cas_mod": 1.05},
        {"name": "Hundred Days (Aug–Nov 1918)", "desc": "The black day of the German Army", "base_cas": 265000, "era_cas_mod": 0.90}
    ],
    "World War II – European Theater": [
        {"name": "Battle of Britain (Jul–Oct 1940)", "desc": "RAF vs Luftwaffe – fight for air supremacy", "base_cas": 43000, "era_cas_mod": 0.35},
        {"name": "Stalingrad (Aug 1942–Feb 1943)", "desc": "The turning point of the Eastern Front", "base_cas": 1800000, "era_cas_mod": 1.40},
        {"name": "Kursk (Jul–Aug 1943)", "desc": "Largest tank battle in history", "base_cas": 860000, "era_cas_mod": 1.25},
        {"name": "D-Day Normandy (Jun 1944)", "desc": "Operation Overlord begins", "base_cas": 225000, "era_cas_mod": 0.80},
        {"name": "Battle of the Bulge (Dec 1944–Jan 1945)", "desc": "Germany’s Ardennes counteroffensive", "base_cas": 195000, "era_cas_mod": 0.95},
        {"name": "Berlin (Apr–May 1945)", "desc": "Final assault on the Reich capital", "base_cas": 410000, "era_cas_mod": 1.05}
    ],
    "Cold War Hotspots 1950–1991": [
        {"name": "Inchon & Chinese Entry (1950)", "desc": "UN counteroffensive → massive escalation", "base_cas": 178000, "era_cas_mod": 0.65},
        {"name": "Vietnam – Tet Offensive (1968)", "desc": "Shock & psychological defeat", "base_cas": 145000, "era_cas_mod": 0.55},
        {"name": "Yom Kippur War (1973)", "desc": "Arab surprise attack on Israel", "base_cas": 21000, "era_cas_mod": 0.40},
        {"name": "Soviet–Afghan War peak (1985–86)", "desc": "Mujahideen vs Soviet 40th Army", "base_cas": 28000, "era_cas_mod": 0.45},
        {"name": "Falklands War (1982)", "desc": "British expeditionary recapture", "base_cas": 1400, "era_cas_mod": 0.25},
        {"name": "Gulf War – Ground Phase (1991)", "desc": "100-hour liberation of Kuwait", "base_cas": 35000, "era_cas_mod": 0.30}
    ]
}

difficulties = {
    "Easy":   {"enemy_bonus": 0.75, "loss_mult": 0.70, "random_low": -0.08},
    "Normal": {"enemy_bonus": 1.00, "loss_mult": 1.00, "random_low": -0.15},
    "Hard":   {"enemy_bonus": 1.30, "loss_mult": 1.35, "random_low": -0.22},
    "Brutal": {"enemy_bonus": 1.65, "loss_mult": 1.80, "random_low": -0.32}
}

# ────────────────────────────────────────────────
#                   SIDEBAR CONTROLS
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("Campaign Settings")
    selected_era = st.selectbox("War Theater", list(campaigns.keys()))
    diff_choice = st.selectbox("Difficulty", list(difficulties.keys()), index=1)
    st.markdown("---")

    if st.button("START / RESTART CAMPAIGN", type="primary", use_container_width=True):
        st.session_state.campaign_active = True
        st.session_state.era = selected_era
        st.session_state.battle_index = 0
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.session_state.turn_log = []
        st.session_state.achievements = set()
        st.session_state.difficulty = diff_choice
        st.rerun()

    if st.session_state.campaign_active:
        if st.button("RESET & START NEW", use_container_width=True):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()

        st.markdown("---")
        st.caption(f"Current difficulty: **{st.session_state.difficulty}**")
        st.caption(f"Battle {st.session_state.battle_index + 1} / {len(campaigns[st.session_state.era])}")

# ────────────────────────────────────────────────
#                   MAIN GAME FLOW
# ────────────────────────────────────────────────
if not st.session_state.campaign_active:
    st.markdown("<h1 class='title-glow'>ECHOES OF WAR</h1>", unsafe_allow_html=True)
    st.markdown("### Historical Campaign Simulator")
    st.markdown("""
    Choose a war, set difficulty, and lead your forces through a full campaign.  
    Every decision affects manpower, supplies, morale and the course of history.
    """)
    st.info("Click **START / RESTART CAMPAIGN** in the sidebar to begin.")
else:
    battles = campaigns[st.session_state.era]
    battle = battles[st.session_state.battle_index]
    diff = difficulties[st.session_state.difficulty]

    # Header
    st.markdown(f"<h1 class='title-glow'>{st.session_state.era}</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.battle_index / len(battles))
    st.subheader(battle["name"])
    st.caption(battle["desc"])

    # Resource dashboard
    cols = st.columns(4)
    cols[0].metric("Manpower", f"{st.session_state.manpower}%", delta_color="off")
    cols[1].metric("Supplies", f"{st.session_state.supplies}%", delta_color="off")
    cols[2].metric("Morale", f"{st.session_state.morale}%", delta_color="off")
    cols[3].metric("History Divergence", f"{st.session_state.history_score}/100", delta_color="off")

    # Command phase
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Issue Orders – Battle Phase")

        colA, colB = st.columns([3,2])

        with colA:
            infantry_focus = st.slider("Infantry & frontal commitment (%)", 20, 85, 52, 5, key="inf")
            support_focus = st.slider("Artillery / Air / Naval emphasis (%)", 10, 65, 32, 5, key="sup")
            aggression    = st.slider("Risk / Aggression level", 1, 10, 5, 1, key="agg")

        with colB:
            st.markdown("**Tactical doctrines** (multi-select)")
            tactics = st.multiselect(
                "Choose up to 4",
                options=[
                    "Massed artillery preparation",
                    "Armored flanking maneuver",
                    "Night / infiltration attack",
                    "Air superiority priority",
                    "Defensive depth & reserves",
                    "Rapid exploitation / pursuit",
                    "Combined arms coordination",
                    "Deception / feint operations"
                ],
                default=["Massed artillery preparation", "Combined arms coordination"],
                max_selections=4,
                key="tactics"
            )

        execute = st.button("EXECUTE OPERATION", type="primary", use_container_width=True, key="exec")

        if execute:
            # Core simulation
            base = 0.46
            inf_mod   = (infantry_focus - 52) / 100 * 0.32
            sup_mod   = (support_focus - 32) / 100 * 0.38
            agg_mod   = (aggression - 5) / 5 * 0.28
            tac_bonus = len(tactics) * 0.065 + (0.18 if "Armored flanking maneuver" in tactics else 0) + \
                        (0.14 if "Air superiority priority" in tactics else 0) + \
                        (0.11 if "Deception / feint operations" in tactics else 0)

            success_raw = base + inf_mod + sup_mod + agg_mod + tac_bonus + random.uniform(-0.18, 0.18)
            success = min(0.96, max(0.06, success_raw * diff["enemy_bonus"] ** -1))

            # Losses
            raw_cas = battle["base_cas"] * battle["era_cas_mod"] * diff["loss_mult"]
            your_loss_factor = 1.45 - success * 1.15
            enemy_loss_factor = 0.65 + success * 1.35
            your_cas = int(raw_cas * your_loss_factor * 0.48)
            enemy_cas = int(raw_cas * enemy_loss_factor * 0.52)

            # Resource impact
            mp_loss = int(24 - success * 20 + diff["enemy_bonus"] * 6)
            sup_loss = int(21 - success * 18 + diff["enemy_bonus"] * 5)
            mor_delta = int((success - 0.5) * 32 + random.uniform(-8,8))

            st.session_state.manpower = max(8,  st.session_state.manpower - mp_loss)
            st.session_state.supplies = max(8,  st.session_state.supplies - sup_loss)
            st.session_state.morale   = max(10, min(100, st.session_state.morale + mor_delta))
            st.session_state.history_score += int((success - 0.5) * 22)

            # Log
            turn_text = f"Battle {st.session_state.battle_index+1}: {success:.0%} success – Losses {your_cas:,} / Enemy {enemy_cas:,}"
            st.session_state.turn_log.append(turn_text)

            # Achievements / flavor
            if success >= 0.82 and "Armored flanking maneuver" in tactics:
                st.session_state.achievements.add("Blitzkrieg Master")
            if success >= 0.75 and st.session_state.morale >= 90:
                st.session_state.achievements.add("High Morale Victory")

            # Visual feedback
            st.success(f"**OPERATION COMPLETE** – Success probability realized: **{success:.0%}**")
            st.markdown(f"**Casualties** – Your side: **{your_cas:,}**     Enemy: **{enemy_cas:,}**")

            # Event
            event_pool = [
                "Heavy rain turned the battlefield into a quagmire.",
                "Your reconnaissance spotted an enemy weakness.",
                "Enemy counter-battery fire silenced your guns.",
                "A heroic stand by reserves prevented collapse.",
                "Logistical failure – ammunition shortage reported.",
                "Air support arrived just in time – devastating strike.",
                "Friendly fire incident caused heavy losses.",
                "Breakthrough! Enemy line shattered.",
                "Propaganda victory – morale surges.",
                "Enemy commander killed in action – confusion ensues."
            ]
            st.markdown(f'<div class="event-box">**Field Report:** {random.choice(event_pool)}</div>', unsafe_allow_html=True)

            st.rerun()

    # ── Navigation & End ─────────────────────────────────────────────
    col_nav1, col_nav2 = st.columns([3,1])

    with col_nav1:
        if st.button("ADVANCE TO NEXT PHASE →", disabled=st.session_state.battle_index >= len(battles)-1):
            st.session_state.battle_index += 1
            st.rerun()

    with col_nav2:
        if st.session_state.battle_index >= len(battles)-1:
            if st.button("VIEW CAMPAIGN SUMMARY", type="primary"):
                st.session_state.show_summary = True

    # Summary screen
    if st.session_state.battle_index >= len(battles)-1 or st.session_state.get("show_summary", False):
        st.markdown("---")
        st.markdown("<h2 style='text-align:center;'>CAMPAIGN CONCLUSION</h2>", unsafe_allow_html=True)

        score = st.session_state.history_score
        if score >= 85:   ending = "Decisive strategic victory – history significantly altered in your favor."
        elif score >= 65: ending = "Solid victory – objectives achieved at acceptable cost."
        elif score >= 45: ending = "Marginal success – war prolonged, heavy price paid."
        elif score >= 30: ending = "Strategic stalemate – neither side gains decisive advantage."
        else:             ending = "Campaign failure – enemy achieves dominance."

        st.markdown(f"**Final History Divergence Score:** {score}/100")
        st.markdown(f"**Outcome:** {ending}")

        if st.session_state.achievements:
            st.markdown("**Distinctions earned:**")
            for ach in st.session_state.achievements:
                st.markdown(f"- {ach}")

        st.markdown("**Battle Log**")
        for entry in st.session_state.turn_log:
            st.markdown(f"- {entry}")

        if st.button("RETURN TO MAIN MENU"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()

st.markdown("---")
st.caption(f"© {date.today().year}  ECHOES OF WAR  –  Historical grand strategy simulation")
