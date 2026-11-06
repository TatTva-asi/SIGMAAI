
import streamlit as st
import time

from main import get_response, chat_history


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SIGMA AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "request_count" not in st.session_state:
    st.session_state.request_count = 0


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main application */

.stApp {
    background:
        radial-gradient(ellipse at 50% 0%,
        rgba(0, 255, 120, 0.09), transparent 45%),
        #050807;
    color: #e5f5eb;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #080e0b;
    border-right: 1px solid rgba(0, 255, 120, 0.15);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Main container */

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main title */

.sigma-title {
    font-size: 54px;
    font-weight: 900;
    letter-spacing: 8px;
    text-align: center;
    color: #00ff88;
    text-shadow:
        0 0 10px rgba(0,255,136,0.6),
        0 0 30px rgba(0,255,136,0.3);
    animation: titleGlow 3s infinite alternate;
}

@keyframes titleGlow {
    from {
        text-shadow: 0 0 10px rgba(0,255,136,0.3);
    }
    to {
        text-shadow: 0 0 25px rgba(0,255,136,0.8);
    }
}

/* Subtitle */

.sigma-subtitle {
    text-align: center;
    color: #719985;
    font-size: 12px;
    letter-spacing: 4px;
    margin-top: -10px;
    margin-bottom: 35px;
}

/* Status badge */

.status-container {
    display: flex;
    justify-content: center;
    margin-bottom: 25px;
}

.status-badge {
    border: 1px solid #00ff8850;
    background: #00ff8810;
    padding: 7px 18px;
    border-radius: 30px;
    color: #00ff88;
    font-size: 11px;
    letter-spacing: 2px;
}

.status-dot {
    display: inline-block;
    height: 7px;
    width: 7px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px #00ff88;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Chat messages */

[data-testid="stChatMessage"] {
    background: rgba(12, 22, 16, 0.85);
    border: 1px solid rgba(0, 255, 120, 0.12);
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 15px;
    animation: messageAppear 0.35s ease-out;
}

@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Chat message text */

[data-testid="stChatMessage"] p {
    color: #d9e9df;
    line-height: 1.7;
    font-size: 15px;
}

/* Chat input */

[data-testid="stChatInput"] {
    border: 1px solid #00ff8840 !important;
    border-radius: 15px !important;
    background: #0a110d !important;
    box-shadow: 0 0 20px rgba(0,255,136,0.05);
}

[data-testid="stChatInput"]:focus-within {
    border: 1px solid #00ff88 !important;
    box-shadow: 0 0 20px rgba(0,255,136,0.15);
}

/* Buttons */

.stButton > button {
    background: #0b1c12;
    color: #00ff88;
    border: 1px solid #00ff8850;
    border-radius: 10px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #00ff88;
    color: #001b0d;
    border-color: #00ff88;
    box-shadow: 0 0 18px rgba(0,255,136,0.35);
    transform: translateY(-2px);
}

/* Sidebar headings */

.sidebar-heading {
    color: #00ff88;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* Info cards */

.info-card {
    background: #0b1510;
    border: 1px solid #00ff8825;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.info-label {
    color: #719985;
    font-size: 10px;
    letter-spacing: 2px;
}

.info-value {
    color: #00ff88;
    font-size: 18px;
    font-weight: bold;
    margin-top: 5px;
}

/* Welcome screen */

.welcome-card {
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(0,255,136,0.06),
        rgba(0,0,0,0.2)
    );
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 20px;
    padding: 45px 20px;
    margin-top: 30px;
}

.welcome-icon {
    font-size: 45px;
    filter: drop-shadow(0 0 15px #00ff88);
}

.welcome-heading {
    color: #00ff88;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 15px;
}

.welcome-text {
    color: #789787;
    font-size: 14px;
    line-height: 2;
}

/* Footer */

.footer {
    text-align: center;
    color: #466353;
    font-size: 11px;
    letter-spacing: 3px;
    margin-top: 45px;
}

/* Scrollbar */

::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-thumb {
    background: #00ff8850;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:10px 0 30px;">
        <div style="font-size:45px;">⚡</div>
        <div style="
            color:#00ff88;
            font-size:25px;
            font-weight:900;
            letter-spacing:5px;">
            SIGMA
        </div>
        <div style="
            color:#658775;
            font-size:10px;
            letter-spacing:3px;">
            AI INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-heading">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-label">CONNECTION</div>
        <div class="info-value">● ONLINE</div>
    </div>
    <div class="info-card">
        <div class="info-label">PERSONALITY</div>
        <div class="info-value">SAVAGE MODE</div>
    </div>
    <div class="info-card">
        <div class="info-label">ENGINE</div>
        <div class="info-value">LANGCHAIN + GROQ</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">SESSION STATISTICS</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Messages sent",
        st.session_state.request_count
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">CONTROLS</div>',
        unsafe_allow_html=True
    )

    if st.button("CLEAR CONVERSATION", use_container_width=True):

        st.session_state.messages = []
        st.session_state.request_count = 0
        chat_history.clear()

        st.rerun()

    st.markdown("""
    <div style="
        position:relative;
        margin-top:50px;
        text-align:center;
        color:#466353;
        font-size:10px;
        letter-spacing:2px;">
        NO SUGARCOATING.<br>
        NO FAKE MOTIVATION.<br>
        ONLY REALITY.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown("""
<div class="sigma-title">SIGMA</div>

<div class="sigma-subtitle">
    BRUTAL HONESTY // ZERO SUGARCOATING
</div>

<div class="status-container">
    <div class="status-badge">
        <span class="status-dot"></span>
        SYSTEM OPERATIONAL
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# WELCOME SCREEN
# ==========================================

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-card">

        <div class="welcome-icon">⚡</div>

        <div class="welcome-heading">
            REALITY DOESN'T CARE ABOUT YOUR FEELINGS.
        </div>

        <div class="welcome-text">
            Welcome to SIGMA AI.<br>
            Ask anything. Expect honesty.<br>
            Your ego is not our responsibility.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;color:#719985;"
        "font-size:12px;margin-top:25px;'>"
        "START A CONVERSATION BELOW"
        "</p>",
        unsafe_allow_html=True
    )


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT AND RESPONSE
# ==========================================

user_input = st.chat_input(
    "Say something. SIGMA is listening..."
)

if user_input:

    # Display user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("SIGMA is preparing a comeback..."):

            try:

                answer = get_response(user_input)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.session_state.request_count += 1

            except Exception as e:

                st.error(f"SIGMA ERROR: {str(e)}")

    st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    POWERED BY LANGCHAIN + GROQ
    <br><br>
    SIGMA AI © 2026
</div>
""", unsafe_allow_html=True)
