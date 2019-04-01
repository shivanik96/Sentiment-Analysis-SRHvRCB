import tweepy
import re
import csv
from tweepy import OAuthHandler
from textblob import TextBlob

class Twitter():
	##Twitter class for sentiment analysis##

	def __init__(self):
		##Authorising Twitter API client##
	
		consumer_key = "OQ6qpSS0dWF81qCW26GiAgt3b"
		consumer_secret = "mwnfribmH5hLhNEza5sLI7ztDIMrKDx4VtgVLXudC8fF0SxiDu"
		access_token = "1112357938444722176-RQiKbDINaz0Ec7rIuTOlCa9PRTcKUz"
		access_token_secret = "F1FH5LDnGno1UzYxdx3oh1QJ3x6XsO2TmZ52Ipd6FBO81"

		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Authentication Failed")

	def preprocess_tweet(self, tweet):
		##Preprocessing a tweet##

		link_ex = "https?:\/\/[A-Za-z0-9./]+"
		handle_ex = "@[A-Za-z0-9_]+"
		hashtag_ex = "#[A-Za-z0-9_]+"
		spcl_ex = "[^0-9A-Za-z .]"

		tweet = re.sub(link_ex, " ", tweet)			#removing links
		tweet = re.sub(handle_ex, " ", tweet)		#removing twitter handles
		tweet = re.sub(hashtag_ex, " ", tweet)		#removing hashtags
		tweet = re.sub(spcl_ex, " ", tweet)			#removing special characters
		tweet = ''.join([i if ord(i) < 128 else ' ' for i in tweet])	#removing non-ascii characters

		return tweet

	def clean_tweet_text(self, tweet_text):
		##Cleaning tweet to store in the CSV file##
		
		spcl_ex = "[^0-9A-Za-z .@#!?]"
		tweet_text = re.sub(spcl_ex, " ", tweet_text)		#removing special characters
		tweet_text = ''.join([i if ord(i) < 128 else ' ' for i in tweet_text])	#removing non-ascii characters

		return tweet_text

	def get_tweet_sentiment(self, tweet):
		##Getting sentiment of a tweet##

		tweet_stats = TextBlob(self.preprocess_tweet(tweet))
		if tweet_stats.sentiment.polarity < 0:
			return "negative"
		elif tweet_stats.sentiment.polarity == 0:
			return "neutral"
		else:
			return "positive"

	def get_tweets(self, topic, tweet_count):
		##GET request to retrieve english tweets on a particular topic##

		tweets = list()
		try:
			matched_tweets = self.api.search(q = topic, lang='en', show_user = False, count = tweet_count)
			for tweet in matched_tweets:
				parsed_tweet = {}
				parsed_tweet['text'] = self.clean_tweet_text(tweet.text)
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				#Checking if the tweet is already present in our list because of it being retweeted
				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets
		except tweepy.TweepError as e:
			print("Error: " +str(e))

def main():
	my_api = Twitter()
	topic = "#SRHvRCB"
	tweets = my_api.get_tweets(topic, tweet_count = 100)

	# for tweet in tweets:
	# 	print(tweet['text'] + " --------->> " + tweet['sentiment'] + "\n\n")

	pos_tweets = [t for t in tweets if t['sentiment'] == 'positive']
	neg_tweets = [t for t in tweets if t['sentiment'] == 'negative']
	neut_tweets_num = len(tweets)-len(pos_tweets)-len(neg_tweets)

	pos_percentage = float(100*len(pos_tweets)/len(tweets))
	neg_percentage = float(100*len(neg_tweets)/len(tweets))
	neut_percentage = float(100*neut_tweets_num/len(tweets))

	print("\n\n---Aggregate Analysis for the topic: " + topic + "---\n")
	print("1. Percentage of POSITIVE tweets -> " + str(pos_percentage) + "%")
	print("2. Percentage of NEGATIVE tweets -> " + str(neg_percentage) + "%")
	print("3. Percentage of NEUTRAL tweets -> " + str(neut_percentage) + "%")
	
	keys = tweets[0].keys()
	with open("Sentiment_Analysis_SRHvRCB.csv", "wb") as f:
		w = csv.DictWriter(f,keys)
		w.writeheader()
		w.writerows(tweets)
	print("\n\n\nCSV file named \"Sentiment_Analysis_SRHvRCB.csv\" created for individual analysis!\n\n")

if __name__ == "__main__": 
	main()