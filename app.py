import streamlit as st
import random
import json
import urllib.parse
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
    .stButton > button[kind="primary"] { background: #b91c1c; color: white; font-size: 1.2rem; padding: 14px 40px; border-radius: 12px; }
    .leader-img { border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

st.title("ECHOES OF WAR")
st.caption("Full Historical Campaigns • Real Stats • Save/Share • Leaderboards • Maps • 1.5–2 Hour Sessions")

# ===================== STATE WITH QUERY PARAMS FOR SAVE/LOAD =====================
@st.cache_data(ttl=300)
def get_state():
    params = st.query_params
    try:
        state = {
            'campaign_active': params.get('active', ['false'])[0] == 'true',
            'era': params.get('era', [''])[0],
            'battle_index': int(params.get('battle', ['0'])[0]),
            'manpower': int(params.get('man', ['100'])[0]),
            'supplies': int(params.get('sup', ['100'])[0]),
            'morale': int(params.get('mor', ['100'])[0]),
            'history_score': int(params.get('score', ['50'])[0])
        }
        return state
    except:
        return {}

def set_state(state):
    params = st.query_params
    params['active'] = ['true'] if state['campaign_active'] else ['false']
    if state['campaign_active']:
        params['era'] = [state['era']]
        params['battle'] = [str(state['battle_index'])]
        params['man'] = [str(state['manpower'])]
        params['sup'] = [str(state['supplies'])]
        params['mor'] = [str(state['morale'])]
        params['score'] = [str(state['history_score'])]
    st.query_params = params

state = get_state()
for key, val in state.items():
    if key != 'campaign_active':
        st.session_state[key] = val
st.session_state.campaign_active = state['campaign_active']

# ===================== CAMPAIGNS WITH MAPS & LEADERS =====================
campaigns = {
    "World War I – The Great War": [
        {"name": "First Battle of the Marne (1914)", "desc": "Stop the German advance on Paris", "base_cas": 250000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Battle_of_the_Marne_-_Map.jpg/800px-Battle_of_the_Marne_-_Map.jpg", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Joffre_1915.jpg/200px-Joffre_1915.jpg"},
        {"name": "Battle of Verdun (1916)", "desc": "The meat grinder of the Western Front", "base_cas": 700000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Battle_of_Verdun_map.png/800px-Battle_of_Verdun_map.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/P%C3%A9tain_1916.jpg/200px-P%C3%A9tain_1916.jpg"},
        {"name": "Battle of the Somme (1916)", "desc": "Bloodiest day in British history", "base_cas": 420000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Map_of_the_Battle_of_the_Somme%2C_1916.svg/800px-Map_of_the_Battle_of_the_Somme%2C_1916.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Sir_Douglas_Haig_portrait.jpg/200px-Sir_Douglas_Haig_portrait.jpg"},
        {"name": "Third Battle of Ypres (1917)", "desc": "Mud and attrition", "base_cas": 400000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Passchendaele_map.jpg/800px-Passchendaele_map.jpg", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Sir_Douglas_Haig_portrait.jpg/200px-Sir_Douglas_Haig_portrait.jpg"},
        {"name": "German Spring Offensive (1918)", "desc": "Germany's last push", "base_cas": 850000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Spring_Offensive_Map.jpg/800px-Spring_Offensive_Map.jpg", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Ludendorff_1918.jpg/200px-Ludendorff_1918.jpg"},
        {"name": "Hundred Days Offensive (1918)", "desc": "Final Allied victory", "base_cas": 180000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Hundred_Days_Offensive_map.svg/800px-Hundred_Days_Offensive_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Joffre_1915.jpg/200px-Joffre_1915.jpg"}
    ],
    "World War II – Global Conflict": [
        {"name": "Battle of Britain (1940)", "desc": "RAF vs Luftwaffe", "base_cas": 45000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Battle_of_Britain_map.svg/800px-Battle_of_Britain_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Dowding_portrait.jpg/200px-Dowding_portrait.jpg"},
        {"name": "Battle of Stalingrad (1942–43)", "desc": "Eastern Front turning point", "base_cas": 1900000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Map_Battle_of_Stalingrad-en.svg/800px-Map_Battle_of_Stalingrad-en.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Zhukov_1943.jpg/200px-Zhukov_1943.jpg"},
        {"name": "Battle of Midway (1942)", "desc": "Pacific carrier battle", "base_cas": 5000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Battle_of_Midway_map.svg/800px-Battle_of_Midway_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Nimitz_portrait.jpg/200px-Nimitz_portrait.jpg"},
        {"name": "D-Day Normandy (1944)", "desc": "Invasion of Europe", "base_cas": 10300, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Map_of_the_D-Day_landings.svg/800px-Map_of_the_D-Day_landings.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Eisenhower_d-day.jpg/200px-Eisenhower_d-day.jpg"},
        {"name": "Battle of the Bulge (1944–45)", "desc": "Ardennes counteroffensive", "base_cas": 190000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Battle_of_the_Bulge_map.svg/800px-Battle_of_the_Bulge_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Eisenhower_d-day.jpg/200px-Eisenhower_d-day.jpg"},
        {"name": "Battle of Berlin (1945)", "desc": "End of the Reich", "base_cas": 350000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Battle_of_Berlin_map.svg/800px-Battle_of_Berlin_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Zhukov_1943.jpg/200px-Zhukov_1943.jpg"}
    ],
    "Cold War – Proxy Wars & Escalation": [
        {"name": "Korean War – Inchon (1950)", "desc": "MacArthur's gamble", "base_cas": 3500, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Inchon_landing_map_%28en%29.svg/800px-Inchon_landing_map_%28en%29.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/MacArthur_portrait.jpg/200px-MacArthur_portrait.jpg"},
        {"name": "Vietnam – Tet Offensive (1968)", "desc": "VC/NVA surprise attack", "base_cas": 45000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Tet_Offensive_map.svg/800px-Tet_Offensive_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Westmoreland_portrait.jpg/200px-Westmoreland_portrait.jpg"},
        {"name": "Afghanistan Invasion (1979)", "desc": "Soviet quagmire begins", "base_cas": 15000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Afghan_War_map_1979.svg/800px-Afghan_War_map_1979.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Brezhnev_portrait.jpg/200px-Brezhnev_portrait.jpg"},
        {"name": "Falklands War (1982)", "desc": "British task force", "base_cas": 900, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Falklands_map.svg/800px-Falklands_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Thatcher_portrait.jpg/200px-Thatcher_portrait.jpg"},
        {"name": "Gulf War – Desert Storm (1991)", "desc": "Coalition liberation", "base_cas": 300, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Desert_Storm_map.svg/800px-Desert_Storm_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Norman_Schwarzkopf.jpg/200px-Norman_Schwarzkopf.jpg"},
        {"name": "Cuban Missile Crisis Alt (1962)", "desc": "Nuclear escalation", "base_cas": 500000, "map": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Cuban_Missile_Crisis_map.svg/800px-Cuban_Missile_Crisis_map.svg.png", "leader": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Kennedy_portrait.jpg/200px-Kennedy_portrait.jpg"}
    ]
}

# Sidebar
with st.sidebar:
    st.header("Campaign HQ")
    selected_campaign = st.selectbox("Choose Campaign", list(campaigns.keys()))
    
    if st.button("🚀 START / LOAD CAMPAIGN", type="primary"):
        set_state({
            'campaign_active': True,
            'era': selected_campaign,
            'battle_index': 0,
            'manpower': 100,
            'supplies': 100,
            'morale': 100,
            'history_score': 50
        })
        st.rerun()
    
    if st.session_state.campaign_active:
        if st.button("💾 SAVE & SHARE CAMPAIGN"):
            current_url = st.secrets.get("streamlit_url", st.experimental_get_query_params().to_dict().get("url", [""])[0]) or st.rerun()
            st.info(f"📋 Copy this URL to share your campaign:\n`{st.secrets.get('base_url', '') + st.experimental_get_query_params().to_dict().get('path', [''])[0]}`")  # Simplified; in practice use js for copy
            st.code(st.secrets.get('current_url', ''), language=None)
        
        if st.button("🔄 NEW CAMPAIGN"):
            set_state({'campaign_active': False})
            st.rerun()

# ===================== GAME =====================
if not st.session_state.campaign_active:
    st.info("👆 Click START to launch a full campaign. Share URLs with friends for leaderboards!")
    st.subheader("🏆 Global Leaderboard (Sample)")
    scores = random.choices(range(40,100), k=10)
    names = ["PatriotGen", "EagleEye", "LibertyCmd", "FreedomFtr", "ReaganFan"]
    for i, score in enumerate(sorted(scores)[-5:], 1):
        st.metric(f"#{i}", random.choice(names), score)
else:
    battles = campaigns[st.session_state.era]
    current = battles[st.session_state.battle_index]
    
    # Leader & Map visuals
    col1, col2 = st.columns([1,4])
    with col1:
        st.image(current["leader"], caption="Your Commander", width=150, use_column_width=True, clamp=True)
    with col2:
        st.image(current["map"], caption="Battlefield Map", use_column_width=True, clamp=True)
    
    st.header(f"{st.session_state.era}")
    st.progress(st.session_state.battle_index / len(battles))
    st.subheader(current["name"])
    st.write(current["desc"])
    
    # Resources
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Manpower", f"{st.session_state.manpower}%")
    col_m2.metric("Supplies", f"{st.session_state.supplies}%")
    col_m3.metric("Morale", f"{st.session_state.morale}%")
    
    # Battle decisions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Issue Orders")
    inf = st.slider("Infantry Focus %", 20, 80, 50)
    sup = st.slider("Support %", 10, 60, 35)
    agg = st.slider("Aggression 1-10", 1, 10, 5)
    tacs = st.multiselect("Tactics", ["Bombard", "Flank", "Air", "Night", "Defend", "Counter"], default=["Bombard"])
    
    if st.button("⚔️ COMMIT TO BATTLE", type="primary"):
        success = min(0.95, max(0.08, 0.48 + (inf/50*0.3) + (sup/35*0.35) + (agg/5*0.25) + len(tacs)*0.07 + random.uniform(-0.15,0.15)))
        cas = int(current["base_cas"] * (1.4 - success))
        
        mp_loss = int(25 - success*18)
        sup_loss = int(22 - success*15)
        mor_chg = int(18 * (success - 0.5))
        
        st.session_state.manpower = max(10, st.session_state.manpower - mp_loss)
        st.session_state.supplies = max(10, st.session_state.supplies - sup_loss)
        st.session_state.morale = max(10, min(100, st.session_state.morale + mor_chg))
        st.session_state.history_score += int((success - 0.5)*18)
        
        set_state(st.session_state)  # Save to URL
        
        st.success(f"VICTORY/DEFEAT • Success: {success:.0%} • Losses: {cas:,}")
        
        # Expanded random events
        events = [
            "Fog delayed artillery – poor start.",
            "Enemy deserters provide intel – bonus.",
            "Supply convoy ambushed.",
            "Heroic charge breaks lines.",
            "Rain floods trenches – stalemate.",
            "Air ace downs 5 enemy planes.",
            "Mutiny in ranks – morale hit.",
            "Breakthrough! Enemy retreats.",
            "Friendly fire incident.",
            "Captured enemy plans – advantage."
        ]
        st.balloons() if random.random() > 0.7 else None
        st.info(f"📰 Event: {random.choice(events)}")
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➡️ ADVANCE TO NEXT BATTLE"):
        if st.session_state.battle_index < len(battles)-1:
            st.session_state.battle_index += 1
            set_state(st.session_state)
            st.rerun()
        else:
            st.balloons()
            st.success("🏆 CAMPAIGN CONQUERED!")
            score = st.session_state.history_score
            endings = {
                range(85,101): "Total Triumph – War ends early, millions saved.",
                range(60,85): "Victory – As in history, but better.",
                range(40,60): "Grind – Pyrrhic win.",
                range(0,40): "Defeat – Axis/Soviets rise."
            }
            for r, end in endings.items():
                if score in r:
                    st.markdown(f"**Final Score: {score}/100**  \n{end}")
                    break

st.divider()
st.caption(f"© {date.today().year} Lawrence • ECHOES OF WAR • Share URLs • Built w/ Streamlit")
