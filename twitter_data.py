#!/usr/bin/env python
# encoding: utf-8

import os
from tweepy import OAuthHandler
import json
import wget
import configparser
import image_processing
import tweepy #https://github.com/tweepy/tweepy
import csv
import argparse
import os

#Twitter API credentials
consumer_key = "jekbS4RL46dzmVvCGxlpphxNg"
consumer_secret = "7XygDfTmTc0P4fnesxhEju7vwsOoYUyY3Ez9az5dMYL9Z040U3"
access_key = "2155459020-QOsV26xZ3nXt7nuD75XF1fOOszqALNGvawfgIl5"
access_secret = "gQWyZ8YxvXlhAfbkvgdIRzRsyskx0OYzV3WIhfbq4L0Re"

dictionaries = []

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
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.created_at, tweet.text.encode("utf-8"), "http://twitter.com/"+screen_name+"/status/"+tweet.id_str] for tweet in alltweets]
	
	f = open("text_tags.txt", "r")
		
	for tweet in alltweets:	
		for line in f:
			if line.strip() in tweet.text.lower():
				dictionaries.append({'text' : tweet.text, 'link' : "http://twitter.com/"+screen_name+"/status/"+tweet.id_str, 'msg' : "This was flagged because it contained" + line, 'date' : tweet.created_at})

def parse_arguments(username):
	parser = []
	parser.append(username)
	parser.append(200)
	parser.append(True)
	parser.append(True)

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

def authorise_twitter_api():
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

def parse_image(image_url, url, date):
	result_text = image_processing.analyzeImage(image_url)
	result = image_processing.checkImageData(result_text)
	dictionaries.append({'img' : image_url, 'link' : url, 'msg' : result, 'date' : date})


def download_images(api, username, retweets, replies, num_tweets):
	tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies)

	downloaded = 0
	while (len(tweets) != 0):
		last_id = tweets[-1].id

		for status in tweets:
			media = status.entities.get('media', [])
			if(len(media) > 0 and downloaded < num_tweets):
				parse_image(media[0]['media_url'], "http://twitter.com/"+username+"/status/" + status.entities.get(0, 'id_str'), status.entities.get(0, 'created_at'))
			downloaded += 1

		tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies, max_id=last_id-1)


def main(username):
	arguments = parse_arguments(username)
	username = arguments[0]
	num_tweets = arguments[1]
	retweets = arguments[2]
	replies = arguments[3]

	auth = authorise_twitter_api()
	api = tweepy.API(auth)

	download_images(api, username, retweets, replies, num_tweets)


def get_parsed_tweets():
#if __name__ == "__main__":
	get_all_tweets("CatHacks2018")
	main("CatHacks2018")
	return dictionaries
