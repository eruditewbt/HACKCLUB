DEFAULT_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
    "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were",
    "will", "with", "i", "you", "your", "we", "they", "them", "this", "these",
    "those", "or", "not", "but", "if", "then", "else", "so", "than", "too",
    "very", "can", "could", "should", "would", "about", "into", "over", "after",
    "before", "between", "because", "why", "what", "which", "who", "whom",
}


def remove_stopwords(tokens, stopwords=None):
    """Remove stopwords from a list of tokens."""
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS
    return [t for t in tokens if t.lower() not in stopwords]
