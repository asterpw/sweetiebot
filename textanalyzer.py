#!/usr/bin/python
import os
import sys
sys.path.append(os.getcwd() + "/readability")
import readability

common_words = set(["it's", "i've", "http", "img", "imgur", "youtube", "that", "this", "then", "and", "you", "its", "the", "but", "for", "www", "com", "net", "are", "where", "was", "when", "im", "have", "just", "not", "like", "with", "they", "what", "there", "their", "did", "theyre", "dont", "you're", "your", "all", "can", "get", "them", "thats", "out", "has", "had", "one", "from", "about", "know", "jpg", "png", "i'm", "i'd", "i've", "don't", "would", "why", "any", "gif", "people", "because", "see", "more", "some", "that's", "also", "were", "how", "will", "isn't", "his", "who", "much", "than", "which", "into", "really", "got", "use", "think", "well", "still", "only", "time", "way", "too", "i'll", "could", "those", "here", "make", "other", "lot", "most", "want", "now", "good", "though", "should", "doesn't", "even", "say", "being", "didn't", "they're", "sure", "can't", "she", "her", "him", "https"])

def calcStats(text):
	'''For a set string of text, return a tuple of the following items:
		number of characters
		number of words
		number of sentences
		number of syllables
		number of complex words (i.e., with >= 3 syllables)
	'''
	characters = 0
	words = 0
	complex_words = 0
	one_syllable_words = 0
	syllables = 0
	sentences = 0
	dictList = [{}, {}, {}, {}, {}]
	lastFewWords = []
	result = {}
	for line in text.split("\n"):
		line = line.strip()
		if len(line) == 0:
			continue
		line = line + "."
		for word in line.split():
			word = word.lower()  # Ignore proper nouns
			if readability.EndOfSentence(word):
				sentences += 1
			word = readability.StripNonletters(word)
			if word.startswith("b:") or word.startswith("f:"):
				continue
			if len(word) == 0:
				continue
			
			lastFewWords.append(word)
			if len(lastFewWords) > 5:
				lastFewWords.pop(0)
			for i in range(len(lastFewWords)):
				phrase = " ".join(lastFewWords[-(i+1):])
				dictList[i][phrase] = dictList[i].get(phrase, 0) + 1
				
			words += 1
			characters += len(word)
			number_of_syllables = readability.CountSyllables(word)
			syllables += number_of_syllables
			if number_of_syllables >= 3:
				complex_words += 1
			if number_of_syllables == 1:
				one_syllable_words += 1
		
	bigphraselists = [frequency.items() for frequency in dictList]
	bigphraselists[0] = [word for word in bigphraselists[0] if len(word[0]) > 3 and word[0].replace("#", "'") not in common_words and not word[0].startswith("http")]
	
	phraselists = []
	for phraselist in bigphraselists:
		phraselist.sort(key=lambda x: -1*x[1])
		phraselists.append(phraselist[0:min(10,len(phraselist))])
	
	fog  = readability.GunningFogIndex(words, sentences, complex_words)
	ari  = readability.AutomatedReadibilityIndex(characters, words, sentences)
	cl   = readability.ColemanLiauIndex(characters, words, sentences)
	fkre = readability.FleschKincaidReadingEase(words, syllables, sentences)
	fkgl = readability.FleschKincaidGradeLevel(words, syllables, sentences)
	smog = readability.SMOGIndex(complex_words, sentences)
	forc = readability.FORCASTReadabilityFormula(words, one_syllable_words)
	result['characters'] = characters
	result['words'] = words
	result['complex_words'] = complex_words
	result['one_syllable_words'] = one_syllable_words
	result['syllables'] = syllables
	result['sentences'] = sentences
	result['GunningFogIndex'] = fog
	result['AutomatedReadibilityIndex'] = ari
	result['ColemanLiauIndex'] = cl
	result['FleschKincaidReadingEase'] = fkre
	result['FleschKincaidGradeLevel'] = fkgl
	result['SMOGIndex'] = smog
	result['FORCASTReadabilityFormula'] = forc
	result['favoritewords0'] = bigphraselists[0][:300]
	result['favoritewords1'] = phraselists[1]
	result['favoritewords2'] = phraselists[2]
	result['favoritewords3'] = phraselists[3]
	result['favoritewords4'] = phraselists[4]
	
	return result
