
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
