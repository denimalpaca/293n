from __future__ import print_function

import csv
import sys
from datetime import datetime
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
import numpy

import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics

numpy.set_printoptions(threshold=numpy.nan)

berkeley_data = []
berkeley_target = []
fsu_data = []
fsu_target = []
texasam_data = []
texasam_target = []
ucla_data = []
ucla_target = []
ucsb_data = []
ucsb_target = []

ifile = open(sys.argv[1], 'rb')

reader = csv.reader(ifile)

categories = ['aggies', 'berkeley', 'fsu', 'ucla', 'UCSantaBarbara']

reader.next()
for row in reader:
	subreddit_raw = row[0]
	comment_raw = row[1]

	if subreddit_raw == 'aggies':
		subreddit = 0
		texasam_data.append(comment_raw)
		texasam_target.append(subreddit)
	elif subreddit_raw == 'berkeley':
		subreddit = 1
		berkeley_data.append(comment_raw)
		berkeley_target.append(subreddit)
	elif subreddit_raw == 'fsu':
		subreddit = 2
		fsu_data.append(comment_raw)
		fsu_target.append(subreddit)
	elif subreddit_raw == 'ucla':
		subreddit = 3
		ucla_data.append(comment_raw)
		ucla_target.append(subreddit)
	elif subreddit_raw == 'UCSantaBarbara':
		subreddit = 4
		ucsb_data.append(comment_raw)
		ucsb_target.append(subreddit)

ifile.close()

training_size = 0.2

berkeley_size = len(berkeley_target)
berkeley_slice = int(berkeley_size*training_size)
texasam_size = len(texasam_target)
texasam_slice = int(texasam_size*training_size)
fsu_size = len(fsu_target)
fsu_slice = int(fsu_size*training_size)
ucla_size = len(ucla_target)
ucla_slice = int(ucla_size*training_size)
ucsb_size = len(ucsb_target)
ucsb_slice = int(ucsb_size*training_size)

y_train = berkeley_target[:berkeley_slice]\
	+ texasam_target[:texasam_slice]\
	+ fsu_target[:fsu_slice]\
	+ ucla_target[:ucla_slice]\
	+ ucsb_target[:ucsb_slice]

y_test = berkeley_target[berkeley_slice:]\
	+ texasam_target[texasam_slice:]\
	+ fsu_target[fsu_slice:]\
	+ ucla_target[ucla_slice:]\
	+ ucsb_target[ucsb_slice:]

X_train_raw = berkeley_data[:berkeley_slice]\
	+ texasam_data[:texasam_slice]\
	+ fsu_data[:fsu_slice]\
	+ ucla_data[:ucla_slice]\
	+ ucsb_data[:ucsb_slice]

X_test_raw = berkeley_data[berkeley_slice:]\
	+ texasam_data[texasam_slice:]\
	+ fsu_data[fsu_slice:]\
	+ ucla_data[ucla_slice:]\
	+ ucsb_data[ucsb_slice:]

if False:
    vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                   n_features=2**16)
    X_train = vectorizer.transform(X_train_raw)
    feature_names = None
else:
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')
    X_train = vectorizer.fit_transform(X_train_raw)
    feature_names = vectorizer.get_feature_names()

if feature_names:
    feature_names = np.asarray(feature_names)

X_test = vectorizer.transform(X_test_raw)

def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

###############################################################################
# Benchmark classifiers
def benchmark(clf):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print("density: %f" % density(clf.coef_))

        if feature_names is not None:
            print("top 10 keywords per class:")
            for i, category in enumerate(categories):
                top10 = np.argsort(clf.coef_[i])[-10:]
                print(trim("%s: %s"
                      % (category, " ".join(feature_names[top10]))))
        print()

    if True:
        print("classification report:")
        print(metrics.classification_report(y_test, pred,
                                            target_names=categories))

    if True:
        print("confusion matrix:")
        print(metrics.confusion_matrix(y_test, pred))

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time


results = []
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
        #(KNeighborsClassifier(n_neighbors=10, n_jobs=-1, leaf_size=120), "kNN"),
        (RandomForestClassifier(n_estimators=100, n_jobs=-1), "Random forest")):
    print('=' * 80)
    print(name)
    results.append(benchmark(clf))

for penalty in ["l2", "l1"]:
    print('=' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    results.append(benchmark(LinearSVC(loss='l2', penalty=penalty,
                                            dual=False, tol=1e-3)))

    # Train SGD model
    results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                           penalty=penalty)))

# Train SGD with Elastic Net penalty
print('=' * 80)
print("Elastic-Net penalty")
results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                       penalty="elasticnet")))

# Train NearestCentroid without threshold
print('=' * 80)
print("NearestCentroid (aka Rocchio classifier)")
results.append(benchmark(NearestCentroid()))

# Train sparse Naive Bayes classifiers
print('=' * 80)
print("Naive Bayes")
results.append(benchmark(MultinomialNB(alpha=.01)))
results.append(benchmark(BernoulliNB(alpha=.01)))

print('=' * 80)
print("LinearSVC with L1-based feature selection")
# The smaller C, the stronger the regularization.
# The more regularization, the more sparsity.
results.append(benchmark(Pipeline([
  ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
  ('classification', LinearSVC())
])))



