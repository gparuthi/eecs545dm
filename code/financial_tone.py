#!/usr/bin/python

def analyst_tone(positive_tokens, negative_tokens, text):
	'''Calculate Analyst Tone Based on Negative/Positive financial terms'''
	
	# Tokenize the text
	eliminate_these_chars = ['&amp;', '\'', '.', '"']
	replace_these_chars_with_space = ["-"]
	for e in eliminate_these_chars: text = text.replace(e,"")
	for e in replace_these_chars_with_space: text = text.replace(e, " ")
	text = text.lower().split(" ")
	
	# Perform Comparison
	positive = [text.count(w) for w in positive_tokens]
	negative = [text.count(w) for w in negative_tokens]
	
	return float(sum(positive) + 1) / float(sum(negative)+1)
