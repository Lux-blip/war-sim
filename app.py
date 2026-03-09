import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="ECHOES OF WAR", page_icon="⚔️", layout="wide")

# Modern dark military theme (mature & clean)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #0a0e17 !important; color: #e2e8f0 !important; }
    h1, h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    .card { background: #1e293b; padding: 24px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; }
    .red { color: #ef4444; }
    .bar { background: linear-gradient(90deg, #ef4444, #f59e0b); height: 12px; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Historical War Simulator • Real Stats • Mature Strategy")

# Sidebar controls
era = st.sidebar.selectbox("Select Era", ["WW1", "WW2", "Cold War"])

scenarios = {
    "WW1": ["Battle of the Somme (1916)"],
    "WW2": ["D-Day Normandy (1944)"],
    "Cold War": ["Inchon Landing + Escalation (1950)"]
}

scenario = st.sidebar.selectbox("Select Scenario", scenarios[era])

# Real historical data
data = {
    "WW1": {
        "title": "Battle of the Somme (1916)",
        "allied_troops": 420000,
        "allied_casualties_hist": 420000,
        "enemy_troops": 500000,
        "enemy_casualties_hist": 500000,
        "desc": "141 days of brutal trench warfare. British & French vs German Empire."
    },
    "WW2": {
        "title": "D-Day Normandy (1944)",
        "allied_troops": 156000,
        "allied_casualties_hist": 10300,
        "enemy_troops": 38000,
        "enemy_casualties_hist": 9000,
        "desc": "Largest amphibious invasion in history. Allies vs Nazi Germany."
    },
    "Cold War": {
        "title": "Inchon Landing + Escalation (1950)",
        "allied_troops": 75000,
        "allied_casualties_hist": 3500,
        "enemy_troops": 40000,
        "enemy_casualties_hist": 12500,
        "desc": "UN forces turn the tide in Korea. Risk of full-scale war with China."
    }
}

d = data[era]
st.header(d["title"])
st.write(d["desc"])

# Interactive Command Center
st.subheader("Command Center – Allocate Your Forces")
col1, col2, col3 = st.columns(3)

with col1:
    infantry = st.slider("Infantry Divisions", 30, 70, 50)
with col2:
    artillery = st.slider("Artillery & Air Support", 10, 40, 25)
with col3:
    morale = st.slider("Morale & Logistics", 40, 90, 65)

tactic = st.radio("Choose Primary Tactic", 
                  ["Heavy Bombardment", "Flank Maneuver", "Rapid Assault", "Defensive Hold"])

if st.button("LAUNCH OPERATION", type="primary"):
    # Simulation engine using real historical base + player choices
    base_success = 0.45  # historical baseline
    modifier = (infantry/50 * 0.3) + (artillery/25 * 0.3) + (morale/65 * 0.2) + \
               (1.2 if tactic in ["Flank Maneuver", "Heavy Bombardment"] else 0.8)
    
    success = min(0.95, max(0.1, base_success * modifier + random.uniform(-0.1, 0.1)))
    
    allied_casualties = int(d["allied_casualties_hist"] * (1.3 - success * 0.8))
    enemy_casualties = int(d["enemy_casualties_hist"] * (0.7 + success * 0.8))
    
    st.success(f"OPERATION COMPLETE – Success Rate: **{success:.0%}**")
    
    st.subheader("After Action Report")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Your Forces Casualties", f"{allied_casualties:,}", f"-{int(d['allied_casualties_hist']-allied_casualties):,}")
    with c2:
        st.metric("Enemy Casualties", f"{enemy_casualties:,}", f"+{int(enemy_casualties-d['enemy_casualties_hist']):,}")
    
    st.progress(success, text="Front Line Advance")
    st.bar_chart({"Your Losses": [allied_casualties], "Enemy Losses": [enemy_casualties]})

    st.write("**Strategic Note:**" + 
             (" Bold flank paid off – history changed." if success > 0.7 else 
              " Heavy losses. The fog of war is unforgiving.") )

# Footer
st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Built with real history & Python")
