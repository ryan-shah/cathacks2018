#!/usr/bin/env python
# encoding: utf-8

import os
from tweepy import OAuthHandler
import json
import wget
import configparser
#import image_processing
import tweepy #https://github.com/tweepy/tweepy
import csv
import argparse
import os

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
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.created_at, tweet.text.encode("utf-8"), "http://twitter.com/"+screen_name+"/status/"+tweet.id_str] for tweet in alltweets]
	
	#write the csv
	#TODO - remove the write code and replace it with dictionary creation
	if (not(os.path.isdir("tweets"))):
		os.mkdir("tweets")
	
	with open('tweets/%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['created_at','text', 'url'])
		writer.writerows(outtweets)
	
	pass

def parse_arguments():
	parser = argparse.ArgumentParser(description='Download pictures from a Twitter feed.')
	parser.add_argument('username', type=str, help='The twitter screen name from the account we want to retrieve all the pictures')
	parser.add_argument('--num', type=int, default=100, help='Maximum number of tweets to be returned.')
	parser.add_argument('--retweets', default=True, action='store_true', help='Include retweets')
	parser.add_argument('--replies', default=True, action='store_true', help='Include replies')
	parser.add_argument('--output', default='pictures/', type=str, help='folder where the pictures will be stored')

	args = parser.parse_args()
	return args

def parse_config(config_file):
	config = configparser.ConfigParser()
	config.read(config_file)
	return config

@classmethod
def parse(cls, api, raw):
	status = cls.first_parse(api, raw)
	setattr(status, 'json', json.dumps(raw))
	return status

def init_tweepy():
	# Status() is the data model for a tweet
	tweepy.models.Status.first_parse = tweepy.models.Status.parse
	tweepy.models.Status.parse = parse
	# User() is the data model for a user profil
	tweepy.models.User.first_parse = tweepy.models.User.parse
	tweepy.models.User.parse = parse

def authorise_twitter_api(config):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

def parse_image(url):
	print('#TODO - parse input') #TODO - use image_processing to assist in creating output

def download_images(api, username, retweets, replies, num_tweets, output_folder):
	tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies)
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	downloaded = 0
	while (len(tweets) != 0):
		last_id = tweets[-1].id

		for status in tweets:
			media = status.entities.get('media', [])
			if(len(media) > 0 and downloaded < num_tweets):
				#wget.download(media[0]['media_url'], out=output_folder)
				if (not(os.path.isdir("pictures"))):
					os.mkdir("pictures")

				parse_image(media[0]['media_url'])

			downloaded += 1

		tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies, max_id=last_id-1)


def main():
	arguments = parse_arguments()
	username = arguments.username
	retweets = arguments.retweets
	replies = arguments.replies
	num_tweets = arguments.num
	output_folder = arguments.output

	config = parse_config('twitter_config.cfg')
	auth = authorise_twitter_api(config)
	api = tweepy.API(auth)

	download_images(api, username, retweets, replies, num_tweets, output_folder)


if __name__ == '__main__':
	#pass in the username of the account you want to download
	parser = argparse.ArgumentParser(description='Process a username.')
	parser.add_argument('username', type=str, help='a username')
	args = parser.parse_args()
	get_all_tweets(args.username)
	main()
