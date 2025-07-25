from data import vectorizer
from AI.CLASSIFIER.train import model

def predict_sentiment(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

print(predict_sentiment("This movie was not bad, I liked it."))  # Should return 'positive'
print(predict_sentiment("It was a horrible experience."))       # Should return 'negative'
