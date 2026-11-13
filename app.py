
import streamlit as st
import pickle
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)

# Load Machine Learning Model
with open("sms_spam_model (1).pkl", "rb") as file:
    data = pickle.load(file)

model = data["model"]
vectorizer = data["vectorizer"]

# Session State
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

# Professional CSS
st.markdown("""
<style>
.stApp {
    background: #080f1e;
    color: white;
}

header {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: white !important;
}

.hero {
    background: linear-gradient(120deg,#101f3c,#123b60);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #1675b9;
    margin-bottom: 25px;
}

.hero h1 {
    color: #35c5ff !important;
}

.metric {
    background: #111d32;
    border: 1px solid #23466c;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
}

.metric h2 {
    color: #35c5ff !important;
}

.stTextArea textarea {
    background: #101d30;
    color: white;
    border: 1px solid #2684c7;
    border-radius: 12px;
}

.stButton button {
    background: linear-gradient(90deg,#0879d1,#00b5e2);
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

.stButton button:hover {
    border: 1px solid #40d5ff;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ CYBERSHIELD AI")
st.sidebar.caption("SMS SECURITY SYSTEM")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Detection History", "About Project"]
)

st.sidebar.markdown("---")
st.sidebar.success("AI Model Loaded")

# Dashboard
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🛡️ CYBERSHIELD AI</h1>
        <h3>Intelligent SMS Spam Detection System</h3>
        <p>Protect yourself from suspicious messages using Machine Learning.</p>
    </div>
    """, unsafe_allow_html=True)

    total = len(st.session_state.history)
    spam_count = sum(
        1 for x in st.session_state.history
        if x["result"] == "spam"
    )
    normal_count = total - spam_count

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<div class="metric"><h2>{total}</h2><p>Total Scanned</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<div class="metric"><h2 style="color:#ff4545">{spam_count}</h2><p>Spam Detected</p></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f'<div class="metric"><h2 style="color:#00e88a">{normal_count}</h2><p>Normal Messages</p></div>',
            unsafe_allow_html=True
        )

    st.markdown("### 📩 SMS Security Scanner")

    message = st.text_area(
        "Enter SMS Message",
        placeholder="Paste your SMS message here...",
        height=150
    )

    if st.button("🔍 SCAN MESSAGE"):

        if message.strip():

            vector = vectorizer.transform([message])
            prediction = model.predict(vector)[0]

            result = str(prediction).lower()

            st.session_state.result = result

            st.session_state.history.append({
                "message": message,
                "result": result
            })

        else:
            st.warning("Please enter a message.")

    # Result Display
    if st.session_state.result == "spam":

        st.markdown("""
        <div style="background:#35121a;border:2px solid #ff3333;
        padding:25px;border-radius:15px;text-align:center;">
        <h1 style="color:#ff3333 !important;">🚨 SPAM DETECTED</h1>
        <h3>DANGEROUS MESSAGE</h3>
        <p>Do not click suspicious links.</p>
        </div>
        """, unsafe_allow_html=True)

        components.html("""
        <style>
        @keyframes blink {
            0%,100% {opacity:1;box-shadow:0 0 30px red;}
            50% {opacity:.2;box-shadow:0 0 3px red;}
        }
        .light {
            width:35px;height:35px;border-radius:50%;
            background:red;margin:auto;
            animation:blink .6s infinite;
        }
        </style>
        <div class="light"></div>
        <p style="color:red;text-align:center;">RED ALERT</p>
        <button onclick="document.getElementById('alarm').play()">
        🔊 Play Alarm</button>
        <audio id="alarm" loop>
        <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg">
        </audio>
        """, height=130)

    elif st.session_state.result == "normal":

        st.markdown("""
        <div style="background:#103528;border:2px solid #00e88a;
        padding:25px;border-radius:15px;text-align:center;">
        <h1 style="color:#00e88a !important;">✅ NORMAL MESSAGE</h1>
        <h3>NO SPAM DETECTED</h3>
        </div>
        """, unsafe_allow_html=True)

        components.html("""
        <style>
        @keyframes glow {
            0%,100% {opacity:1;box-shadow:0 0 25px #00ff88;}
            50% {opacity:.4;box-shadow:0 0 5px #00ff88;}
        }
        .light {
            width:35px;height:35px;border-radius:50%;
            background:#00ff88;margin:auto;
            animation:glow 1.5s infinite;
        }
        </style>
        <div class="light"></div>
        <p style="color:green;text-align:center;">GREEN SAFE</p>
        """, height=90)

# History
elif page == "Detection History":

    st.title("📜 Detection History")

    if st.session_state.history:

        for i, item in enumerate(reversed(st.session_state.history), 1):
            if item["result"] == "spam":
                st.error(f"{i}. SPAM - {item['message']}")
            else:
                st.success(f"{i}. NORMAL - {item['message']}")

    else:
        st.info("No messages scanned yet.")

# About
elif page == "About Project":

    st.title("ℹ️ About CyberShield AI")

    st.write("""
    CyberShield AI is an SMS Spam Detection project
    developed using Python, Machine Learning and Streamlit.

    **Main Features:**
    - SMS Spam Classification
    - Red and Green Alert System
    - Detection History
    - Professional Security Dashboard

    **Technology Used:**
    - Python
    - Machine Learning
    - Streamlit
    - Scikit-learn
    """)

st.markdown("---")
st.caption("CYBERSHIELD AI | SMS SECURITY SYSTEM")
