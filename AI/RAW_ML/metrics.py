def confusion_matrix(y_true, y_pred, labels=None):
    """Compute confusion matrix for multiclass labels."""
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    index = {label: i for i, label in enumerate(labels)}
    size = len(labels)
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for yt, yp in zip(y_true, y_pred):
        matrix[index[yt]][index[yp]] += 1
    return matrix, labels


def accuracy(y_true, y_pred):
    """Compute accuracy score."""
    if not y_true:
        return 0.0
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    return correct / len(y_true)


def precision_recall_f1(y_true, y_pred, labels=None):
    """Compute macro-averaged precision, recall, and F1."""
    cm, labels = confusion_matrix(y_true, y_pred, labels=labels)
    n = len(labels)
    precisions = []
    recalls = []
    f1s = []
    for i in range(n):
        tp = cm[i][i]
        fp = sum(cm[r][i] for r in range(n) if r != i)
        fn = sum(cm[i][c] for c in range(n) if c != i)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    return {
        "precision": sum(precisions) / n if n else 0.0,
        "recall": sum(recalls) / n if n else 0.0,
        "f1": sum(f1s) / n if n else 0.0,
    }


def mse(y_true, y_pred):
    if not y_true:
        return 0.0
    return sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)


def mae(y_true, y_pred):
    if not y_true:
        return 0.0
    return sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / len(y_true)


def r2_score(y_true, y_pred):
    if not y_true:
        return 0.0
    mean_y = sum(y_true) / len(y_true)
    ss_tot = sum((yt - mean_y) ** 2 for yt in y_true)
    ss_res = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred))
    return 1.0 - (ss_res / ss_tot if ss_tot else 0.0)
