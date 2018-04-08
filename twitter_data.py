#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import argparse

#Twitter API credentials
consumer_key = "jekbS4RL46dzmVvCGxlpphxNg"
consumer_secret = "7XygDfTmTc0P4fnesxhEju7vwsOoYUyY3Ez9az5dMYL9Z040U3"
access_key = "2155459020-QOsV26xZ3nXt7nuD75XF1fOOszqALNGvawfgIl5"
access_secret = "gQWyZ8YxvXlhAfbkvgdIRzRsyskx0OYzV3WIhfbq4L0Re"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('tweets/%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	parser = argparse.ArgumentParser(description='Process a username.')
	parser.add_argument('username', type=str, help='a username')
	args = parser.parse_args()
	get_all_tweets(args.username)

