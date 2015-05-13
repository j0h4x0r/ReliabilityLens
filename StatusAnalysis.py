import math
import collections

def analyze_series(series):
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

def generate_count_series(tweets):
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