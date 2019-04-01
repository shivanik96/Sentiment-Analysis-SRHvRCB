# Sentiment-Analysis-SRHvRCB

Overview
--------
This project is a python script that performs sentiment analysis on tweets on the topic- SRHvRCB.
This project uses Tweepy python library to access Twitter API to retrieve tweets on the topic - SRHvRCB. The retrieved tweets are preprocessed by removing texts that include links, twitter handles, hashtags and any other special character. TextBlob is a function in the Python library textblob which is used to identify the polarity of the given tweet which is further used to do sentiment analysis.
Aggregate sentiment analysis is displayed on the terminal only while sentiment analysis for each tweet retrieved is stored in a CSV file.

Procedure
--------
-> We start our python script by authorising Twitter API client.
-> Then we make a GET request to Twitter API to fetch english language tweets for a particular topic.
-> The fetched tweets are preprocessed by removing any links, twitter handles, hashtags or other special characters.
-> We parse each fetched tweet and store it in a python dictionary along with the tweet's sentiment which is computed using the polarity returned by the TextBlob function. The polarity value lies between -1 and 1. If the value is >0 the text's sentiment is considered to be positive. If it is <0 the sentiment is considered to be negative. Otherwise, the sentiment is considered to be neutral.
-> We use a simple rule to check whether the tweet is already present in the dictionary so that no tweet is repeated even if it is retweeted.
-> Finally, we calculate the percentage of the positive, negative and neutral tweets in the retrieved tweets.
-> Individual tweets along with their sentiments are stored in a csv file.

Libraries Required
--------
tweepy, re, csv, textblob
