import json

def readExamples(filename):
    """Reads examples from a file. Each line should be: label \t text"""
    examples = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                label, text = parts
                examples.append((text, int(label)))
    return examples

def outputWeights(weights, filename):
    """Writes weights to a file in JSON format."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(weights, f, indent=2)

def outputErrorAnalysis(examples, featureExtractor, weights, filename):
    """Writes error analysis to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for x, y in examples:
            features = featureExtractor(x)
            score = dotProduct(features, weights)
            f.write(f"{x}\tTrue: {y}\tPred: {1 if score > 0 else -1}\tScore: {score}\n")

def dotProduct(d1, d2):
    """Computes the dot product of two feature dictionaries."""
    return sum(d1.get(f, 0) * d2.get(f, 0) for f in d1)

def evaluatePredictor(examples, predictor):
    """Evaluates the predictor on the examples and returns the error rate."""
    error = 0
    for x, y in examples:
        pred = predictor(x)
        if pred != y:
            error += 1
    return error / len(examples) if examples else 0