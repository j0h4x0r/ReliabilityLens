# ReliabilityLens
## Motivation
This is a social media reliability analysis. The goal of this project is to tell whether an Twitter account is reliable or not based on a self-designed rating system. Some algorithms are designed to compute a score for a given account. An account with a higher score is more likely to be an authority.

## Approach
### Status Analysis
* Time Series Analysis
The input is a list of numbers that represents the amounts of tweets a user created every day, and it returns a score showing how normal the potential pattern is. 

An account that suddenly tweets a lot in a short period of time is more likely to be spam. It is assumed that the data are normally distributed, and likelihood is then used as the score. So the account with a higher likelihood is less likely to be a fake follower or spam.

* Sentiment Analysis
The input can be a single tweet or a list of tweets. It first returns a value between -5 and 5 indicating the sentiment of the tweets(s), and then a final score between 0 and 1 indicating how neutrality is computed.

A simple lexicon-based method sentiment analysis algorithm is used here.

* Word Analysis
The input is a list of tweets, and the output is a score between 0 and 1, which indicates the quality of the tweets.

It is assumed that meaningful tweets should contain a reasonable number of repeated use of words, punctuations, all-uppercase words. Normal tweets should also have reasonable length.

### User Analysis
* Profile Analysis
A user's profile, including followings, followers, favourites, statuses count and join time, is analyzed here. A score between 0 and 1 is returned here. 

A reliable Twitter account should not have a very high following/follower ratio, and its status count and join time should be reasonable.

* Friend Analysis
A normal user should have a reasonable range of interests. Thus the groups of all its friends should not be too many. To identify the groups of all the friends, a clustering algorithm (Mean-shift) is used here.

Features like followings and favourites of a user’s friends are extracted. Clustering is then performed to see how many groups the friends can be divided into. The more groups, the worse the user is. 8~10 groups should be reasonable, and a score between 0 and 1 will be returned.

## Tools & Libraries
* Data collecting: [Tweepy](https://github.com/tweepy/tweepy)
* Analysis: [Numpy](http://www.numpy.org/), [Scikit-learn](http://scikit-learn.org/), [NLTK](http://www.nltk.org/)
* Web: [Flask](http://flask.pocoo.org/), [D3.js](http://d3js.org/), [d3-cloud](https://github.com/jasondavies/d3-cloud)
