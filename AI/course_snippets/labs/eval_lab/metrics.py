from __future__ import annotations

from typing import Dict, List, Tuple


def confusion_counts(y_true: List[int], y_pred: List[int]) -> Dict[str, int]:
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn}


def precision_recall_f1(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    c = confusion_counts(y_true, y_pred)
    tp, fp, fn = c["tp"], c["fp"], c["fn"]
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


