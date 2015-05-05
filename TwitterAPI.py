import tweepy

class TwitterAPI(object):

	def __init__():
		self.consumer_key = 'drsdK24HynMJ4muIUJeRRDOGw'
		self.consumer_secret = 'LzQe8b0n9kDGTvt8NHZReNsAiHvAyVtiePiO5vAH1qiegje4Ub'
		self.access_token = '1064868938-2iS7qSA0LzgywVLbonbXeyblfbYRoyOCetSNQfO'
		self.access_token_secret = 'wAM6NJWM8jCGmwx7a4rbYBko97DDsKCBxwCRUpCwoKl0m'

		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)

		# settings
		self.friends_limit = 1000

	def extract_user_info(self, user):
		res = {}
		res['id'] = user.id
		res['screen_name'] = user.screen_name
		res['followers_count'] = user.followers_count
		res['friends_count'] = user.friends_count # followings count
		res['favourites_count'] = user.favourites_count
		res['statuses_count'] = user.statuses_count
		res['description'] = user.description
		res['profile_image_url'] = user.profile_image_url
		try:
			res['status'] = user.status.text.encode(encoding = 'utf-8')
		except:
			res['status'] = None
		return res

	def get_user(self, user_id = None, screen_name = ""):
		uid = user_id if user_id else screen_name
		try:
			user = self.api.get_user(id = uid)
		except tweepy.TweepError as e:
			return {}
		return self.extract_user_info(user)

	def get_friends(self, user_id = None, screen_name = ""):
		uid = user_id if user_id else screen_name
		try:
			friends = tweepy.Cursor(self.api.friends, id = uid, count = 200).items(self.friends_limit)
		except tweepy.TweepError as e:
			return []
		res = []
		for friend in friends:
			res.append(self.extract_user_info(friend))
		return res

	def get_comments(self):
		### TO DO

	def get_statuses(self):
		### TO DO