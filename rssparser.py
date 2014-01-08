#!/usr/bin/python
""" rssparser.py
	This grabs a rss feed and scrolls the titles from this acros the oled display.
	Choose rss feed from command line options.
	Used as a test for feedparser and argparse.
	sudo pip install feedparser
"""
import feedparser
import oled
import time
import argparse
import logging
import datetime

class rssparser:
	def __init__(self,rows=2):
		self.divider = " ** "
		self.delay=4
		self.rowcount = rows
		self.scrolldelay = .2
		self.myOled = oled.oled(4)
		self.myOled.writerow(1,"RSS Testing....      ")

	def output(self,outputstring):
		chars = '{:<20}'.format(outputstring[0:20])	
		self.myOled.writerow(1,chars)
		chars = '{:<20}'.format(outputstring[20:40])		
		self.myOled.writerow(2,chars)
		chars = '{:<20}'.format(outputstring[40:60])		
		self.myOled.writerow(3,chars)
		self.titlerow()
		
	def titlerow(self):
		chars = '{:<20}'.format("RSS: BBC Tech News")		
		self.myOled.writerow(4,chars)
				
	def defaultlink(self):
		d = feedparser.parse('http://feeds.bbci.co.uk/news/technology/rss.xml')
		return(d)

	def newlink(self):
		d = feedparser.parse('http://www.theregister.co.uk/data_centre/cloud/headlines.atom')
		return(d)

	def filtering(self,d):
		z = []
		j = 0
		for k in d.entries:
			if k.title[0:5] != "VIDEO":
				z.append(k)			# pop does not take it off the list, but returns it
				j += 1
		print "*** Number of entries: ",len(d.entries),
		print "Number of entries after remove: ",len(z)
		return(z)
			
	def parsing(self):
		parser = argparse.ArgumentParser(description='parser.py - display the contents of a rss feed on an oled')
		parser.add_argument('-l', '--link', dest='link', action='store_true',
						   help='process this link')
		args = parser.parse_args()
		if args.link == True:
			d = self.newlink()
		else:
			d = self.defaultlink()
		print d.feed.title
		return(d,d.feed.title)
		
	def scrollingshowentries(self,filteredlist,feedtitle):
		self.titlerow()
		oldstring = ""
		for j,i in enumerate(filteredlist[0:3]):
#			self.myOled.writerow(2,feedtitle[:13]+":"+str(j))
			start=0
			divstart=0
			print i.title
			if oldstring == "":
				oldstring = i.title
				continue
			while start < (len(oldstring)+len(self.divider)):
				padding = 20 - len(oldstring) - len(self.divider) + start
				if (start > len(oldstring)):
					divstart += 1
				outputstring = oldstring[start:]+self.divider[divstart:]+i.title[0:padding]
				self.myOled.writerow(1, outputstring)
				start += 1
				time.sleep(self.scrolldelay)
				oldstring = i.title
		# now need to just output the very last item
		start = 0
		while start < (len(i.title)+1):
			outputstring = i.title[start:]+" "		#remember to clear the trailing char
			self.myOled.writerow(1,outputstring)
			start += 1
			time.sleep(self.scrolldelay)
		return(0)

	def doitall(self):
		d,feedtitle = self.parsing()
		filteredlist = self.filtering(d)
		self.showentries(filteredlist,feedtitle)
	
	def showentries(self,filteredlist,feedtitle):
		oldstring = ""
		for j,i in enumerate(filteredlist[0:3]):
			start=0
			divstart=0
			print i.title
			if oldstring == "":
				oldstring = i.title
			outputstring = i.title
			self.output(outputstring)
			time.sleep(self.delay)
		return(0)
		
if __name__ == "__main__":
	print "Running parser class as a standalone app"
	logging.basicConfig(filename='log/parser.log',
						filemode='w',
						level=logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running parser class as a standalone app")
	myParser = rssparser(4)
	myParser.doitall()
#	while True:
#		tweetlist = myTweeter.gettweet()
#		for tweet in tweetlist:
#			myTweeter.showtweet(tweet)
#			myTweeter.showtweet4row(tweet)
#			time.sleep(5*60)			

