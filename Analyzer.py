import TwitterAPI, UserAnalysis, StatusAnalysis
import json, heapq, copy

def analyze(username):
	# collect data
	api = TwitterAPI.TwitterAPI()
	print 'Getting user information...'
	user = api.get_user(username)
	print 'Getting frineds information...'
	friends = api.get_friends(username)
	print 'Getting tweets...'
	tweets = api.get_statuses(username)
	print 'All data collected!'

	res = {'analysis': {}, 'data': {}, 'user': copy.deepcopy(user)}
	# datetime is converted to ISO string to be serializable
	res['user']['created_at'] = res['user']['created_at'].isoformat()
	total = []

	# user analysis
	print '\nPerforming user analysis...'
	res['analysis']['user'] = {}
	print 'Analyzing profile...'
	profileAnalyzer = UserAnalysis.ProfileAnalysis()
	res['analysis']['user']['profile'] = profileAnalyzer.analyze(user)
	total.append(res['analysis']['user']['profile'])
	print 'Analyzing friends...'
	friendsAnalyzer = UserAnalysis.FriendsAnalysis()
	res['analysis']['user']['friends'] = friendsAnalyzer.analyze(friends)
	total.append(res['analysis']['user']['friends'])

	# status analysis
	print '\nPerforming status analysis...'
	res['analysis']['status'] = {}
	print 'Analyzing frequency...'
	timeSeriesAnalyer = StatusAnalysis.TimeSeriesAnalysis()
	res['analysis']['status']['frequency'] = timeSeriesAnalyer.analyze(tweets)
	total.append(res['analysis']['status']['frequency'])
	print 'Analyzing sentiment...'
	sentimentAnalyzer = StatusAnalysis.SentimentAnalysis()
	res['analysis']['status']['sentiment'] = sentimentAnalyzer.analyze(tweets)
	total.append(res['analysis']['status']['sentiment'])
	print 'Analyzing words...'
	wordAnalyzer = StatusAnalysis.WordAnalysis()
	res['analysis']['status']['word'] = wordAnalyzer.analyze(tweets)
	total.append(res['analysis']['status']['word'])

	print 'Analysis done!'

	# data for front end
	print '\nPreparing data...'
	res['data']['friends'] = []
	for friend in friends:
		info = {k: friend[k] for k in friend if k in ['screen_name', 'friends_count', 'profile_image_url']}
		res['data']['friends'].append(info)
	# top 10 words, only work after word analysis
	words_count = wordAnalyzer.stats['words_count']
	res['data']['words'] = map(lambda k: (k, words_count[k]), heapq.nlargest(10, words_count, key = lambda k: words_count[k]))
	print 'Data prepared!'

	# total score
	#res['analysis']['total'] = sum(total) / len(total)
	res['analysis']['total'] = min(total)
	return res

if __name__ == '__main__':
	username = raw_input('Input the username to be analyzed: ')
	res = analyze(username)
	with open('result.txt', 'w') as resfile:
		resfile.write(json.dumps(res))
