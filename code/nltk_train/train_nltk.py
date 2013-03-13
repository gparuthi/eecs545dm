import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 

class BayesClass(object):
	def __init__(self):
		self.feats = []
		self.load_nltk()


	def word_feats(self, words):
	    return dict([(word, True) for word in words])

	def load_nltk(self): 
		negids = movie_reviews.fileids('neg')
		posids = movie_reviews.fileids('pos')
		 
		negfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
		posfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
		 
		negcutoff = len(negfeats)*3/4
		poscutoff = len(posfeats)*3/4
		 
		trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
		testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
		print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
		 
		classifier = NaiveBayesClassifier.train(trainfeats)
		print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

		classifier.show_most_informative_features()

		self.classifier = classifier
		self.feats = testfeats[0][0]

	def getBagOfWords(self,text):
		eliminate_these_chars = ['&amp;', '\'', '.', '"']
		replace_these_chars_with_space = ["-"]
		for e in eliminate_these_chars: text = text.replace(e,"")
		for e in replace_these_chars_with_space: text = text.replace(e, " ")
		bow = text.lower().split(" ")
		return bow

	def getSentiment(self, bow):
		feats = self.feats
		for f in feats:
			feats[f] = False
		for w in bow:
			if w in feats:
				feats[w] = True
		return self.classifier.classify(feats)

	def getSentimentFromText(self,anal_text):
		# get bag of words
		anal_bow = self.getBagOfWords(anal_text)
		# get sentiment
		anal_sent = self.getSentiment(anal_bow)
		return anal_sent


def getSentiments(bc, item):
	from datetime import datetime
	from financial_tone import analyst_tone,POSITIVE,NEGATIVE

	c = 0
	res = {}
	anal_text = ''
	manager_text = ''
	cid= item[0]
	res[cid] = {}

	if 'Analyst' in item[1]:
	    anal_text = item[1]['Analyst']
	    #print anal_text

	if 'CEO-Chair' in item[1]:
	    manager_text += item[1]['CEO-Chair']

	if 'Finance' in item[1]:
	    manager_text += item[1]['Finance']
	    
	if 'Operator' in item[1]:
	    manager_text += item[1]['Operator']

	ana_tone = bc.getSentimentFromText(anal_text)
	manager_tone = bc.getSentimentFromText(manager_text)
	res[cid]['a_tone'] = ana_tone
	res[cid]['m_tone'] = manager_tone   
	# print '[%s] %s' % (str(datetime.now()), res[cid])
	return (cid,res[cid])

# each item in items is a dict: {cid:{MASTER1:'text', MASTER2:'text'}}
def start(items):
	nltk_res = {}
	b= BayesClass()
	c =0 
	print datetime.now()
	rc= parallel.Client()
	lview = rc.load_balanced_view() 
	lview.block = True
	dview = rc[:]
	for r in items:
	    a = getSentiments(b,r)
	    nltk_res[a[a.keys()[0]]]append(a)
	    if c%100 == 0:
	    	print '[%s] %d/%d' %(datetime.now(), c, len(items))

