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
		self.myOled = oled.oled(self.rowcount)
		self.myOled.writerow(1,"RSS Testing....     ")
		self.feeds = {	"RSS: BBC Tech News" : 'http://feeds.bbci.co.uk/news/technology/rss.xml',
						"RSS: The Register" : 'http://www.theregister.co.uk/data_centre/cloud/headlines.atom',
						"RSS: Jobsite" : 'http://www.jobsite.co.uk/cgi-bin/advsearch?rss_feed=1&skill_include=product%20development&location_include=Gloucestershire&location_within=20&search_currency_code=GBP&search_single_currency_flag=N&search_salary_type=A&daysback=7&scc=UK&compare_resolved=CO_GLOUCESTERSHIRE&compare_search=Gloucestershire'
						}

	def output(self,outputstring):
		chars = '{:<20}'.format(outputstring[0:20])	
		self.myOled.writerow(1,chars)
		chars = '{:<20}'.format(outputstring[20:40])		
		self.myOled.writerow(2,chars)
		chars = '{:<20}'.format(outputstring[40:60])		
		self.myOled.writerow(3,chars)
		
	def titlerow(self,string):
		chars = '{:<20}'.format(string)		
		self.myOled.writerow(4,chars)
						
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
						   help='the register rss')
		parser.add_argument('-j', '--jobs', dest='joblink', action='store_true',
						   help='jobsite rss')
		args = parser.parse_args()
		if args.link == True:
			d = self.newlink()
		elif args.joblink == True:
			d = self.jobslink()
		else:
			d = self.defaultlink()
		print d.feed.title
		return(d,d.feed.title)
	
	def nonparsed(self,link):
		if link == "Register":
			d = self.newlink()
		elif link == "Jobs":
			d = self.jobslink()
		else:
			d = self.defaultlink()
		print d.feed.title
		return(d,d.feed.title)
	
	def timeonly(self):
		stuff = time.strftime("%R")
		self.myOled.writerow(2,stuff)
		return(0)
	
	def dictread(self):
		for feedname,feedaddress in self.feeds.iteritems():
			print feedname
			self.titlerow(feedname)
			d = feedparser.parse(feedaddress)
			filteredlist = self.filtering(d)
			self.showentries(filteredlist,feedname,count=2)
		return(0)
			
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
	
	def showentries(self,filteredlist,feedtitle,count=3):
		oldstring = ""
		for j,i in enumerate(filteredlist[0:count]):
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
	myParser = rssparser(2)
	while True:
		myParser.timeonly()
		time.sleep(30)
#	myParser.dictread()
	

