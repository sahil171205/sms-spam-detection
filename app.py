
import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩",
    layout="wide"
)

# Dark Dashboard Design
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
textarea {
    background-color: #1e293b !important;
    color: white !important;
}
.result-spam {
    background-color: #7f1d1d;
    border: 2px solid #ef4444;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.result-normal {
    background-color: #14532d;
    border: 2px solid #22c55e;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# Train Machine Learning Model
@st.cache_resource
def train_model():

    data = pd.read_csv("spam.csv", encoding="latin-1")

    # Kaggle Dataset columns
    if "v1" in data.columns and "v2" in data.columns:
        labels = data["v1"]
        messages = data["v2"]
    else:
        labels = data.iloc[:, 0]
        messages = data.iloc[:, 1]

    df = pd.DataFrame({
        "label": labels,
        "message": messages
    })

    df = df.dropna()
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["message"] = df["message"].astype(str)

    df = df[df["label"].isin(["ham", "spam"])]

    if df["label"].nunique() < 2:
        raise ValueError("Dataset must contain both ham and spam messages.")

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000
        )),
        ("classifier", MultinomialNB())
    ])

    model.fit(df["message"], df["label"])

    return model, len(df)


# Header
st.title("📩 SMS SPAM DETECTION")
st.caption("AI & Machine Learning Based SMS Security System")

st.divider()

# Load Model
try:
    model, total_sms = train_model()

    st.success(f"Machine Learning Model Ready | Dataset: {total_sms} SMS")

except Exception as e:
    st.error(f"Dataset Error: {e}")
    st.info("Please keep spam.csv in the same folder as app.py.")
    st.stop()


# Dashboard
col1, col2 = st.columns(2)

with col1:
    st.metric("Dataset Messages", total_sms)

with col2:
    st.metric("Detection System", "Active")

st.divider()

st.subheader("🔍 Check Your SMS")

sms = st.text_area(
    "Enter SMS Message:",
    placeholder="Example: Congratulations! You won a lottery prize...",
    height=130
)

# Common scam phrases
spam_patterns = [
    r"\bwon\s+(a\s+)?lottery\b",
    r"\blottery\b",
    r"\bclaim\s+(your\s+)?prize\b",
    r"\byou\s+have\s+won\b",
    r"\bselected\s+as\s+a\s+winner\b",
    r"\bcash\s+prize\b",
    r"\bfree\s+entry\b",
    r"\bclick\s+here\s+to\s+claim\b"
]


if st.button("🔍 DETECT SMS", use_container_width=True):

    if not sms.strip():
        st.warning("Please enter an SMS first.")

    else:
        message = sms.strip()

        # ML Prediction
        prediction = model.predict([message])[0]
        probabilities = model.predict_proba([message])[0]

        spam_index = list(model.classes_).index("spam")
        spam_probability = probabilities[spam_index] * 100

        # Additional scam phrase check
        suspicious = any(
            re.search(pattern, message, re.IGNORECASE)
            for pattern in spam_patterns
        )

        if prediction == "spam" or suspicious:

            st.markdown("""
            <div class="result-spam">
                <h1>🔴 SPAM DETECTED</h1>
                <h3>Warning! Suspicious SMS Message</h3>
                <p>Do not click unknown links or share OTP.</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(1.0)
            st.write(f"Model Spam Probability: {spam_probability:.2f}%")

        else:

            st.markdown("""
            <div class="result-normal">
                <h1>🟢 NORMAL MESSAGE</h1>
                <h3>Message classified as Normal</h3>
            </div>
            """, unsafe_allow_html=True)

            st.progress(float(spam_probability / 100))
            st.write(f"Model Spam Probability: {spam_probability:.2f}%")

st.divider()

st.caption("SMS Spam Detection | Python | Streamlit | Machine Learning")
