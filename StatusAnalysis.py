import math, collections, re

class TimeSeriesAnalysis(object):
	def _analyze_series(self, series):
		'''
		This is a time series analysis. The input is a list of number, 
		and it returns a score showing how normal the potential pattern is.
		We assume the data are normally distributed, and likelihood is 
		then used as the score.
		'''
		# This may only works well with large data
		if not len(series):
			return 0
		# compute likelihood
		mean = float(sum(series)) / len(series)
		variance = sum(map(lambda x: (x - mean) ** 2, series))
		distribution = lambda x: 1 / math.sqrt(2 * math.pi * variance) * (math.e ** ((-(x - mean) ** 2) / (2 * variance)))
		likelihood = reduce(lambda x, y: x * y, map(distribution, series))
		return likelihood

	def _generate_count_series(self, tweets):
		'''
		This function takes a list of tweets (with timestamps) 
		and return a list of the numbers of tweets a user created every day.
		'''
		dates = map(lambda t: t['created_at'].date(), tweets)
		count_dict = collections.Counter(dates)
		min_date = min(dates)
		days = (max(dates) - min_date).days + 1
		count_series = [count_dict[min_date + datetime.timedelta(i)] if min_date + datetime.timedelta(i) in count_dict else 0 for i in range(days)]
		return count_series

	def analyze(self, tweets):
		series = self._generate_count_series(tweets)
		score = self._analyze_series(series)
		return score

class SentimentAnalysis(object):
	def __init__(self, lexicon = 'AFINN-111.txt'):
		self._read_sentiment_lexicon(lexicon)

	def _read_sentiment_lexicon(self, lexicon):
		with open(lexicon) as dictfile:
			senti_dict = {line[0]: int(line[1]) for line in dictfile}
		self.sentiment_word_dict = {k: senti_dict[k] for k in senti_dict if ' ' not in k}
		self.sentiment_phrase_dict = {k: senti_dict[k] for k in senti_dict if ' ' in k}

	def _tokenize(self, text):
		# remove all non-ascii
		eng_text = re.sub('/[^a-zA-Z- ]+/g', '', text)
		# remove continuous spaces
		clean_text = re.sub('/ {2,}/', ' ', eng_text).lower()
		return clean_text.split()

	def _lexicon_based_analyze(self, text):
		# score is a number between -5 and 5
		tokens = self._tokenize(text)
		score = 0.0
		for token in tokens:
			if token in self.sentiment_word_dict:
				score += self.sentiment_word_dict[token]
		for phrase in self.sentiment_phrase_dict:
			if phrase in text:
				score += self.sentiment_phrase_dict[phrase]
		score /= len(tokens)
		return score

	def analyze(self, tweet):
		score = self._lexicon_based_analyze(tweet['text'])
		return score