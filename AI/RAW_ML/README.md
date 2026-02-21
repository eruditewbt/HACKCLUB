# RAW_ML

Pure-Python machine learning utilities with no third-party dependencies.

## Modules
- `metrics.py`: Confusion matrix, accuracy, precision/recall/F1, MSE/MAE/R2.
- `split.py`: Train/test split and k-fold indices.
- `linear_regression.py`: Batch GD linear regression.
- `logistic_regression.py`: Batch GD binary logistic regression.
- `naive_bayes.py`: Multinomial Naive Bayes for tokenized docs.
- `knn.py`: KNN classifier and regressor.
- `perceptron.py`: Binary perceptron.
- `preprocessing.py`: Min-max scale, standardize, L2 normalize, one-hot.

## Quick start
```python
from RAW_ML import LinearRegressionGD

X = [[1, 2], [2, 3], [3, 4]]
y = [3, 5, 7]

model = LinearRegressionGD(lr=0.1, epochs=500)
model.fit(X, y)
print(model.predict([[4, 5]]))
```

## Notes
- All models are minimal baselines intended for learning or quick prototyping.
- No automatic batching, regularization, or early stopping.
