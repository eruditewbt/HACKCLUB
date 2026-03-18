from __future__ import annotations

from .error_analysis import Example, false_negatives, false_positives
from .metrics import precision_recall_f1


def main():
    examples = [
        Example("cheap meds online", 1, 1),
        Example("hello how are you", 0, 1),
        Example("limited time offer", 1, 0),
        Example("meeting at 3pm", 0, 0),
    ]
    y_true = [e.y_true for e in examples]
    y_pred = [e.y_pred for e in examples]
    m = precision_recall_f1(y_true, y_pred)
    print("Metrics:", m)
    print("\nFalse positives:")
    for e in false_positives(examples):
        print("-", e.text)
    print("\nFalse negatives:")
    for e in false_negatives(examples):
        print("-", e.text)


if __name__ == "__main__":
    main()

