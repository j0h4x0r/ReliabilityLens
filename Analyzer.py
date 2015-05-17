import TwitterAPI, UserAnalysis, StatusAnalysis
import json

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

	res = {'analysis': {}, 'data': {}}

	# user analysis
	print '\nPerforming user analysis...'
	res['analysis']['user'] = {}
	print 'Analyzing profile...'
	profileAnalyzer = UserAnalysis.ProfileAnalysis()
	res['analysis']['user']['profile'] = profileAnalyzer.analyze(user)
	print 'Analyzing friends...'
	friendsAnalyzer = UserAnalysis.FriendsAnalysis()
	res['analysis']['user']['friends'] = friendsAnalyzer.analyze(friends)

	# status analysis
	print '\nPerforming status analysis...'
	res['analysis']['status'] = {}
	print 'Analyzing frequency...'
	timeSeriesAnalyer = StatusAnalysis.TimeSeriesAnalysis()
	res['analysis']['status']['frequency'] = timeSeriesAnalyer.analyze(tweets)
	print 'Analyzing sentiment...'
	sentimentAnalyzer = StatusAnalysis.SentimentAnalysis()
	res['analysis']['status']['sentiment'] = sentimentAnalyzer.analyze(tweets)
	print 'Analyzing words...'
	wordAnalyzer = StatusAnalysis.WordAnalysis()
	res['analysis']['status']['word'] = wordAnalyzer.analyze(tweets)

	print 'Analysis done!'

	# data for front end
	print '\nPreparing data...'
	res['data']['friends'] = []
	for friend in friends:
		info = {k: friend[k] for k in friend if k in ['screen_name', 'friends_count', 'profile_image_url']}
		res['data']['friends'].append(info)
	print 'Data prepared!'
	return res

if __name__ == '__main__':
	username = raw_input('Input the username to be analyzed: ')
	res = analyze(username)
	with open('result.txt', 'w') as resfile:
		resfile.write(json.dumps(res))
