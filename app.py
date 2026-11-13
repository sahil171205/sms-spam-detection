import streamlit as st
import pickle

st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩"
)

# Load Machine Learning Model
with open("sms_spam_model (1).pkl", "rb") as file:
    data = pickle.load(file)

model = data["model"]
vectorizer = data["vectorizer"]

# Website Title
st.title("📩 SMS Spam Detection")
st.write("Check whether your SMS is Spam or Normal.")

# SMS Input
message = st.text_area("Enter your SMS here:")

if st.button("Check SMS"):
    if message.strip():
        message_vector = vectorizer.transform([message])
        prediction = model.predict(message_vector)[0]

        if prediction == "spam":
            st.error("⚠️ This is a SPAM Message!")
        else:
            st.success("✅ This is a NORMAL Message!")
    else:
        st.warning("Please enter an SMS first.")
