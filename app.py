import streamlit as st
import time
import pandas as pd
import numpy as np
import pydeck as pdk

# --- Page Configuration ---
st.set_page_config(
    page_title="Ulinzi-AI | Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E88E5; text-align: center; font-weight: 800;}
    .sub-header {font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem;}
    .metric-card {background-color: #1E1E1E; padding: 1rem; border-radius: 8px; color: white; text-align: center; border: 1px solid #333;}
    .metric-val {font-size: 2rem; font-weight: bold; color: #4CAF50;}
    .metric-label {font-size: 0.9rem; color: #aaa;}
    .stButton>button {width: 100%; border-radius: 5px; font-weight: bold;}
    .risk-high {color: #ff4b4b; font-weight: bold;}
    .risk-low {color: #00cc96; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if 'visual_state' not in st.session_state:
    st.session_state.visual_state = "secure" # secure, hacked, restoring
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- Helper Functions ---
def add_log(event_type, message, status="INFO"):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.audit_log.insert(0, {"time": timestamp, "type": event_type, "msg": message, "status": status})

# --- Header ---
st.markdown('<div class="main-header">🛡️ Ulinzi-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous National Cyber-Physical Intelligence Grid</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ System Parameters")
st.sidebar.markdown("**Identity:** Sentinel-X Node 01")
st.sidebar.markdown("**Status:** 🟢 ACTIVE (Zero-Trust Mode)")

mode = st.sidebar.selectbox("Select Operation Mode", 
    ["Dashboard Overview", "⚔️ Sovereign Sentinel (Gov)", "💸 Financial Sentinel (Bank)", "🚨 Duress Protocol (Citizen)"])

st.sidebar.divider()
st.sidebar.info("Tip for Judges: Use the controls in the main window to trigger threats and watch the AI respond autonomously.")

# --- 1. DASHBOARD OVERVIEW ---
if mode == "Dashboard Overview":
    
    # Live Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-val">1.2ms</div><div class="metric-label">Avg Response Latency</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-val">42</div><div class="metric-label">Attacks Neutralized (24h)</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-val">KES 1.5M</div><div class="metric-label">Fraud Prevented</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-val">100%</div><div class="metric-label">Govt Uptime</div></div>', unsafe_allow_html=True)

    st.divider()
    
    # Live Network Map
    st.subheader("🌍 Real-Time Threat Map (Network Traffic)")
    
    # Random data for map visualization
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [-1.2921, 36.8219],
        columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(
            latitude=-1.2921,
            longitude=36.8219,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=map_data,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))
    
    st.caption("Live visualization of IPs accessing Sovereign Infrastructure (Nairobi Node)")

# --- 2. SOVEREIGN VISUAL SENTINEL ---
elif mode == "⚔️ Sovereign Sentinel (Gov)":
    st.subheader("🏛️ Ministry Website Integrity Monitor")
    
    col_sim, col_log = st.columns([2, 1])
    
    with col_sim:
        st.markdown("### Live Visual State")
        
        # Visual State Logic
        if st.session_state.visual_state == "secure":
            st.image("https://placehold.co/800x400/2E7D32/FFF?text=MINISTRY+OF+INTERIOR%0AOfficial+Secure+Portal", caption="Status: SECURE (Gold Standard Match)")
            
            if st.button("🔴 SIMULATE CYBERATTACK (Inject Defacement)"):
                st.session_state.visual_state = "hacked"
                st.rerun()

        elif st.session_state.visual_state == "hacked":
            st.image("https://placehold.co/800x400/B71C1C/FFF?text=HACKED+BY+ANONYMOUS%0A(Hate+Symbols+Injected)", caption="Status: COMPROMISED (Visual Anomaly Detected)")
            
            # Auto-Revert Simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.error("⚠️ ANOMALY DETECTED! AI AGENT ACTIVATED.")
            time.sleep(1)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            
            status_text.info("🔄 ROLLING BACK TO SECURE SNAPSHOT...")
            time.sleep(1)
            st.session_state.visual_state = "restoring"
            st.rerun()
            
        elif st.session_state.visual_state == "restoring":
            st.success("✅ REVERT COMPLETE. Site Restored.")
            st.image("https://placehold.co/800x400/2E7D32/FFF?text=MINISTRY+OF+INTERIOR%0AOfficial+Secure+Portal", caption="Status: RESTORED (Autonomous Action Taken)")
            if st.button("Reset Simulation"):
                st.session_state.visual_state = "secure"
                st.rerun()

    with col_log:
        st.markdown("### 🧠 Agent Logic Logs")
        if st.session_state.visual_state == "secure":
            st.code("""[INFO] Siamese Network: Match 99.9%
[INFO] No deviations detected.
[INFO] Polling interval: 100ms""", language="bash")
        elif st.session_state.visual_state == "hacked":
            st.code("""[ALERT] Siamese Network: Match 12.4%
[CRITICAL] Visual deviation > Threshold
[ACTION] Triggering Kubernetes Rollback
[ACTION] Locking IP 102.44.x.x
[LOG] Evidence hashed to Blockchain""", language="bash")

# --- 3. FINANCIAL SENTINEL ---
elif mode == "💸 Financial Sentinel (Bank)":
    st.subheader("💳 Transaction Anomaly Detection (The 'Mullot' Defense)")
    
    st.markdown("Use the controls to simulate a transaction. Watch the **Risk Score** change in real-time.")
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        amount = st.slider("Transaction Amount (KES)", 0, 1000000, 5000)
        tx_time = st.slider("Time of Day (24h)", 0, 23, 14)
        location = st.selectbox("Location", ["Nairobi (Home)", "Mombasa (Known)", "Bomet (New/Anomalous)", "International (High Risk)"])
        sim_swap = st.checkbox("Simulate Recent SIM Swap?")
        
    # AI Logic Simulation
    risk_score = 10 # Base risk
    
    # Rule 1: Amount
    if amount > 100000: risk_score += 30
    if amount > 500000: risk_score += 40
    
    # Rule 2: Time (3 AM Anomaly)
    if tx_time < 5 or tx_time > 23: risk_score += 20
    
    # Rule 3: Location
    if location == "Bomet (New/Anomalous)": risk_score += 25
    if location == "International (High Risk)": risk_score += 50
    
    # Rule 4: SIM Swap (The Kill Switch)
    if sim_swap: risk_score = 99 # Instant block
    
    # Cap score
    risk_score = min(risk_score, 100)
    
    with col_output:
        st.markdown("### 🧠 AI Risk Assessment")
        
        # Dynamic Color
        color = "green"
        if risk_score > 50: color = "orange"
        if risk_score > 85: color = "red"
        
        st.markdown(f"""
        <div style="text-align: center; font-size: 3rem; font-weight: bold; color: {color}; border: 2px solid {color}; border-radius: 10px; padding: 20px;">
            {risk_score}/100
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Decision:**")
        if risk_score < 50:
            st.success("✅ **APPROVE**: Transaction looks normal.")
        elif risk_score < 85:
            st.warning("⚠️ **CHALLENGE**: Circuit Breaker Triggered. Video Liveness Check Required.")
        else:
            st.error("🚫 **BLOCK**: Critical Threat. Account Frozen. Telco Mismatch.")

# --- 4. DURESS PROTOCOL ---
elif mode == "🚨 Duress Protocol (Citizen)":
    st.subheader("🆘 Autonomous Duress Response")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Banking App Simulation")
        st.info("You are being forced to withdraw money. Enter your PIN.")
        
        pin_input = st.text_input("Enter PIN (Try 1234 for Normal, 9999 for Duress)", type="password", max_chars=4)
        
        if st.button("Submit PIN"):
            if pin_input == "1234":
                st.success("✅ Login Successful. Welcome, John.")
            elif pin_input == "9999":
                # THE TRICK
                st.success("✅ Login Successful. Welcome, John.") 
                st.balloons() # Fake success visual
                
                # THE REALITY
                with col2:
                    st.error("🚨 DURESS SIGNAL DETECTED [SILENT]")
                    st.markdown("**Autonomous Actions Executed:**")
                    st.code("""
1. [GPS] Lat: -1.2921, Lon: 36.8219
2. [API] POST /police/alert (CODE RED)
3. [API] POST /mpesa/freeze_target
4. [LOG] Evidence #D-99182 created on Blockchain
                    """, language="json")
                    
                    st.map(pd.DataFrame({'lat': [-1.2921], 'lon': [36.8219]}))
                    st.caption("Live Tracking sent to DCI/Police HQ")
            else:
                st.warning("Incorrect PIN")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Ulinzi-AI | **National Cyber-Intelligence & Prevention Platform**")
