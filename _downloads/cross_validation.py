"""
Cross-validation: some gotchas
===============================

Cross-validation is the ubiquitous test of a machine learning model. Yet
many things can go wrong.

"""

###############################################################
# The uncertainty of measured accuracy
# ------------------------------------
#
# The first thing to have in mind is that the results of a
# cross-validation are noisy estimate of the real prediction accuracy
#
# Let us create a simple artificial data
from sklearn import datasets, discriminant_analysis
import numpy as np
np.random.seed(0)
data, target = datasets.make_blobs(centers=[(0, 0), (0, 1)])
classifier = discriminant_analysis.LinearDiscriminantAnalysis()

###############################################################
# Characterizing the uncertainty of cross-validation
# ...................................................
from sklearn.model_selection import cross_val_score
print(cross_val_score(classifier, data, target))

###############################################################
# What if we try different random shuffles of the data?
from sklearn import utils
for _ in range(10):
    data, target = utils.shuffle(data, target)
    print(cross_val_score(classifier, data, target))

###############################################################
# This should not be surprising: if the lassification rate is p, the
# observed distribution of correct classifications on a set of size
# follows a binomial distribution
from scipy import stats
n = len(data)
distrib = stats.binom(n=n, p=.7)

###############################################################
# We can plot it:
from matplotlib import pyplot as plt
plt.figure(figsize=(6, 3))
plt.plot(np.linspace(0, 1, n), distrib.pmf(np.arange(0, n)))

###############################################################
# It is wide, because there are not that many samples to mesure the error
# upon: iris is a small dataset
#
# We can look at the interval in which 95% of the observed accuracy lies
# for different sample sizes
for n in [100, 1000, 10000, 100000]:
    distrib = stats.binom(n, .7)
    interval = (distrib.isf(.025) - distrib.isf(.975)) / n
    print("Size: {0: 7}  | interval: {1}%".format(n, 100 * interval))

###############################################################
# At 100 000 samples, 5% of the observed classification accuracy still
# fall more than .5% away of the true rate
#
# **Keep in mind that cross-val is a noisy measure**

###############################################################
# Confounding effects and non independence
# -----------------------------------------

###############################################################
# Permutations to measure chance
# -------------------------------

