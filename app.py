
import streamlit as st
import streamlit.components.v1 as components
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #07111f;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton > button {
    background: #0878d1;
    color: white;
    border-radius: 10px;
    border: 1px solid #00aaff;
    padding: 10px 20px;
    font-weight: bold;
}
.stButton > button:hover {
    background: #00aaff;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #101d30;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    with open("sms_spam_model (1).pkl", "rb") as file:
        data = pickle.load(file)

    return data["model"], data["vectorizer"]

try:
    model, vectorizer = load_model()
except Exception as e:
    st.error("Model file load failed. Check your pickle file name.")
    st.code(str(e))
    st.stop()

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "message" not in st.session_state:
    st.session_state.message = ""

if "scan_id" not in st.session_state:
    st.session_state.scan_id = 0

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛡️ CYBER SECURITY")
st.sidebar.caption("AI SMS Protection System")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Detection History", "About Project"]
)

st.sidebar.markdown("---")
st.sidebar.success("AI Model: ONLINE")
st.sidebar.info("System Status: ACTIVE")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("📩 SMS SPAM DETECTION")
    st.write("AI Based Cyber Security Monitoring Dashboard")

    total = len(st.session_state.history)
    spam_count = sum(
        1 for x in st.session_state.history
        if x["result"] == "spam"
    )
    normal_count = sum(
        1 for x in st.session_state.history
        if x["result"] == "normal"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", total)
    c2.metric("Spam Messages", spam_count)
    c3.metric("Normal Messages", normal_count)

    st.markdown("---")
    st.subheader("🔍 SMS Security Scanner")

    message = st.text_area(
        "Enter your SMS:",
        value=st.session_state.message,
        height=130,
        placeholder="Enter or paste your SMS here..."
    )

    if st.button("🚀 SCAN MESSAGE"):

        if message.strip():

            msg_vector = vectorizer.transform([message])
            prediction = str(
                model.predict(msg_vector)[0]
            ).lower().strip()

            if prediction in ["spam", "1"]:
                result = "spam"
            elif prediction in ["ham", "normal", "not spam", "0"]:
                result = "normal"
            else:
                result = "unknown"

            st.session_state.result = result
            st.session_state.message = message
            st.session_state.scan_id += 1

            st.session_state.history.insert(0, {
                "message": message,
                "result": result
            })

        else:
            st.warning("Please enter an SMS first.")

    # ---------------- SPAM RESULT ----------------
    if st.session_state.result == "spam":

        st.markdown("""
        <div style="
            background:#421414;
            border:2px solid #ff3030;
            padding:25px;
            border-radius:15px;
            text-align:center;
        ">
            <h1 style="color:#ff3030 !important;">
                ⚠️ SPAM MESSAGE DETECTED
            </h1>
            <h3 style="color:white !important;">
                DANGEROUS MESSAGE - BE CAREFUL
            </h3>
            <div style="
                width:35px;
                height:35px;
                border-radius:50%;
                background:#ff2020;
                margin:20px auto;
                box-shadow:0 0 30px red;
                animation:redblink 1s infinite;
            "></div>
            <h3 style="color:#ff3030 !important;">
                🔴 RED ALERT
            </h3>
        </div>
        <style>
        @keyframes redblink {
            0%,100% {opacity:1; box-shadow:0 0 30px red;}
            50% {opacity:0.2; box-shadow:0 0 5px red;}
        }
        </style>
        """, unsafe_allow_html=True)

        st.error("⚠️ Warning: This SMS may be fraudulent.")

        # Audio alert - browser autoplay may be blocked
        components.html("""
        <audio autoplay>
            <source
            src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
            type="audio/ogg">
        </audio>
        """, height=20)

        # Manual fallback
        if st.button("🔊 PLAY ALARM"):
            components.html("""
            <audio autoplay>
                <source
                src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
                type="audio/ogg">
            </audio>
            """, height=50)

    # ---------------- NORMAL RESULT ----------------
    elif st.session_state.result == "normal":

        st.markdown("""
        <div style="
            background:#103528;
            border:2px solid #00ff88;
            padding:25px;
            border-radius:15px;
            text-align:center;
        ">
            <h1 style="color:#00ff88 !important;">
                ✅ NORMAL MESSAGE
            </h1>
            <h3 style="color:white !important;">
                NO SPAM DETECTED
            </h3>
            <div style="
                width:35px;
                height:35px;
                border-radius:50%;
                background:#00ff88;
                margin:20px auto;
                box-shadow:0 0 30px #00ff88;
                animation:greenblink 1s infinite;
            "></div>
            <h3 style="color:#00ff88 !important;">
                🟢 GREEN SAFE
            </h3>
        </div>

        <style>
        @keyframes greenblink {
            0%,100% {opacity:1; box-shadow:0 0 30px #00ff88;}
            50% {opacity:0.25; box-shadow:0 0 5px #00ff88;}
        }
        </style>
        """, unsafe_allow_html=True)

        st.success("✅ This message is classified as NORMAL.")

    elif st.session_state.result == "unknown":
        st.warning("Unknown prediction label. Please check model classes.")

# ---------------- DETECTION HISTORY ----------------
elif page == "Detection History":

    st.title("📋 DETECTION HISTORY")

    if st.session_state.history:

        for i, item in enumerate(
            st.session_state.history, start=1
        ):
            st.markdown(f"**Scan {i}:** {item['message']}")

            if item["result"] == "spam":
                st.error("🔴 SPAM MESSAGE")
            elif item["result"] == "normal":
                st.success("🟢 NORMAL MESSAGE")
            else:
                st.warning("UNKNOWN")

            st.markdown("---")

        if st.button("🗑️ CLEAR HISTORY"):
            st.session_state.history = []
            st.session_state.result = None
            st.session_state.message = ""
            st.rerun()

    else:
        st.info("No detection history available.")

# ---------------- ABOUT PROJECT ----------------
elif page == "About Project":

    st.title("ℹ️ ABOUT PROJECT")

    st.markdown("""
    ### SMS Spam Detection System

    This project uses Machine Learning to identify
    spam and normal SMS messages.

    **Technologies Used:**
    - Python
    - Streamlit
    - Machine Learning
    - Scikit-learn
    - Pickle

    **Features:**
    - SMS Spam Detection
    - Normal Message Detection
    - Red Alert Indicator
    - Green Safe Indicator
    - Alarm Sound
    - Detection History

    **Project Objective:**

    To identify suspicious SMS messages and
    improve digital security.
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🛡️ SMS Spam Detection | AI Cyber Security Project")

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load original dataset
df = pd.read_csv("spam.csv", encoding="latin-1")

# Select dataset columns
if "v1" in df.columns and "v2" in df.columns:
    df = df[["v1", "v2"]]
    df.columns = ["label", "message"]
else:
    df = df.iloc[:, :2]
    df.columns = ["label", "message"]

# Clean dataset
df = df.dropna()
df["label"] = df["label"].astype(str).str.lower().str.strip()
df["message"] = df["message"].astype(str)

df = df[df["label"].isin(["spam", "ham"])]

# Additional SMS training examples
extra_data = [
    ("spam", "Hi you won lottery"),
    ("spam", "Congratulations you have won a lottery prize"),
    ("spam", "You won 1000000 rupees claim now"),
    ("spam", "Claim your free cash prize now"),
    ("spam", "You are selected as a lucky winner"),
    ("spam", "Click here to claim your reward"),
    ("spam", "Urgent! You have won a free gift"),
    ("spam", "Congratulations your number won a jackpot"),
    ("spam", "You have won a cash prize"),
    ("spam", "Free entry in a weekly lottery"),
    ("ham", "Hi how are you"),
    ("ham", "I will call you later"),
    ("ham", "Where are you now"),
    ("ham", "Meet me tomorrow"),
    ("ham", "Thank you for your help"),
    ("ham", "Are you coming to college today"),
    ("ham", "Good morning have a nice day"),
    ("ham", "I am waiting for you"),
    ("ham", "Please send me the notes"),
        ("spam", "You won lottery"),
    ("spam", "You won a lottery"),
    ("spam", "You have won lottery"),
    ("spam", "Congratulations you won lottery"),
    ("spam", "You are a lottery winner"),
    ("spam", "You won 1000000 rupees"),
    ("spam", "Claim your lottery prize now"),
    ("spam", "Your lottery prize is waiting"),
    ("ham", "See you soon")
]

extra_df = pd.DataFrame(
    extra_data,
    columns=["label", "message"]
)

df = pd.concat([df, extra_df], ignore_index=True)

# Train model
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    stop_words="english"
)

X = vectorizer.fit_transform(df["message"])
y = df["label"]

model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
data = {
    "model": model,
    "vectorizer": vectorizer
}

with open("sms_spam_model (1).pkl", "wb") as file:
    pickle.dump(data, file)

print("Model trained successfully!")
print("Total SMS:", len(df))
print("Model saved successfully!")
