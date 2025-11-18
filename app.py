import streamlit as st
import time
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime, timedelta
import random

# Try to import Plotly with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- Page Configuration ---
st.set_page_config(
    page_title="Ulinzi-AI | National Cyber-Intelligence Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3rem; 
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(30, 136, 229, 0.3);
    }
    
    .sub-header {
        font-size: 1.4rem; 
        color: #aaa; 
        text-align: center; 
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        border: 1px solid #333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }
    
    .metric-val {
        font-size: 2.5rem; 
        font-weight: 800;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-danger .metric-val {
        background: linear-gradient(135deg, #ff4b4b 0%, #b71c1c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-warning .metric-val {
        background: linear-gradient(135deg, #FF9800 0%, #E65100 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem; 
        color: #aaa;
        font-weight: 500;
    }
    
    .stButton>button {
        width: 100%; 
        border-radius: 8px; 
        font-weight: 600;
        padding: 0.75rem;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.4);
    }
    
    .module-card {
        background: rgba(30, 30, 30, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #1E88E5;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .alert-banner {
        background: linear-gradient(90deg, #b71c1c 0%, #ff4b4b 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .success-banner {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Custom gauge styles for fallback */
    .gauge-container {
        width: 100%;
        background: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
        position: relative;
    }
    
    .gauge-fill {
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper functions ---
def create_simple_gauge(risk_score):
    """Create a simple gauge visualization without Plotly"""
    color = "#00cc96"
    if risk_score > 50: color = "#FF9800"
    if risk_score > 85: color = "#ff4b4b"
    
    html = f"""
    <div class="gauge-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #aaa;">0</span>
            <span style="color: white; font-size: 1.5rem; font-weight: bold;">{risk_score}/100</span>
            <span style="color: #aaa;">100</span>
        </div>
        <div style="background: #333; border-radius: 10px; height: 20px;">
            <div class="gauge-fill" style="width: {risk_score}%; background: {color};"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="color: #00cc96;">Low</span>
            <span style="color: #FF9800;">Medium</span>
            <span style="color: #ff4b4b;">High</span>
        </div>
    </div>
    """
    return html

def generate_threat_data():
    """Generate simulated threat intelligence data"""
    threats = []
    for i in range(50):
        threats.append({
            "lat": -1.2921 + random.uniform(-0.5, 0.5),
            "lon": 36.8219 + random.uniform(-0.5, 0.5),
            "threat_level": random.choice(["low", "medium", "high", "critical"]),
            "type": random.choice(["SIM Swap", "DDoS", "Phishing", "Defacement", "Data Exfiltration"]),
            "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 120))
        })
    return threats

def generate_financial_data():
    """Generate simulated financial transaction data"""
    transactions = []
    for i in range(10):
        risk = random.randint(1, 100)
        status = "APPROVED" if risk < 50 else "FLAGGED" if risk < 85 else "BLOCKED"
        transactions.append({
            "Time": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).strftime("%H:%M"),
            "Amount (KES)": f"{random.randint(1000, 500000):,}",
            "Location": random.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]),
            "Risk Score": risk,
            "Status": status,
            "Type": random.choice(["Transfer", "Withdrawal", "Deposit", "Payment"])
        })
    return transactions

# --- Session State Init ---
if 'visual_state' not in st.session_state:
    st.session_state.visual_state = "secure"  # secure, hacked, restoring
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'threat_data' not in st.session_state:
    st.session_state.threat_data = generate_threat_data()
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = generate_financial_data()
if 'system_status' not in st.session_state:
    st.session_state.system_status = {
        "sovereign_sentinel": "🟢 ACTIVE",
        "financial_sentinel": "🟢 ACTIVE", 
        "duress_protocol": "🟢 ACTIVE",
        "intelligence_core": "🟢 ACTIVE"
    }

# --- Helper function for logs ---
def add_log(event_type, message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.audit_log.insert(0, {
        "time": timestamp, 
        "type": event_type, 
        "msg": message, 
        "status": status
    })

# --- Header ---
st.markdown('<div class="main-header">🛡️ ULINZI-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous National Cyber-Physical Intelligence Grid</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ System Command Center")
st.sidebar.markdown("**Identity:** Sentinel-X Node 01")
st.sidebar.markdown("**Status:** 🟢 ACTIVE (Zero-Trust Mode)")

mode = st.sidebar.selectbox("Select Operation Mode", 
    ["Dashboard Overview", "⚔️ Sovereign Sentinel (Gov)", "💸 Financial Sentinel (Bank)", "🚨 Duress Protocol (Citizen)", "🔍 Intelligence Core"])

st.sidebar.divider()

# System Status Sidebar
st.sidebar.subheader("System Status")
for module, status in st.session_state.system_status.items():
    st.sidebar.markdown(f"**{module.replace('_', ' ').title()}:** {status}")

st.sidebar.divider()
st.sidebar.info("💡 **Tip for Judges:** Use the controls in the main window to trigger threats and watch the AI respond autonomously.")

# --- 1. DASHBOARD OVERVIEW ---
if mode == "Dashboard Overview":
    
    # System Status Banner
    col_status1, col_status2, col_status3, col_status4 = st.columns(4)
    with col_status1:
        st.markdown('<div class="metric-card"><div class="metric-val">1.2ms</div><div class="metric-label">Avg Response Latency</div></div>', unsafe_allow_html=True)
    with col_status2:
        st.markdown('<div class="metric-card"><div class="metric-val">42</div><div class="metric-label">Attacks Neutralized (24h)</div></div>', unsafe_allow_html=True)
    with col_status3:
        st.markdown('<div class="metric-card"><div class="metric-val">KES 1.5M</div><div class="metric-label">Fraud Prevented</div></div>', unsafe_allow_html=True)
    with col_status4:
        st.markdown('<div class="metric-card"><div class="metric-val">100%</div><div class="metric-label">Govt Uptime</div></div>', unsafe_allow_html=True)

    st.divider()
    
    # System Modules Overview
    st.subheader("🛡️ Ulinzi-AI Defense Layers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="module-card">
            <h3>🏛️ Sovereign Sentinel</h3>
            <p>Autonomous website protection & defacement reversal</p>
            <div style="color: #4CAF50; font-weight: bold;">🟢 ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="module-card">
            <h3>💸 Financial Sentinel</h3>
            <p>Real-time fraud detection & SIM swap prevention</p>
            <div style="color: #4CAF50; font-weight: bold;">🟢 ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="module-card">
            <h3>🚨 Duress Protocol</h3>
            <p>Covert emergency response & life protection</p>
            <div style="color: #4CAF50; font-weight: bold;">🟢 ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="module-card">
            <h3>🔍 Intelligence Core</h3>
            <p>Attribution analysis & threat intelligence</p>
            <div style="color: #4CAF50; font-weight: bold;">🟢 ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Live Network Map and Analytics
    col_map, col_analytics = st.columns([2, 1])
    
    with col_map:
        st.subheader("🌍 Real-Time National Threat Map")
        
        # Enhanced threat visualization
        threat_df = pd.DataFrame(st.session_state.threat_data)
        
        # Color mapping for threat levels
        threat_df['color'] = threat_df['threat_level'].map({
            'low': [0, 255, 0, 160],
            'medium': [255, 165, 0, 160],
            'high': [255, 69, 0, 160],
            'critical': [255, 0, 0, 160]
        })
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=-1.2921,
                longitude=36.8219,
                zoom=6,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=threat_df,
                    get_position='[lon, lat]',
                    get_color='color',
                    get_radius=20000,
                    radius_min_pixels=5,
                    radius_max_pixels=15,
                    pickable=True,
                    filled=True
                ),
            ],
            tooltip={
                "html": "<b>Threat Level:</b> {threat_level} <br/> <b>Type:</b> {type}",
                "style": {"color": "white"}
            }
        ))
        
        st.caption("Live visualization of active threats across Kenya - Ulinzi-AI National Grid")
    
    with col_analytics:
        st.subheader("📊 Threat Analytics")
        
        # Threat distribution
        threat_counts = threat_df['threat_level'].value_counts()
        
        if PLOTLY_AVAILABLE:
            # Use Plotly if available
            fig_pie = px.pie(
                values=threat_counts.values, 
                names=threat_counts.index,
                color=threat_counts.index,
                color_discrete_map={
                    'low': '#00cc96', 
                    'medium': '#FF9800', 
                    'high': '#ff4b4b', 
                    'critical': '#b71c1c'
                }
            )
            fig_pie.update_layout(
                showlegend=True,
                margin=dict(l=20, r=20, t=30, b=20),
                height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Plotly not detected. Using simplified view.")
        
        st.markdown("**Recent Critical Alerts:**")
        recent_alerts = threat_df[threat_df['threat_level'] == 'critical'].head(3)
        for _, alert in recent_alerts.iterrows():
            st.error(f"🚨 {alert['type']} Detected")

# --- 2. SOVEREIGN VISUAL SENTINEL ---
elif mode == "⚔️ Sovereign Sentinel (Gov)":
    st.subheader("🏛️ Sovereign Visual Sentinel - Ministry Website Integrity Monitor")
    
    # Status banner
    if st.session_state.visual_state == "secure":
        st.markdown('<div class="success-banner">🛡️ ALL SYSTEMS SECURE - Monitoring 47 Critical Government Domains</div>', unsafe_allow_html=True)
    elif st.session_state.visual_state == "hacked":
        st.markdown('<div class="alert-banner">🚨 CRITICAL THREAT DETECTED - Autonomous Response Activated</div>', unsafe_allow_html=True)
    
    col_sim, col_log = st.columns([2, 1])
    
    with col_sim:
        st.markdown("### Live Visual State Monitor")
        
        # Visual State Logic
        if st.session_state.visual_state == "secure":
            st.image("https://placehold.co/800x400/2E7D32/FFF?text=MINISTRY+OF+INTERIOR%0AOfficial+Secure+Portal%0A%0A🛡️+ULINZI-AI+PROTECTED", 
                    caption="Status: SECURE (Gold Standard Match 99.9%) - Siamese Neural Network Active")
            
            if st.button("🔴 SIMULATE CYBERATTACK (Inject Defacement)", key="attack_btn", use_container_width=True):
                st.session_state.visual_state = "hacked"
                add_log("SOVEREIGN_SENTINEL", "Visual anomaly detected - Ministry of Interior website", "CRITICAL")
                st.rerun()
            
        elif st.session_state.visual_state == "hacked":
            st.image("https://placehold.co/800x400/B71C1C/FFF?text=HACKED+BY+ANONYMOUS%0AGovernment+Systems+Compromised%0A%0A⚠️+NATIONAL+SECURITY+THREAT", 
                    caption="Status: COMPROMISED (Visual Anomaly Detected - 12.4% Match)")
            
            # Auto-Revert Simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.error("🚨 VISUAL ANOMALY DETECTED! AI AGENT ACTIVATED.")
            
            # Enhanced progress simulation
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.warning(f"🔍 Analyzing pixel deviation: {i*3}%")
                elif i < 70:
                    status_text.info(f"🔄 Initiating Kubernetes rollback: {i}%")
                else:
                    status_text.info(f"✅ Restoring secure snapshot: {i}%")
                time.sleep(0.03)
            
            status_text.success("✅ AUTONOMOUS RECOVERY COMPLETE - Threat Neutralized")
            st.session_state.visual_state = "restoring"
            add_log("SOVEREIGN_SENTINEL", "Autonomous hot-swap completed - Site restored", "SUCCESS")
            time.sleep(1)
            st.rerun()
            
        elif st.session_state.visual_state == "restoring":
            st.success("✅ AUTONOMOUS RECOVERY VERIFIED - All Systems Secure")
            st.image("https://placehold.co/800x400/2E7D32/FFF?text=MINISTRY+OF+INTERIOR%0AOfficial+Secure+Portal%0A%0A✅+AUTONOMOUSLY+RESTORED", 
                    caption="Status: RESTORED (Autonomous Action Completed in 487ms)")
            
            st.balloons()
            if st.button("🔄 Reset Simulation", use_container_width=True):
                st.session_state.visual_state = "secure"
                st.rerun()

    with col_log:
        st.markdown("### 🧠 Autonomous Agent Logic")
        
        if st.session_state.visual_state == "secure":
            st.code("""[INFO] Siamese Neural Network: Active
[INFO] Gold Standard Match: 99.9% 
[INFO] Monitoring 47 critical domains
[INFO] Polling interval: 100ms
[INFO] Last health check: 12ms ago
[INFO] All systems nominal""", language="bash")
        
        elif st.session_state.visual_state == "hacked":
            st.code("""[ALERT] Visual deviation detected!
[CRITICAL] Siamese Network Match: 12.4%
[ACTION] Triggering autonomous response
[ACTION] Kubernetes: Initiating hot-swap
[ACTION] IP 102.44.213.45 blocked
[ACTION] Evidence hashed to blockchain
[ACTION] NC4 alert dispatched
[STATUS] Recovery in progress...""", language="bash")
        
        else:  # restoring
            st.code("""[SUCCESS] Autonomous recovery complete
[INFO] Recovery time: 487ms
[INFO] Zero downtime achieved
[INFO] Public access maintained
[INFO] Threat intelligence updated
[INFO] Returning to monitoring mode
[INFO] All systems secure""", language="bash")

# --- 3. FINANCIAL SENTINEL ---
elif mode == "💸 Financial Sentinel (Bank)":
    st.subheader("💳 Financial Sentinel - Real-time Fraud Detection & Prevention")
    st.markdown("Simulate transactions to test the AI's real-time anomaly detection capabilities.")
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.markdown("#### 🎯 Transaction Simulation")
        amount = st.slider("Transaction Amount (KES)", 0, 2000000, 50000, 1000)
        tx_time = st.slider("Time of Day (24h)", 0, 23, 14)
        location = st.selectbox("Location Pattern", 
            ["Nairobi (Home - Normal)", "Mombasa (Known Travel)", "Bomet (New/Anomalous)", "International (High Risk)", "3 AM Anomaly"])
        sim_swap = st.checkbox("🔴 SIM Swap Detected (Telco API)")
        behavioral_anomaly = st.checkbox("🎭 Behavioral Anomaly (Unusual Pattern)")
        
        # AI Logic Calculation (Reactive)
        risk_score = 15
        if amount > 50000: risk_score += 15
        if amount > 200000: risk_score += 25
        if amount > 500000: risk_score += 35
        if tx_time < 5 or tx_time > 23: 
            risk_score += 25
            if location == "3 AM Anomaly": risk_score += 30
        if location == "Bomet (New/Anomalous)": risk_score += 20
        if location == "International (High Risk)": risk_score += 35
        if behavioral_anomaly: risk_score += 25
        if sim_swap: risk_score = 99
        risk_score = min(risk_score, 100)

        if st.button("🚀 Process Transaction", use_container_width=True):
            add_log("FINANCIAL_SENTINEL", f"Processing KES {amount:,} transaction. Risk Score: {risk_score}", "INFO")
            if risk_score > 85:
                st.toast("Transaction BLOCKED due to High Risk", icon="🚫")
            elif risk_score > 50:
                st.toast("Circuit Breaker Triggered: Verification Required", icon="⚠️")
            else:
                st.toast("Transaction Approved", icon="✅")
    
    with col_output:
        st.markdown("#### 🧠 AI Risk Assessment Engine")
        
        # Dynamic visualization
        color = "#00cc96"
        decision = "✅ APPROVE"
        if risk_score > 50: 
            color = "#FF9800"
            decision = "⚠️ CHALLENGE"
        if risk_score > 85: 
            color = "#ff4b4b"
            decision = "🚫 BLOCK"
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score", 'font': {'size': 24, 'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(0, 204, 150, 0.3)'},
                        {'range': [50, 85], 'color': 'rgba(255, 152, 0, 0.3)'},
                        {'range': [85, 100], 'color': 'rgba(255, 75, 75, 0.3)'}
                    ],
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(create_simple_gauge(risk_score), unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='text-align: center; color: {color};'>{decision}</h3>", unsafe_allow_html=True)
        
        if risk_score > 85:
            st.error("""
            **Critical Threat Identified:**
            - SIM swap / Anomaly confirmed via telco API
            - Account immediately frozen
            - Law enforcement notified
            """)
            if st.checkbox("Show Liveness Check"):
                st.image("https://placehold.co/400x300/000000/FFF?text=Live+Face+Scan+Required", caption="Biometric Challenge Active")

    st.divider()
    st.subheader("📋 Recent Transaction Logs")
    st.dataframe(pd.DataFrame(st.session_state.financial_data), use_container_width=True)

# --- 4. DURESS PROTOCOL ---
elif mode == "🚨 Duress Protocol (Citizen)":
    st.subheader("🆘 Autonomous Duress Response System")
    st.info("This system protects citizens during physical threats by enabling covert emergency signaling.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Banking App Simulation")
        st.markdown("You are being forced to withdraw money. **Test the logic:**")
        st.markdown("- **Normal PIN:** `1234`")
        st.markdown("- **Duress PIN:** `9999` (Triggers Alarm)")
        
        pin_input = st.text_input("Enter PIN", type="password", max_chars=4, placeholder="Enter 4-digit PIN")
        amount = st.slider("Withdrawal Amount (KES)", 1000, 500000, 50000)
        
        if st.button("Process Withdrawal", use_container_width=True):
            if pin_input == "1234":
                st.success("✅ Transaction Successful")
                st.info(f"KES {amount:,} has been withdrawn.")
            elif pin_input == "9999":
                # THE COVERT RESPONSE
                st.success("✅ Transaction Appears Successful") 
                st.balloons()
                
                # THE REAL AUTONOMOUS RESPONSE
                with col2:
                    st.markdown('<div class="alert-banner">🚨 SILENT DURESS SIGNAL DETECTED</div>', unsafe_allow_html=True)
                    st.markdown("**Autonomous Emergency Protocol Activated:**")
                    
                    with st.status("Executing Code Red Protocol...", expanded=True):
                        time.sleep(1)
                        st.write("📍 GPS Triangulation... **[Locked: -1.2921, 36.8219]**")
                        time.sleep(0.5)
                        st.write("🚓 Alerting National Police Service... **[SENT]**")
                        time.sleep(0.5)
                        st.write("💸 Freezing Recipient Account... **[EXECUTED]**")
                        time.sleep(0.5)
                        st.write("🔗 Immutable Evidence Log... **[HASHED]**")
                    
                    st.map(pd.DataFrame({'lat': [-1.2921], 'lon': [36.8219]}), zoom=14)
                    st.caption("Live Tracking sent to DCI/Police HQ")
            else:
                st.warning("Incorrect PIN. Please try again.")

# --- 5. INTELLIGENCE CORE ---
elif mode == "🔍 Intelligence Core":
    st.subheader("🔍 Intelligence Core - Attribution & Threat Analysis")
    st.markdown("Advanced AI-powered attribution and threat intelligence analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌐 Chain Analysis Engine")
        attack_data = pd.DataFrame({
            'Stage': ['Initial Access', 'Lateral Movement', 'Data Exfiltration', 'Financial Transfer', 'Money Laundering'],
            'Time': ['14:30:02', '14:35:18', '14:41:45', '14:50:22', '15:15:10'],
            'Confidence': [85, 92, 78, 95, 88],
            'Status': ['Detected', 'Detected', 'Prevented', 'Tracked', 'Monitoring']
        })
        st.dataframe(attack_data, use_container_width=True)
        
        st.markdown("#### 🎯 Attribution Analysis")
        col_att1, col_att2, col_att3 = st.columns(3)
        col_att1.metric("Confidence", "94%", "High")
        col_att2.metric("Actor", "APT-41", "Known")
        col_att3.metric("Method", "Res-Proxy", "Botnet")
        
    with col2:
        st.markdown("#### 🕸️ Transaction Network Analysis")
        st.image("https://placehold.co/600x300/1a1a1a/FFFFFF?text=Graph+Neural+Network+Analysis%0AIdentifying+Money+Laundering+Patterns", 
                caption="GNN identifying funnel accounts across banking network")

# --- Main Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("✅ **USSD Gateway (*334#)**: Connected")
st.sidebar.markdown("✅ **Mobile App API**: Connected")
st.sidebar.markdown("✅ **Internet Banking**: Connected")
st.sidebar.markdown("✅ **Telco Integration**: Active")
st.markdown("---")
st.markdown("© 2025 Ulinzi-AI | **National Cyber-Intelligence & Prevention Platform** | Protecting Kenya's Digital Sovereignty")
