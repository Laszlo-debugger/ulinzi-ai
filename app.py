import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Ulinzi-AI: National Cyber-Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    .log-container {
        background-color: #0e1117;
        color: #00ff00;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown('<div class="main-header">🛡️ Ulinzi-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">National Autonomous Cyber-Physical Intelligence System</div>', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("🕹️ Command Center Controls")
st.sidebar.info("Select a threat scenario to activate the Autonomous Agent.")

scenario = st.sidebar.radio(
    "Active Threat Scenarios:",
    (
        "--- Select Scenario ---",
        "Scenario 1: The '3 AM' Anomaly (Financial Sentinel)",
        "Scenario 2: The Duress Protocol (Physical Threat)",
        "Scenario 3: Sovereign Defacement (Visual Sentinel)"
    )
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:** 🟢 ONLINE")
st.sidebar.markdown("**Connected Nodes:**")
st.sidebar.markdown("- 🏦 KCB Core Banking")
st.sidebar.markdown("- 🏦 Equity Core Banking")
st.sidebar.markdown("- 📡 Safaricom Telco API")
st.sidebar.markdown("- 🏛️ Ministry of Interior Web")

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔴 Live Intelligence Log")
    log_placeholder = st.empty()
    
    # Default Empty State
    if scenario == "--- Select Scenario ---":
        log_placeholder.info("Waiting for event trigger...")

with col2:
    st.subheader("🤖 Autonomous Agent Status")
    agent_status = st.empty()
    agent_status.info("Status: IDLE (Monitoring)")
    
    st.subheader("⚡ Action Impact")
    impact_status = st.empty()
    impact_status.warning("No actions taken yet.")

# --- Simulation Logic ---

# SCENARIO 1: FINANCIAL FRAUD
if scenario == "Scenario 1: The '3 AM' Anomaly (Financial Sentinel)":
    
    log_text = ">> [03:01:10] MONITORING TRANSACTION STREAM...\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(1)
    
    # Step 1: Event Detection
    agent_status.info("Status: ANALYZING ANOMALY...")
    log_text += ">> [03:01:12] EVENT DETECTED: High-Value Withdrawal\n"
    log_text += "   - User ID:   KE-88291 (Jane Doe)\n"
    log_text += "   - Amount:    KES 850,000.00\n"
    log_text += "   - Time:      03:01 AM (High Risk)\n"
    log_text += "   - Location:  Naivasha (Geo-Anomaly)\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(2)

    # Step 2: AI Analysis
    log_text += "\n>> [03:01:13] AI RISK ASSESSMENT (Isolation Forest):\n"
    log_text += "   - ⚠️ Velocity Alert: 150x deviation from 30-day avg.\n"
    log_text += "   - ⚠️ Telco Signal: SIM Swap detected 4 hours ago.\n"
    log_text += "   - 🔴 RISK SCORE: 98/100 (CRITICAL FRAUD)\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(2)

    # Step 3: Autonomous Action
    agent_status.error("Status: ENGAGING CIRCUIT BREAKER")
    log_text += "\n>> [03:01:14] AUTONOMOUS ACTION TRIGGERED:\n"
    log_text += "   - 🚫 ACTION: Transaction BLOCKED immediately.\n"
    log_text += "   - 🔒 ACTION: Account 'KE-88291' Frozen.\n"
    log_text += "   - 📹 ACTION: Video Liveness Check challenge sent to App.\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(1)

    # Final Impact
    impact_status.success("💸 FRAUD PREVENTED: KES 850,000 SAVED")
    st.toast("Threat Neutralized: Financial Anomaly Detected")


# SCENARIO 2: DURESS PROTOCOL
elif scenario == "Scenario 2: The Duress Protocol (Physical Threat)":
    
    log_text = ">> [14:15:22] MONITORING USER SESSIONS...\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(1)

    # Step 1: Duress PIN Entry
    agent_status.info("Status: PROCESSING AUTHENTICATION...")
    log_text += ">> [14:15:25] AUTH EVENT: User Login\n"
    log_text += "   - User ID:   KE-44510 (John Kamau)\n"
    log_text += "   - Input:     PIN ENTRY ****\n"
    log_text += "   - Analysis:  MATCHES 'DURESS PIN' HASH.\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(2)

    # Step 2: The "Trick" & AI Response
    agent_status.warning("Status: EXECUTING DURESS PROTOCOL")
    log_text += "\n>> [14:15:26] DURESS PROTOCOL ACTIVATED:\n"
    log_text += "   - ✅ FRONTEND: Display 'Transaction Successful' (Deception).\n"
    log_text += "   - 🚓 BACKEND: Dispatch 'CODE RED' to NPS (Police).\n"
    log_text += "     -> GPS Lat/Long: -1.2921, 36.8219 (Hurlingham)\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(2)

    # Step 3: The Money Marker
    log_text += "\n>> [14:15:27] CHAIN ANALYSIS AGENT:\n"
    log_text += "   - Target:    M-PESA 0722-XXX-XXX (The Kidnapper)\n"
    log_text += "   - Action:    API Call -> POST /mpesa/freeze_account\n"
    log_text += "   - Result:    TARGET ACCOUNT FROZEN (Funds Trapped).\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(1)

    # Final Impact
    impact_status.success("👮 POLICE ALERTED. FUNDS TRAPPED. USER SAFE.")
    st.toast("Emergency Protocol Executed")


# SCENARIO 3: VISUAL SENTINEL
elif scenario == "Scenario 3: Sovereign Defacement (Visual Sentinel)":
    
    log_text = ">> [09:45:00] VISUAL SENTINEL: MONITORING 'statehouse.go.ke'...\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(1)

    # Step 1: The Attack
    agent_status.info("Status: SCANNING VISUAL STATE...")
    
    # Displaying the "Attack" visually
    with col1:
        st.image("https://placehold.co/600x150/red/white?text=HACKED:+MINISTRY+WEBSITE+DEFACED", caption="Simulated Live View: 09:45:05 AM")

    log_text += ">> [09:45:05] ALERT: VISUAL INTEGRITY COMPROMISED!\n"
    log_text += "   - Diff Score: 15.4% (Threshold: 5%)\n"
    log_text += "   - Anomaly:    Foreign content/Hate symbols detected.\n"
    log_placeholder.code(log_text, language="bash")
    time.sleep(3)

    # Step 2: Autonomous Revert
    agent_status.error("Status: AUTONOMOUS REVERT INITIATED")
    log_text += "\n>> [09:45:05.500] AGENT ACTION: HOT-SWAP RESTORE\n"
    log_text += "   - Command:    kubectl rollout undo deployment/web-frontend\n"
    log_text += "   - Latency:    450ms response time.\n"
    log_text += "   - Evidence:   Snapshot stored to Blockchain Ledger.\n"
    log_placeholder.code(log_text, language="bash")
    
    # Displaying the "Fix" visually
    with col1:
        st.image("https://placehold.co/600x150/green/white?text=SECURE:+OFFICIAL+GOVERNMENT+PORTAL", caption="Restored Live View: 09:45:06 AM")
    
    time.sleep(1)

    # Final Impact
    impact_status.success("🛡️ SOVEREIGNTY RESTORED IN <1 SECOND.")
    st.toast("Sovereign Defense: Attack Neutralized")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Ulinzi-AI | Powered by Agentic AI & Zero-Trust Architecture")
