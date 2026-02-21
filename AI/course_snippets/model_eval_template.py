def accuracy(y_true, y_pred):
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / max(1, len(y_true))


def confusion_binary(y_true, y_pred):
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 0 and p == 1:
            fp += 1
        elif t == 0 and p == 0:
            tn += 1
        elif t == 1 and p == 0:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def main():
    y_true = [1, 0, 1, 1, 0, 0, 1]
    y_pred = [1, 0, 0, 1, 0, 1, 1]
    print("accuracy=", round(accuracy(y_true, y_pred), 4))
    print("confusion=", confusion_binary(y_true, y_pred))


if __name__ == "__main__":
    main()
