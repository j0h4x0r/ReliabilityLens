import datetime
import numpy
from sklearn.cluster import MeanShift, estimate_bandwidth

class ProfileAnalysis(object):
	'''
	This is a simple analysis of user's profile, 
	including following/follower ratio, status count 
	and created time.
	It returns a score between 0 and 1.
	'''
	def __init__(self):
		self.follow_ratio_limit = 10.0
		self.statuses_count_limit = 20.0
		self.join_time_limit = 7.0

	def _get_follow_ratio(self, user):
		ratio = float(user['friends_count']) / user['followers_count']
		return ratio

	def _get_statuses_count(self, user):
		return user['statuses_count']

	def _get_join_time(self, user):
		return user['created_at']

	def get_statistics(self, user):
		res = {
			'follow_ratio': self._get_follow_ratio(user),
			'statuses_count': self._get_statuses_count(user),
			'join_time': self._get_join_time(user),
		}
		return res

	def analyze(self, user):
		score = 0.0
		stats = self.get_statistics(user)
		# Here we use 1/x to calculate the score so that larger ratio will be punished significantly more
		score += 1 if stats['follow_ratio'] < self.follow_ratio_limit else 1 / (stats['follow_ratio'] - self.follow_ratio_limit + 1)
		score += 1 if stats['statuses_count'] > self.statuses_count_limit else stats['statuses_count'] / self.statuses_count_limit
		today = datetime.date.today()
		now = datetime.datetime.now()
		limit = datetime.timedelta(self.join_time_limit)
		score += 1 if today - stats['join_time'].date() > limit else (now - stats['join_time']).seconds / float(limit.seconds)
		score /= len(stats)
		return score

class FriendsAnalysis(object):
	'''
	This is an analysis of a user's friends. 
	We extract features including followings, 
	favorites, etc. And then we perform clustering
	to see how many groups the friends can be divided.
	The more groups, the worse the user is.
	3~5 groups should be reasonable.
	A number between 0 and 1 will be returned.
	'''
	def __init__(self):
		self.group_limit = 10.0

	def _extract_features(self, friends):
		vectors = []
		for friend in friends:
			vec = [friend['followers_count'], friend['friends_count'], friend['favourites_count'], friend['statuses_count']]
			vectors.append(vec)
		return vectors

	def _mean_shift_clustering(self, X):
		ms = MeanShift()
		ms.fit(X)
		labels = ms.labels_
		cluster_centers = ms.cluster_centers_
		labels_unique = numpy.unique(labels)
		n_clusters = len(labels_unique)
		return {
			'labels': labels,
			'cluster_centers': cluster_centers,
			'n_clusters': n_clusters,
		}

	def clustering(self, friends):
		vectors = self._extract_features(friends)
		res = self._mean_shift_clustering(vectors)
		return res

	def analyze(self, friends):
		group_count = self.clustering(friends)['n_clusters']
		score = 1 if group_count < self.group_limit else self.group_limit / group_count
		print 'Number of groups among the friends:', group_count
		return score
