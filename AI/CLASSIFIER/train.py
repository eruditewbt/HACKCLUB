from sklearn.naive_bayes import MultinomialNB, Perceptron
from sklearn.metrics import accuracy_score, classification_report
from data import X_train, X_test, y_train, y_test

model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
