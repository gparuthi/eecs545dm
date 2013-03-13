import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 

class nltk_analysis(object):
	def __init__(self):



	def word_feats(self, words):
	    return dict([(word, True) for word in words])

	def load_nltk(self): 
		negids = movie_reviews.fileids('neg')
		posids = movie_reviews.fileids('pos')
		 
		negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
		posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
		 
		negcutoff = len(negfeats)*3/4
		poscutoff = len(posfeats)*3/4
		 
		trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
		self.testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
		print 'train on %d instances, test on %d instances' % (len(trainfeats), len(self.testfeats))
		 
		classifier = NaiveBayesClassifier.train(trainfeats)
		print 'accuracy:', nltk.classify.util.accuracy(classifier, self.testfeats)
		classifier.show_most_informative_features()