#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class TwitterStreamListener(StreamListener):
	"""
	Listener that store tweets received from Twitter stream in a file
	"""
	
	def __init__(self, filename):
		"""
		Default constructor. Initializes the listener and open the file where the tweets will be stored
		
		:param filename File name where the tweets will be stored
		"""

		super(TwitterStreamListener, self).__init__()
		self.tweetsFile = open(filename, 'w')

	def on_data(self, rawData):
		"""
		Handler when data are received, store them in the file
		
		:param rawData Raw data received from the Twitter stream
		"""

		self.tweetsFile.write(rawData)
		return True
	
	def on_error(self, statusCode):
		"""
		Handler when an error occurred
		
		:param statusCode
		"""

		print statusCode

def load_credentials(filename = "credentials.txt"):
	"""
	Load Twitter credentials from a file
	
	:param filename File name from which the credentials will be loaded
	:return Dictionnary containing information for OAuth loaded from the configuration file
	"""
	
	oauthInfos = {}

	with open(filename) as credentials_file:
		for line in credentials_file:
			oauth_varname, oauth_val = line.split('=')
			oauthInfos[oauth_varname.strip()] = oauth_val.strip()
	
	return oauthInfos

def usage():
	"""
	Print a help message
	"""

	print "usage: twgrabber [-h] <keywords> <file>"
	print "\t-c | --credentials <file>	file containing the credentials to use for the authentication on the Twitter API. Default is credentials.txt"
	print "\t-h | --help				print this help message and exit"
	print "\t<keywords>					list of keywords to filter separated by a comma"
	print "\t<file>						file where data will be written"

def print_version():
	"""
	Print the version on stdout
	"""
	
	print "twgrabber 0.1"

if __name__ == "__main__":
	# parse command line
	try:
		options, arguments = getopt.getopt(sys.argv[1:], "c:hv", ["credentials=", "help", "version"])
	except getopt.GetoptError as error:
		print error
		usage()
		sys.exit(1)
	
	# parse options
	credentialFile = "credentials.txt"
	for option, argument in options:
		if option == "-c" or option == "--credentials":
			credentialFile = argument
			print credentialFile
		elif option == "-h" or option == "--help":
			usage()
			sys.exit(0)
		elif option == "-v" or option == "--version":
			print_version()
			sys.exit(0)
	
	# one and only one argument should be given, it is the file where the data will be stored
	if len(arguments) != 2:
		usage()
		sys.exit(1)
	
	keywords = arguments[0].split(',')
	outputFilename = arguments[1]
	
	# load credentials from configuration file
	oauthInfos = load_credentials(credentialFile)
	
	# initialize the authentication
	auth = OAuthHandler(oauthInfos['consumer_key'], oauthInfos['consumer_secret'])
	auth.set_access_token(oauthInfos['access_token'], oauthInfos['access_token_secret'])
	
	# initialize the stream and start grabbing tweets
	stream = Stream(auth, TwitterStreamListener(outputFilename))
	stream.filter(track=keywords)
