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
    st.warning("Plotly not available - using simplified visualizations")

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
        color: #666; 
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
    
    .metric-danger {
        background: linear-gradient(135deg, #ff4b4b 0%, #b71c1c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-warning {
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
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.4);
    }
    
    .attack-button {
        background: linear-gradient(135deg, #ff4b4b 0%, #b71c1c 100%) !important;
    }
    
    .attack-button:hover {
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4) !important;
    }
    
    .risk-high {color: #ff4b4b; font-weight: bold;}
    .risk-medium {color: #FF9800; font-weight: bold;}
    .risk-low {color: #00cc96; font-weight: bold;}
    
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
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%);
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

# --- Helper functions for fallback visualizations ---
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

def create_simple_pie_chart(threat_counts):
    """Create a simple pie chart visualization without Plotly"""
    total = sum(threat_counts.values)
    html = '<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">'
    
    color_map = {
        'low': '#00cc96',
        'medium': '#FF9800', 
        'high': '#ff4b4b',
        'critical': '#b71c1c'
    }
    
    for level, count in threat_counts.items():
        percentage = (count / total) * 100
        html += f"""
        <div style="text-align: center; margin: 10px;">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: {color_map.get(level, '#666')}; 
                        display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {percentage:.0f}%
            </div>
            <div style="margin-top: 5px; font-size: 0.8rem; color: #aaa;">
                {level.title()}<br>({count})
            </div>
        </div>
        """
    html += '</div>'
    return html

# --- Session State Init ---
if 'visual_state' not in st.session_state:
    st.session_state.visual_state = "secure"  # secure, hacked, restoring
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'threat_data' not in st.session_state:
    st.session_state.threat_data = []
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = []
if 'system_status' not in st.session_state:
    st.session_state.system_status = {
        "sovereign_sentinel": "🟢 ACTIVE",
        "financial_sentinel": "🟢 ACTIVE", 
        "duress_protocol": "🟢 ACTIVE",
        "intelligence_core": "🟢 ACTIVE"
    }

# --- Helper Functions ---
def add_log(event_type, message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.audit_log.insert(0, {
        "time": timestamp, 
        "type": event_type, 
        "msg": message, 
        "status": status
    })

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
    for i in range(100):
        risk = random.randint(1, 100)
        status = "APPROVED" if risk < 30 else "FLAGGED" if risk < 70 else "BLOCKED"
        transactions.append({
            "time": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).strftime("%H:%M"),
            "amount": random.randint(1000, 500000),
            "location": random.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]),
            "risk_score": risk,
            "status": status,
            "type": random.choice(["Transfer", "Withdrawal", "Deposit", "Payment"])
        })
    return transactions

# Initialize data
if not st.session_state.threat_data:
    st.session_state.threat_data = generate_threat_data()
if not st.session_state.financial_data:
    st.session_state.financial_data = generate_financial_data()

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

# System Status
st.sidebar.subheader("System Status")
for module, status in st.session_state.system_status.items():
    st.sidebar.markdown(f"**{module.replace('_', ' ').title()}:** {status}")

st.sidebar.divider()
st.sidebar.info("💡 **Tip for Judges:** Use the controls to trigger threats and watch the AI respond autonomously in real-time.")

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
                    get_radius=50000,
                    radius_min_pixels=3,
                    radius_max_pixels=10,
                    pickable=True
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
                height=250
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            # Use fallback visualization
            st.markdown(create_simple_pie_chart(threat_counts), unsafe_allow_html=True)
        
        # Recent alerts
        st.markdown("**Recent Alerts:**")
        recent_alerts = threat_df.nlargest(5, 'timestamp')
        for _, alert in recent_alerts.iterrows():
            st.write(f"• {alert['type']} - **{alert['threat_level'].upper()}**")

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
            
            col_attack, col_reset = st.columns(2)
            with col_attack:
                if st.button("🔴 SIMULATE COORDINATED CYBERATTACK", key="attack_btn", use_container_width=True):
                    st.session_state.visual_state = "hacked"
                    add_log("SOVEREIGN_SENTINEL", "Visual anomaly detected - Ministry of Interior website", "CRITICAL")
                    st.rerun()
            
        elif st.session_state.visual_state == "hacked":
            st.image("https://placehold.co/800x400/B71C1C/FFF?text=HACKED+BY+ANONYMOUS%0AGovernment+Systems+Compromised%0A%0A⚠️+NATIONAL+SECURITY+THREAT", 
                    caption="Status: COMPROMISED (Visual Anomaly Detected - 12.4% Match)")
            
            # Auto-Revert Simulation with enhanced visualization
            progress_bar = st.progress(0)
            status_text = st.empty()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Response Time", "142ms", delta="Autonomous")
            with col2:
                st.metric("Threat Level", "CRITICAL", delta="Defacement")
            with col3:
                st.metric("AI Confidence", "99.7%", delta="High")
            
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
                time.sleep(0.02)
            
            status_text.success("✅ AUTONOMOUS RECOVERY COMPLETE - Threat Neutralized")
            st.session_state.visual_state = "restoring"
            add_log("SOVEREIGN_SENTINEL", "Autonomous hot-swap completed - Site restored", "SUCCESS")
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
        
        # Enhanced log display
        log_container = st.container()
        with log_container:
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
        
        st.divider()
        st.markdown("### 📈 System Metrics")
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("Domains Protected", "47", "All Critical")
        with col_metric2:
            st.metric("Uptime", "100%", "30 days")

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
        
        if st.button("🚀 Process Transaction", use_container_width=True):
            add_log("FINANCIAL_SENTINEL", f"Processing KES {amount:,} transaction", "INFO")
    
    # Advanced AI Logic Simulation
    risk_score = 15  # Base risk
    
    # Rule 1: Amount-based risk
    if amount > 50000: risk_score += 15
    if amount > 200000: risk_score += 25
    if amount > 500000: risk_score += 35
    
    # Rule 2: Time-based anomalies (3 AM circuit breaker)
    if tx_time < 5 or tx_time > 23: 
        risk_score += 25
        if location == "3 AM Anomaly":
            risk_score += 30
    
    # Rule 3: Location intelligence
    if location == "Bomet (New/Anomalous)": risk_score += 20
    if location == "International (High Risk)": risk_score += 35
    
    # Rule 4: SIM Swap (Instant block)
    if sim_swap: 
        risk_score = 99  # Instant block
    
    # Rule 5: Behavioral analytics
    if behavioral_anomaly: risk_score += 25
    
    # Rule 6: Graph Neural Network detection
    if amount > 300000 and location == "International (High Risk)":
        risk_score += 20  # Potential money laundering pattern
    
    # Cap score
    risk_score = min(risk_score, 100)
    
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
            # Use Plotly gauge if available
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score", 'font': {'size': 24}},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 70], 'color': "gray"},
                        {'range': [70, 100], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Use fallback gauge
            st.markdown(create_simple_gauge(risk_score), unsafe_allow_html=True)
        
        st.markdown(f"**AI Decision:** {decision}")
        
        # Detailed reasoning
        st.markdown("#### 🔍 Detection Logic")
        if risk_score < 50:
            st.success("""
            **Normal Transaction Pattern:**
            - Amount within expected range
            - Location matches user history
            - No behavioral anomalies detected
            - Telco verification: PASSED
            """)
        elif risk_score < 85:
            st.warning("""
            **Suspicious Pattern Detected:**
            - Circuit breaker activated
            - Video liveness check required
            - Secondary authentication needed
            - Transaction held for review
            """)
        else:
            st.error("""
            **Critical Threat Identified:**
            - SIM swap confirmed via telco API
            - Account immediately frozen
            - Law enforcement notified
            - Chain analysis initiated
            """)

    # Transaction history
    st.divider()
    st.subheader("📋 Recent Transaction Monitoring")
    
    # Display recent transactions
    recent_tx = pd.DataFrame(st.session_state.financial_data[-10:])
    st.dataframe(recent_tx, use_container_width=True)

# --- 4. DURESS PROTOCOL ---
elif mode == "🚨 Duress Protocol (Citizen)":
    st.subheader("🆘 Autonomous Duress Response System")
    
    st.info("This system protects citizens during physical threats by enabling covert emergency signaling.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Banking App Simulation")
        st.markdown("You are being forced to withdraw money under duress.")
        
        # Enhanced PIN input with instructions
        st.markdown("**Normal PIN:** `1234` | **Duress PIN:** `9999`")
        pin_input = st.text_input("Enter PIN", type="password", max_chars=4, 
                                 placeholder="Enter 4-digit PIN")
        
        amount = st.slider("Withdrawal Amount (KES)", 1000, 500000, 50000)
        
        if st.button("Process Withdrawal", use_container_width=True):
            if pin_input == "1234":
                st.success("✅ Transaction Successful")
                st.info("KES {:,.0f} has been withdrawn.".format(amount))
            elif pin_input == "9999":
                # THE COVERT RESPONSE
                st.success("✅ Transaction Appears Successful") 
                st.balloons()
                
                # THE REAL AUTONOMOUS RESPONSE
                with col2:
                    st.markdown('<div class="alert-banner">🚨 SILENT DURESS SIGNAL DETECTED</div>', unsafe_allow_html=True)
                    
                    st.markdown("**Autonomous Emergency Protocol Activated:**")
                    
                    # Response steps
                    steps = st.container()
                    with steps:
                        col_step1, col_step2, col_step3, col_step4 = st.columns(4)
                        with col_step1:
                            st.metric("Step 1", "GPS Tracking", "ACTIVE")
                        with col_step2:
                            st.metric("Step 2", "Police Alert", "SENT")
                        with col_step3:
                            st.metric("Step 3", "Funds Frozen", "EXECUTED")
                        with col_step4:
                            st.metric("Step 4", "Evidence Log", "SECURED")
                    
                    st.code("""
// AUTONOMOUS ACTIONS EXECUTED
1. [GPS] Location: -1.2921, 36.8219 (Nairobi CBD)
2. [API] POST /nc4/alert (CODE_RED: Armed robbery)
3. [API] POST /mpesa/freeze?target=254712345678
4. [BLOCKCHAIN] Log #D-99182 created (Immutable)
5. [AUDIT] Full session recorded for investigation
6. [COMMS] Silent alert to DCI/Police dispatch
                    """, language="json")
                    
                    # Live tracking map
                    st.map(pd.DataFrame({'lat': [-1.2921], 'lon': [36.8219]}), zoom=15)
                    st.caption("📍 Real-time location tracking active - DCI Dispatch notified")
                    
                    # Evidence chain
                    st.markdown("#### 🔗 Digital Evidence Chain")
                    st.info("""
                    **Blockchain Verification:**
                    - Timestamp: {:%Y-%m-%d %H:%M:%S}
                    - Transaction ID: TX-{}-DURESS
                    - GPS Coordinates: -1.2921, 36.8219
                    - Police Case: #DCI-2024-99182
                    - Status: ACTIVE RESPONSE
                    """.format(datetime.now(), random.randint(10000, 99999)))
            else:
                st.warning("Incorrect PIN. Please try again.")

# --- 5. INTELLIGENCE CORE ---
elif mode == "🔍 Intelligence Core":
    st.subheader("🔍 Intelligence Core - Attribution & Threat Analysis")
    
    st.markdown("Advanced AI-powered attribution and threat intelligence analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌐 Chain Analysis Engine")
        
        # Simulated attack chain visualization
        attack_data = pd.DataFrame({
            'Stage': ['Initial Access', 'Lateral Movement', 'Data Exfiltration', 'Financial Transfer', 'Money Laundering'],
            'Time': ['14:30:02', '14:35:18', '14:41:45', '14:50:22', '15:15:10'],
            'Confidence': [85, 92, 78, 95, 88],
            'Status': ['Detected', 'Detected', 'Prevented', 'Tracked', 'Monitoring']
        })
        
        st.dataframe(attack_data, use_container_width=True)
        
        # Attribution analysis
        st.markdown("#### 🎯 Attribution Analysis")
        st.metric("Attribution Confidence", "94%", "High")
        st.metric("Threat Actor", "APT-41", "Known Group")
        st.metric("Infrastructure", "Residential Proxies", "Botnet")
        
    with col2:
        st.markdown("#### 📈 Threat Intelligence")
        
        # Threat timeline
        timeline_data = pd.DataFrame({
            'Event': ['SIM Swap Attempt', 'Mule Account Created', 'Lateral Movement', 'Data Exfiltration', 'Funds Transfer'],
            'Timestamp': ['14:30', '14:45', '15:00', '15:15', '15:30'],
            'Risk': ['High', 'Medium', 'High', 'Critical', 'High']
        })
        
        st.dataframe(timeline_data, use_container_width=True)
        
        # Graph network visualization placeholder
        st.markdown("#### 🕸️ Transaction Network Analysis")
        st.image("https://placehold.co/600x300/1a1a1a/FFFFFF?text=Graph+Neural+Network+Analysis%0AIdentifying+Money+Laundering+Patterns", 
                caption="GNN identifying funnel accounts across banking network")

# --- System Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("**Network Status:**")
st.sidebar.markdown("✅ **USSD Gateway (*334#)**: Connected")
st.sidebar.markdown("✅ **Mobile App API**: Connected")
st.sidebar.markdown("✅ **Internet Banking**: Connected")
st.sidebar.markdown("✅ **Telco Integration**: Active")
st.sidebar.markdown("✅ **Blockchain Audit**: Live")

st.sidebar.markdown("---")
st.sidebar.markdown("**Threat Intelligence:**")
st.sidebar.markdown("🟢 **NC4 Integration**: Active")
st.sidebar.markdown("🟢 **BS-SOC Feed**: Live")
st.sidebar.markdown("🟢 **International TI**: Connected")

# --- Main Footer ---
st.markdown("---")
st.markdown("© 2025 Ulinzi-AI | **National Cyber-Intelligence & Prevention Platform** | Protecting Kenya's Digital Sovereignty")
