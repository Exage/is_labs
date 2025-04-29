import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import json

for r in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4", "vader_lexicon"]:
    nltk.download(r, quiet=True)

def load_texts(p):
    with open(p, "r", encoding="cp1251") as f:
        return [l.strip() for l in f if l.strip()]

file_name = "Лермонтов.txt" # <== Менять файл тут!
file_folder = "data"
texts = load_texts(f"{file_folder}/{file_name}")

labels = ["Класс 1"] * (len(texts) // 2) + ["Класс 2"] * (len(texts) - len(texts) // 2)
df = pd.DataFrame({"text": texts, "label": labels})

le = LabelEncoder()
df["label_encoded"] = le.fit_transform(df["label"])

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label_encoded"], test_size=0.2, random_state=42)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("russian"))

def process_text(t):
    toks = word_tokenize(t, language="russian")
    lemmas = [lemmatizer.lemmatize(tok) for tok in toks]
    filtered = [tok for tok in toks if tok.lower() not in stop_words]
    return {"tokens": toks, "lemmas": lemmas, "filtered_tokens": filtered}

processed_data = [process_text(t) for t in texts]

with open("processed_data.json", "w", encoding="utf-8") as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)

tfidf = TfidfVectorizer(max_features=10)
X_tfidf = tfidf.fit_transform(df["text"]).toarray()
print("Ключевые слова:", tfidf.get_feature_names_out())

sia = SentimentIntensityAnalyzer()
df["sentiment"] = df["text"].apply(lambda x: sia.polarity_scores(x))
print("Тональность:", df[["text", "sentiment"]])

wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(texts))
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

bow = CountVectorizer(max_features=500)
X_train_bow = bow.fit_transform(X_train).toarray()
X_test_bow = bow.transform(X_test).toarray()

class LSTMClassifier(nn.Module):
    def __init__(self, inp, hid, layers, out):
        super().__init__()
        self.lstm = nn.LSTM(inp, hid, layers, batch_first=True)
        self.fc = nn.Linear(hid, out)
    def forward(self, x):
        o, _ = self.lstm(x)
        return self.fc(o[:, -1, :])

model = LSTMClassifier(X_train_bow.shape[1], 128, 2, len(le.classes_))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

X_train_t = torch.tensor(X_train_bow, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test_bow, dtype=torch.float32).unsqueeze(1)
y_train_t = torch.tensor(y_train.to_numpy(), dtype=torch.long)
y_test_t = torch.tensor(y_test.to_numpy(), dtype=torch.long)

for e in range(10):
    model.train()
    optimizer.zero_grad()
    out = model(X_train_t)
    loss = criterion(out, y_train_t)
    loss.backward()
    optimizer.step()
    print(f"Epoch {e+1}/10 Loss: {loss.item():.4f}")

model.eval()
with torch.no_grad():
    preds = model(X_test_t)
    pred_cls = torch.argmax(preds, axis=1)
    acc = accuracy_score(y_test, pred_cls.numpy())
    print(f"Accuracy: {acc:.2f}")
