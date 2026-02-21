import random


def train_test_split(data, labels, test_size=0.2, shuffle=True, seed=None):
    """Split data and labels into train/test subsets."""
    if len(data) != len(labels):
        raise ValueError("data and labels must be the same length")
    n = len(data)
    indices = list(range(n))
    if shuffle:
        rnd = random.Random(seed)
        rnd.shuffle(indices)
    split = int(n * (1.0 - test_size))
    train_idx = indices[:split]
    test_idx = indices[split:]
    X_train = [data[i] for i in train_idx]
    y_train = [labels[i] for i in train_idx]
    X_test = [data[i] for i in test_idx]
    y_test = [labels[i] for i in test_idx]
    return X_train, X_test, y_train, y_test


def k_fold_indices(n, k, shuffle=True, seed=None):
    """Generate k-fold train/test index splits."""
    indices = list(range(n))
    if shuffle:
        rnd = random.Random(seed)
        rnd.shuffle(indices)
    folds = [indices[i::k] for i in range(k)]
    splits = []
    for i in range(k):
        test_idx = folds[i]
        train_idx = [idx for j, fold in enumerate(folds) if j != i for idx in fold]
        splits.append((train_idx, test_idx))
    return splits
