import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

data = {
    'review': [
        "I loved the movie, it was fantastic!",
        "Absolutely terrible film, I hated it.",
        "It was a good movie, really enjoyed it.",
        "Worst experience ever. So boring.",
        "Not bad at all, pretty good.",
        "Awful. Don't waste your time.",
    ],
    'sentiment': ['positive', 'negative', 'positive', 'negative', 'positive', 'negative']
}

df = pd.DataFrame(data)

X = df['review']
y = df['sentiment']

# Convert text to word count vectors
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.33, random_state=42)