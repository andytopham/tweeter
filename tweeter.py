#!/usr/bin/python
''' 
		tweeter.py - my twitter tester.
'''

import sys
from twython import Twython
import oled
import time
import logging
import datetime
import rssparser
import twitterkeys

class tweeter:
	def __init__(self):
		print "Tweeter tester"
		self.myOled = oled.oled(4)
		self.myOled.writerow(1,"Tweeter          ")
		self.api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
		self.myParser = rssparser.rssparser()
		
	def sendtweet(self):
		self.api.update_status(status=sys.argv[1][:140])

	def gettweet(self):
		''' Return a single tweet. '''
		user_timeline = self.api.get_home_timeline(count=3)
		return(user_timeline)
		
	def showtweet(self, tweet):
		''' Get the latest tweet and show it on the oled.'''
#		user_timeline = self.api.get_home_timeline(count=1)
		oldstuff="Scrambled text."
		stuff = tweet['text']
		userarray = tweet['user']
		screen_name = userarray['screen_name']
		print "Sender: ",screen_name
		print "Tweet text: ",stuff
		self.myOled.writerow(1,screen_name)
		self.myOled.writerow(2,stuff[0:20])
		for i in range(len(stuff)+5):	#add 5 to handle scroll limitations
			time.sleep(.2)
			self.myOled.scroll(stuff, 2)

	def processtweet(self, incoming):
		shortened = incoming[0:138]			# often get rubbish at the tail of msg
		try:
			shortened.decode('ascii')		# catch any scrambled text
		except:
			return("Scrambled msg")
		if shortened[0:10] == "New post: ":
			return(shortened[10:])
		else:
			return(shortened)
			
	def showtweet4row(self, tweet):
		''' Get the latest tweet and show it on the oled.'''
		oldstuff="Scrambled text."
		incoming = tweet['text']
		userarray = tweet['user']
		screen_name = userarray['screen_name']
		print "Sender: ",screen_name
		print "Tweet text: ",incoming
		stuff = self.processtweet(incoming)
		self.myOled.writerow(1,screen_name)
		self.myOled.writerow(2,stuff[0:20])
		self.myOled.writerow(3,stuff[20:40])
		self.myOled.writerow(4,stuff[40:60])

	def scrolllastrow(self,stuff):
		for i in range(len(stuff)+5):	#add 5 to handle scroll limitations
			time.sleep(.2)
			self.myOled.scroll(stuff[40:], 4)
		self.myOled.writerow(4,stuff[40:60])	# leave the finish looking OK
							
	def testing(self):
		''' Just some stuff to add more dictionary parsing. '''
		print repr(tweet)
		print tweet.keys()
		for key, value in tweet.iteritems():
			print key, value
			try:
				for subkey, newvalue in key.iteritems():
					print subkey, newvalue
			except:
				pass
	
if __name__ == "__main__":
	print "Running tweeter class as a standalone app"
	logging.basicConfig(filename='log/tweeter.log',
						filemode='w',
						level=logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running tweeter class as a standalone app")
	myTweeter = tweeter()
	myParser = rssparser.rssparser()
	while True:
		myParser.doitall()	
		tweetlist = myTweeter.gettweet()
		for tweet in tweetlist:
			myTweeter.showtweet4row(tweet)
			time.sleep(5)
		