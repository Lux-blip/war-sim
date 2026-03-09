import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# Mature military dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .red { color: #ef4444; }
    .bar { height: 14px; border-radius: 7px; background: linear-gradient(90deg, #ef4444, #f59e0b); }
    .stButton > button[kind="primary"] { background: #b91c1c; color: white; font-size: 1.2rem; padding: 14px 40px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Full Historical Campaigns • Real Stats • 1.5–2 Hour Play Sessions")

# ===================== SESSION STATE FOR CAMPAIGN PERSISTENCE =====================
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

# ===================== CAMPAIGNS =====================
campaigns = {
    "World War I – The Great War": [
        {"name": "First Battle of the Marne (1914)", "desc": "Stop the German advance on Paris", "base_cas": 250000},
        {"name": "Battle of Verdun (1916)", "desc": "The meat grinder of the Western Front", "base_cas": 700000},
        {"name": "Battle of the Somme (1916)", "desc": "Bloodiest day in British military history", "base_cas": 420000},
        {"name": "Third Battle of Ypres (Passchendaele) (1917)", "desc": "Mud, rain, and attrition", "base_cas": 400000},
        {"name": "German Spring Offensive (1918)", "desc": "Last chance for Germany", "base_cas": 850000},
        {"name": "Hundred Days Offensive (1918)", "desc": "The final Allied push", "base_cas": 180000}
    ],
    "World War II – Global Conflict": [
        {"name": "Battle of Britain (1940)", "desc": "Air war for survival", "base_cas": 45000},
        {"name": "Battle of Stalingrad (1942–43)", "desc": "Turning point on the Eastern Front", "base_cas": 1900000},
        {"name": "Battle of Midway (1942)", "desc": "Pacific naval showdown", "base_cas": 5000},
        {"name": "D-Day Normandy (1944)", "desc": "Largest amphibious invasion ever", "base_cas": 10300},
        {"name": "Battle of the Bulge (1944–45)", "desc": "Hitler’s last gamble", "base_cas": 190000},
        {"name": "Battle of Berlin (1945)", "desc": "Fall of the Third Reich", "base_cas": 350000}
    ],
    "Cold War – Proxy Wars & Escalation": [
        {"name": "Korean War – Inchon & Chinese Intervention (1950)", "desc": "Risk of WW3", "base_cas": 3500},
        {"name": "Vietnam – Tet Offensive (1968)", "desc": "Psychological turning point", "base_cas": 45000},
        {"name": "Soviet Invasion of Afghanistan (1979–89)", "desc": "Soviet Vietnam", "base_cas": 15000},
        {"name": "Falklands War (1982)", "desc": "Modern naval & air campaign", "base_cas": 900},
        {"name": "Gulf War – Operation Desert Storm (1991)", "desc": "High-tech blitzkrieg", "base_cas": 300},
        {"name": "Cuban Missile Crisis Escalation (1962 Alternate)", "desc": "Nuclear brinkmanship", "base_cas": 500000}
    ]
}

# Sidebar
with st.sidebar:
    st.header("Campaign Selection")
    selected_campaign = st.selectbox("Choose War Campaign", list(campaigns.keys()))
    
    if st.button("🚀 START NEW CAMPAIGN", type="primary"):
        st.session_state.campaign_active = True
        st.session_state.era = selected_campaign
        st.session_state.battle_index = 0
        st.session_state.manpower = 100
        st.session_state.supplies = 100
        st.session_state.morale = 100
        st.session_state.history_score = 50
        st.rerun()
    
    if st.session_state.campaign_active and st.button("🔄 Reset Campaign"):
        st.session_state.campaign_active = False
        st.rerun()

# ===================== MAIN GAME =====================
if not st.session_state.campaign_active:
    st.info("Select a campaign and click START NEW CAMPAIGN to begin a 1.5–2 hour strategic experience.")
else:
    battles = campaigns[st.session_state.era]
    current_battle = battles[st.session_state.battle_index]
    
    st.header(f"Campaign: {st.session_state.era}")
    st.progress(st.session_state.battle_index / len(battles), text=f"Battle {st.session_state.battle_index + 1} of {len(battles)}")
    
    st.subheader(current_battle["name"])
    st.write(current_battle["desc"])
    
    # Resource panel
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.metric("Manpower", f"{st.session_state.manpower}%", delta=None)
    with col_r2:
        st.metric("Supplies", f"{st.session_state.supplies}%", delta=None)
    with col_r3:
        st.metric("Morale", f"{st.session_state.morale}%", delta=None)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Command Decisions – Battle Phase")
    
    infantry = st.slider("Infantry & Ground Forces (%)", 20, 80, 50)
    support = st.slider("Artillery / Air / Naval Support (%)", 10, 60, 35)
    aggression = st.slider("Aggression Level (1–10)", 1, 10, 5)
    
    tactics = st.multiselect("Special Tactics", 
        ["Heavy Bombardment", "Armored Breakthrough", "Night Assault", "Air Superiority", "Logistical Defense", "Rapid Counter-Attack"],
        default=["Heavy Bombardment"])
    
    if st.button("EXECUTE BATTLE", type="primary"):
        # Realistic simulation with carry-over effects
        base_success = 0.48
        mod = (infantry/50 * 0.3) + (support/35 * 0.35) + (aggression/5 * 0.25)
        tactic_bonus = len(tactics) * 0.07
        success = min(0.95, max(0.08, base_success + mod + tactic_bonus + random.uniform(-0.15, 0.15)))
        
        casualties = int(current_battle["base_cas"] * (1.4 - success))
        
        # Resource changes
        manpower_loss = int(25 - success * 18)
        supplies_loss = int(22 - success * 15)
        morale_change = int(18 * (success - 0.5))
        
        st.session_state.manpower = max(10, st.session_state.manpower - manpower_loss)
        st.session_state.supplies = max(10, st.session_state.supplies - supplies_loss)
        st.session_state.morale = max(10, min(100, st.session_state.morale + morale_change))
        st.session_state.history_score += int((success - 0.5) * 18)
        
        st.success(f"Battle Complete • Success Rate: **{success:.0%}** • Casualties: **{casualties:,}**")
        
        # Random historical event
        events = ["Rain turned the battlefield into mud.", "Enemy reinforcements arrived early.", "Your intelligence was spot-on.", "A surprise flanking maneuver worked perfectly."]
        st.info("Event: " + random.choice(events))
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Continue button
    if st.button("➡️ Continue to Next Battle"):
        if st.session_state.battle_index < len(battles) - 1:
            st.session_state.battle_index += 1
            st.rerun()
        else:
            # CAMPAIGN END SCREEN
            st.balloons()
            st.success("CAMPAIGN COMPLETE")
            final_score = st.session_state.history_score
            if final_score > 85:
                ending = "You changed history — decisive victory. The war ends years earlier."
            elif final_score > 60:
                ending = "Hard-fought victory. The Allies (or your side) prevail, but at enormous cost."
            elif final_score > 40:
                ending = "Stalemate. The war drags on longer than in real history."
            else:
                ending = "Strategic defeat. The enemy gains the upper hand."
            
            st.write(f"**Final History Divergence Score: {final_score}**")
            st.write(ending)
            st.caption("Your decisions altered the course of the 20th century.")

# Footer
st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Full campaigns • Real historical stats")
