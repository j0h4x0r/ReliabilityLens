import math, collections, re, datetime
from nltk.corpus import stopwords

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
		# another likelihood
		likelihood = reduce(lambda x, y: x + y, map(distribution, series))
		#likelihood /= len(series)
		#likelihood = 1 if likelihood * 100 > 1 else likelihood * 100
		likelihood = 1 if likelihood > 1 else likelihood
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
	'''
	This is a sentiment analysis. The input can be a single tweet or a list of tweets.
	analyze_sentiment() returns a value between -5 and 5 indicating the sentiment of the tweets(s). 
	analyze() returns a score value between 0 and 1 based on the sentiment indicating how neutral a user is.
	If a list is given, the average score will be returned.
	Here a lexicon-based method is used.
	'''
	def __init__(self, lexicon = 'AFINN-111.txt'):
		self._read_sentiment_lexicon(lexicon)

	def _read_sentiment_lexicon(self, lexicon):
		with open(lexicon) as dictfile:
			senti_dict = dict(map(lambda (k, v): (k, int(v)), [line.split('\t') for line in dictfile]))
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

	def analyze_sentiment(self, tweets):
		if type(tweets) is list:
			score = 0.0
			for tweet in tweets:
				score += self._lexicon_based_analyze(tweet['text'])
			score /= len(tweets)
		else:
			score = self._lexicon_based_analyze(tweets['text'])
		return score

	def analyze(self, tweets):
		sentiment = self.analyze_sentiment(tweets)
		score = float(sentiment + 1) / 2
		score = 0 if score < 0 else (1 if score > 1 else score)
		# compute how neutral
		score -= 0.5
		score = -score if score < 0 else score
		score *= 2
		score = 1 - score
		return score

class WordAnalysis(object):
	'''
	This is an analysis for words in a list of tweets.
	The output is a score between 0 and 1, indicating
	the quality of the tweets.
	Here repeating words, punctuations, uppercase words 
	and average length are considered.
	'''
	def __init__(self):
		self.stopwords = []
		for word in stopwords.words('english'):
			self.stopwords.append(word.encode('utf8', 'ignore'))
		# limit of average appearance of a word in a sentence
		self.max_avg_limit = 1.0
		self.punctuation_limit = 5.0
		self.uppercase_limit = 1.0
		self.length_limit = 5.0

	def _tokenize(self, text):
		# remove all non-ascii
		eng_text = re.sub('/[^a-zA-Z- ]+/g', '', text)
		# remove continuous spaces
		clean_text = re.sub('/ {2,}/', ' ', eng_text).lower()
		return clean_text.split()

	def count_words(self, tweet):
		'''
		It counts the number of every word in the tweet and
		returns a Counter object which is a subclass of dict.
		'''
		tokens = self._tokenize(tweet['text'])
		return collections.Counter(tokens)

	def count_punctuaions(self, tweet):
		#exception_list = '#@'
		#count = reduce(lambda x, y: x + 1 if y not in exception_list and y in string.puncuation else x, tweet['text'], 0)
		count = reduce(lambda x, y: x + 1 if y in '?!~$*' else x, tweet['text'], 0)
		return count

	def count_uppercase(self, tweet):
		tokens = self._tokenize(tweet['text'])
		count = reduce(lambda x, y: x + 1 if y.isupper() else x, tokens, 0)
		return count

	def calculate_length(self, tweet):
		return len(self._tokenize(tweet['text']))

	def calculate_statistics(self, tweets):
		res = {
			'words_count': collections.Counter(),
			'punctuation': 0,
			'uppercase': 0,
			'length': 0,
		}
		for tweet in tweets:
			res['words_count'].update(self.count_words(tweet))
			res['punctuation'] += self.count_punctuaions(tweet)
			res['uppercase'] += self.count_uppercase(tweet)
			res['length'] += self.calculate_length(tweet)
		# stop words are removed
		res['words_count'] = {key: res['words_count'][key] for key in res['words_count'] if key not in self.stopwords}
		res['punctuation'] /= float(len(tweets))
		res['uppercase'] /= float(len(tweets))
		res['length'] /= float(len(tweets))
		return res

	def analyze(self, tweets):
		stats = self.calculate_statistics(tweets)
		self.stats = stats
		score = 0.0
		count = float(len(tweets))
		# if the top word appears almost in every tweet, then this might be meaningless.
		max_word_avg = max(stats['words_count'].iteritems(), key = lambda x: x[1])[1] / count
		score += 0 if max_word_avg > self.max_avg_limit else 1 - max_word_avg / self.max_avg_limit
		# punctuation
		score += 0 if stats['punctuation'] > self.punctuation_limit else 1 - stats['punctuation'] / self.punctuation_limit
		# uppercase
		score += 0 if stats['uppercase'] > self.uppercase_limit else 1 - stats['uppercase'] / self.uppercase_limit
		# avg length
		score += 1 if stats['length'] > 5 else stats['length'] / self.length_limit
		score /= len(stats)
		return score
