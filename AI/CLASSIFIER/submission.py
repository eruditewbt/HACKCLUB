from collections import defaultdict

def learnPredictor(trainExamples, devExamples, featureExtractor, numIters=20, learningRate=1.0):
    """
    A simple perceptron learner.
    """
    weights = defaultdict(float)
    for iter in range(numIters):
        for x, y in trainExamples:
            features = featureExtractor(x)
            score = sum(weights[f] * v for f, v in features.items())
            prediction = 1 if score > 0 else -1
            if prediction != y:
                for f, v in features.items():
                    weights[f] += learningRate * y * v
    return dict(weights)