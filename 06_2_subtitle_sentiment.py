# -*- coding: utf-8 -*-
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
#from nltk.tokenize.regexp import WordTokenizer, WhitespaceTokenizer
#from nltk.tokenize.treebank import TreebankWordTokenizer
import os
import re
import string
import sys
import math


#file = "shining_text-only.txt"
#print file

os.chdir(sys.argv[1])
file = "subtitles.txt"

corpus = PlaintextCorpusReader(os.getcwd(), file) # word_tokenizer=TreebankWordTokenizer()


def evaluate_classifier(featx):
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	 
	negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
	 
	trainfeats = negfeats + posfeats
	classifier = NaiveBayesClassifier.train(trainfeats)

	p = 0
	n = 0
	x = 0

	for s in corpus.sents():
		s = [w for w in s] # if w not in stopwords.words("english")
		
		prob = classifier.prob_classify(featx(s))
		
		if prob.prob("pos") > 0.65:
			p += 1
		elif prob.prob("neg") > 0.65:
			n += 1
		else:
			# ignore almost "neutral" ones
			x += 1
			pass

	print "pos:", p, "-- neg:", n, "-- ignored:", x
	if n > p:
		print "1 :", n/float(p)
		print math.degrees( math.atan( 0.5 * n/float(p) ) ), "°" # steigungswinkel
		                                                   # negativ fällt, positiv steigt
	if p > n:
		print p/float(n), ": 1"
		print "-", math.degrees( math.atan( 0.5 * p/float(p) ) ), "°"


def word_feats(words):
	return dict([(word, True) for word in words])

#evaluate_classifier(word_feats)


import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
 
def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
	bigram_finder = BigramCollocationFinder.from_words(words)
	bigrams = bigram_finder.nbest(score_fn, n)
	return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])
 
#evaluate_classifier(bigram_word_feats)

# #################################################################
from nltk.probability import FreqDist, ConditionalFreqDist

word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

for word in movie_reviews.words(categories=['pos']):
	word_fd.inc(word.lower())
	label_word_fd['pos'].inc(word.lower())

for word in movie_reviews.words(categories=['neg']):
	word_fd.inc(word.lower())
	label_word_fd['neg'].inc(word.lower())

# n_ii = label_word_fd[label][word]
# n_ix = word_fd[word]
# n_xi = label_word_fd[label].N()
# n_xx = label_word_fd.N()

pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()
total_word_count = pos_word_count + neg_word_count

word_scores = {}

for word, freq in word_fd.iteritems():
	pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
	neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
	word_scores[word] = pos_score + neg_score

best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
bestwords = set([w for w, s in best])

def best_word_feats(words):
	return dict([(word, True) for word in words if word in bestwords])

#evaluate_classifier(best_word_feats)


def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
	bigram_finder = BigramCollocationFinder.from_words(words)
	bigrams = bigram_finder.nbest(score_fn, n)
	d = dict([(bigram, True) for bigram in bigrams])
	d.update(best_word_feats(words))
	return d

#print 'evaluating best words + bigram chi_sq word features'
evaluate_classifier(best_bigram_word_feats)