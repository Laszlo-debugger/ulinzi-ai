import streamlit as st
import time
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime

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
    .stButton>button {width: 100%; border-radius: 5px; font-weight: bold; height: 3em;}
    .risk-high {color: #ff4b4b; font-weight: bold;}
    .risk-low {color: #00cc96; font-weight: bold;}
    .auth-box {border: 2px dashed #1E88E5; padding: 20px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if 'visual_state' not in st.session_state:
    st.session_state.visual_state = "secure" 
if 'transaction_status' not in st.session_state:
    st.session_state.transaction_status = "idle" # idle, blocked, verifying, cleared

# --- Header ---
st.markdown('<div class="main-header">🛡️ Ulinzi-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous National Cyber-Physical Intelligence Grid</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ System Parameters")
st.sidebar.markdown("**Identity:** Sentinel-X Node 01")
st.sidebar.markdown("**Status:** 🟢 ACTIVE (Zero-Trust Mode)")

mode = st.sidebar.selectbox("Select Operation Mode", 
    ["Dashboard Overview", "💸 Financial Sentinel (Anti-Fraud)", "🚨 Duress Protocol (Anti-Kidnap)", "⚔️ Sovereign Sentinel (Gov)"])

st.sidebar.divider()
st.sidebar.info("Tip: Enable your camera permissions for the Financial Sentinel demo.")

# --- 1. DASHBOARD OVERVIEW ---
if mode == "Dashboard Overview":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-val">1.2ms</div><div class="metric-label">Avg Response Latency</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-val">42</div><div class="metric-label">Attacks Neutralized</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-val">KES 1.5M</div><div class="metric-label">Fraud Prevented</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-val">100%</div><div class="metric-label">Govt Uptime</div></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🌍 Real-Time Threat Map (Network Traffic)")
    
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [-1.2921, 36.8219],
        columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=-1.2921, longitude=36.8219, zoom=11, pitch=50),
        layers=[
            pdk.Layer('HexagonLayer', data=map_data, get_position='[lon, lat]', radius=200, elevation_scale=4, elevation_range=[0, 1000], pickable=True, extruded=True),
        ],
    ))

# --- 2. FINANCIAL SENTINEL (THE CAMERA DEMO) ---
elif mode == "💸 Financial Sentinel (Anti-Fraud)":
    st.subheader("💳 Transaction Anomaly & Liveness Check")
    
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        st.markdown("#### 1. Simulate Transaction")
        amount = st.slider("Amount (KES)", 0, 1000000, 5000)
        location = st.selectbox("Location", ["Nairobi (Home)", "Bomet (Mullot - High Risk)", "International"])
        
        if st.button("Attempt Transfer"):
            if amount > 100000 or location == "Bomet (Mullot - High Risk)":
                st.session_state.transaction_status = "blocked"
            else:
                st.session_state.transaction_status = "cleared"
                
    with col_output:
        st.markdown("#### 2. AI Decision Engine")
        
        if st.session_state.transaction_status == "idle":
            st.info("Waiting for transaction...")
            
        elif st.session_state.transaction_status == "cleared":
            st.success("✅ RISK SCORE: 12/100. Transaction Approved.")
            
        elif st.session_state.transaction_status == "blocked":
            st.error("🔴 RISK SCORE: 98/100. ANOMALY DETECTED.")
            st.markdown("**Autonomous Action:** Circuit Breaker Engaged.")
            st.warning("⚠️ **LIVENESS CHECK REQUIRED**")
            
            st.markdown('<div class="auth-box">', unsafe_allow_html=True)
            st.write("Please take a photo to verify your identity:")
            
            # THE REAL WORKING CAMERA INPUT
            picture = st.camera_input("Take a Selfie", key="liveness_check")
            
            if picture:
                with st.spinner("Analyzing Biometrics..."):
                    time.sleep(2) # Simulate AI processing time
                    st.success("✅ FACE MATCH CONFIRMED (99.8%)")
                    st.success("🔓 ACCOUNT UNLOCKED. TRANSACTION PROCESSED.")
                    st.caption(f"Log ID: {datetime.now().strftime('%Y%m%d-%H%M%S')}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- 3. DURESS PROTOCOL ---
elif mode == "🚨 Duress Protocol (Anti-Kidnap)":
    st.subheader("🆘 Autonomous Duress Response")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Banking App Simulation")
        st.info("Scenario: Kidnapper demands you withdraw cash. Enter PIN.")
        
        pin_input = st.text_input("Enter PIN (Try 1234 for Normal, 9999 for Duress)", type="password", max_chars=4)
        
        if st.button("Submit PIN"):
            if pin_input == "1234":
                st.success("✅ Login Successful. Welcome, John.")
            elif pin_input == "9999":
                st.success("✅ Login Successful. Welcome, John.") 
                st.balloons() # Deception
                
                with col2:
                    st.error("🚨 DURESS SIGNAL SILENTLY ACTIVATED")
                    st.markdown("##### 🕵️‍♂️ Autonomous Backend Actions:")
                    
                    with st.status("Executing Code Red Protocol...", expanded=True):
                        st.write("📍 Triangulating GPS... **[Locked: -1.2921, 36.8219]**")
                        time.sleep(0.5)
                        st.write("🚓 Dispatching National Police Service... **[SENT]**")
                        time.sleep(0.5)
                        st.write("📸 Capturing Silent Front-Camera Evidence... **[SECURED]**")
                        time.sleep(0.5)
                        st.write("💸 Freezing Recipient M-PESA Account... **[SUCCESS]**")
                        time.sleep(0.5)
                        st.write("🔗 Logging Evidence to Blockchain... **[HASH: 0x7f8...a2]**")
                    
                    st.image("https://placehold.co/400x300/000000/FFF?text=SILENT+EVIDENCE+PHOTO%0A(Sent+to+DCI)", caption="Evidence #99281")

# --- 4. SOVEREIGN VISUAL SENTINEL ---
elif mode == "⚔️ Sovereign Sentinel (Gov)":
    st.subheader("🏛️ Government Website Integrity Monitor")
    
    col_sim, col_log = st.columns([2, 1])
    
    with col_sim:
        if st.session_state.visual_state == "secure":
            st.image("https://placehold.co/800x400/2E7D32/FFF?text=MINISTRY+OF+INTERIOR%0AOfficial+Secure+Portal", caption="Status: SECURE")
            if st.button("🔴 SIMULATE HACK (Inject Defacement)"):
                st.session_state.visual_state = "hacked"
                st.rerun()

        elif st.session_state.visual_state == "hacked":
            st.image("https://placehold.co/800x400/B71C1C/FFF?text=HACKED+BY+ANONYMOUS%0A(Hate+Symbols+Injected)", caption="Status: COMPROMISED")
            
            # Auto-Revert Simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.error("⚠️ ANOMALY DETECTED! AI AGENT ACTIVATED.")
            
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.005) # Fast revert
            
            st.session_state.visual_state = "secure"
            st.rerun()

    with col_log:
        st.markdown("### 🧠 Agent Logs")
        st.code(f"""
[09:45:01] Monitor: ACTIVE
[09:45:01] Visual Diff: 0.0%
[09:45:02] Visual Diff: 0.0%
[09:45:05] ALERT: Diff > 15%
[09:45:05] ACTION: REVERT
[09:45:06] SUCCESS: Restored
        """, language="bash")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("✅ **USSD Gateway (*334#)**: Connected")
st.sidebar.markdown("✅ **Mobile App API**: Connected")
st.markdown("---")
st.markdown("© 2025 Ulinzi-AI | **National Cyber-Intelligence & Prevention Platform**")
