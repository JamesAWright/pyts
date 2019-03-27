"""
===========================================
Bag-of-SFA Symbols in Vector Space (BOSSVS)
===========================================

This example shows how the BOSSVS algorithm transforms a dataset
consisting of time series and their corresponding labels into a
document-term matrix using tf-idf statistics. Each class is represented
as a tfidf vector. For an unlabeled time series, the predicted label is
the label of the tfidf vector giving the highest cosine similarity with
the tf vector of the unlabeled time series. BOSSVS algorithm is
implemented as :class:`pyts.classification.BOSSVS`.
"""

import numpy as np
import matplotlib.pyplot as plt
from pyts.classification import BOSSVS

# Parameters
n_samples, n_timestamps = 100, 144
n_classes = 2

# Toy dataset
rng = np.random.RandomState(41)
X = rng.randn(n_samples, n_timestamps)
y = rng.randint(n_classes, size=n_samples)
X[y == 0] = np.cumsum(X[y == 0], axis=1)

# BOSSVS transformation
bossvs = BOSSVS(word_size=2, n_bins=3, window_size=10)
bossvs.fit(X, y)
tfidf = bossvs.tfidf_
vocabulary_length = len(bossvs.vocabulary_)
X_new = bossvs.decision_function(X)

# Visualize the transformation
plt.figure(figsize=(16, 5))
width = 0.4

plt.subplot(121)
plt.bar(np.arange(vocabulary_length) - width / 2, tfidf[0],
        width=width, label='Class 0')
plt.bar(np.arange(vocabulary_length) + width / 2, tfidf[1],
        width=width, label='Class 1')
plt.xticks(np.arange(vocabulary_length),
           np.vectorize(bossvs.vocabulary_.get)(np.arange(vocabulary_length)),
           fontsize=14)
plt.xlabel("Words", fontsize=14)
plt.ylabel("tf-idf", fontsize=14)
plt.title("tf-idf vector for each class", fontsize=18)
plt.legend(loc='best')

plt.subplot(122)
n_samples_plot = 8
plt.bar(np.arange(n_samples_plot) - width / 2, X_new[:n_samples_plot, 0],
        width=width, label='Class 0')
plt.bar(np.arange(n_samples_plot) + width / 2, X_new[:n_samples_plot, 1],
        width=width, label='Class 1')
plt.xticks(np.arange(n_samples_plot), np.arange(1, n_samples_plot + 1),
           fontsize=14)
plt.xlabel("Samples", fontsize=14)
plt.ylabel("Cosine similarity", fontsize=14)
plt.title(("Cosine similarity between tf-idf vectors for each class\n"
           "and tf vectors for each sample"), fontsize=15)
plt.legend(loc='best')

plt.suptitle("BOSSVS", y=1.06, fontsize=22)
plt.show()
