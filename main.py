#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import gdata.youtube
import gdata.youtube.service
import gdata.alt.appengine
import re
import jinja2
import os
import traceback
import httplib
import feedparser

#####jinja setup ######
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

###### Handler setup #######
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw)) 
        
def to_unicode(obj, encoding='utf-8'):
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding)
	return obj  
	         
def getVideos(handler,queryString):

	client = gdata.youtube.service.YouTubeService()
    	gdata.alt.appengine.run_on_appengine(client)
    	query = gdata.youtube.service.YouTubeVideoQuery()
    	query.vq = queryString  # the term(s) that you are searching for
    	query.orderby = 'relevance_lang_en' 
    	query.time = 'today'   # how to display the results
    	query.max_results = '8'        # number of results to retrieve
    	query.lang = "utf-8"
    	#handler.response.out.write('<span class="listing_title">Searching for "' +  query.vq + '"</span><br /><br />')
    	feed = client.YouTubeQuery(query)
    	entries = feed.entry
    	for e in entries:
    		e.title.text.decode('utf-8')
    		e.title.text.encode('utf-8')
    		
    	handler.render('sport_vids.html', entries=entries)
    	
    	
####web scraping methods...they work but then found feedparser#####
""" 
def getLinks(handler, sportString):
	links = []
	response = ''
	error = ''
	if sportString == 'soccer':
		url = 'http://espnfc.com/'
	else:
		url = 'http://www.espn.com'
		url += sportString
	
	try:	
		response = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		error = e
		links.append(error)
		return links
	except urllib2.URLError as e:
		error = e
		links.append(error)
		return links
	except httplib.HTTPException as e:
		error = e
		links.append(error)
		return links
	except Exception:
		links.append('Somethings totally messed up...try again later')
		return links
	
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	results = soup.find('ul', attrs={'class' : 'headlines'})
	if results:
		for h in results.find_all('a'):
			link = h.get('href')
			preLink = 'http://espnfc.com/'
			if not str(link).startswith('http://'):
				if sportString == 'soccer':
					link = preLink + str(link)
				else:
					link = 'http://www.espn.com' + link
			text = h.contents[0]
			a = {"link":link, "title":text}
			if len(links) < 8:
				links.append(a)
	else:
		links.append('Could not find any links')
	
	return links
			
def getSILinks(handler, sportString):
	links = []
	response = ''
	error = ''
	
	url = 'http://sportsillustrated.cnn.com/'
	url += sportString
	
	try:	
		response = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		error = e
		links.append(error)
		return links
	except urllib2.URLError as e:
		error = e
		links.append(error)
		return links
	except httplib.HTTPException as e:
		error = e
		links.append(error)
		return links
	except Exception:
		links.append('Somethings totally messed up...try again later')
		return links
	
		
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	
	results = soup.find('div', attrs={'class' : 'cnnT2s'})
	if results:
	
		for h in results.find_all('a'):
			link = h.get('href')
			preLink = 'http://sportsillustrated.cnn.com'
			if not str(link).startswith('http://'):
				link = preLink + str(link)
			text = h.contents[0]
			a = {"link":link, "title":text}
			if len(links) < 10:
				links.append(a)
		#first two li's are not actual links... so slicing them off	
		links = links[2:]
		
	else:
		links.append('Could not find any links')

	return links
	
def getCBSLinks(handler, sportString):
	links = []
	response = ''
	error = ''
	
	url = 'http://www.cbssports.com/'
	url += sportString
	
	try:	
		response = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		error = e
		links.append(error)
		return links
	except urllib2.URLError as e:
		error = e
		links.append(error)
		return links
	except httplib.HTTPException as e:
		error = e
		links.append(error)
		return links
	except Exception:
		links.append('Somethings totally messed up...try again later')
		return links
	
		
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	
	results = soup.find('ul', attrs={'class' : 'topStories flush linone'})
	if results:
	
		for h in results.find_all('a'):
			link = h.get('href')
			preLink = 'http://www.cbssports.com'
			if not str(link).startswith('http://'):
				link = preLink + str(link)
			text = h.contents[0]
			a = {"link":link, "title":text}
			if len(links) < 8:
				links.append(a)
	else:
		links.append('Could not find any links')
			
	return links
	
def getGoalLinks(handler, sportString):
	links = []
	response = ''
	error = ''
	
	url = 'http://www.goal.com/en-us/'
	url += sportString
	
	try:	
		response = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		error = e
		links.append(error)
		return links
	except urllib2.URLError as e:
		error = e
		links.append(error)
		return links
	except httplib.HTTPException as e:
		error = e
		links.append(error)
		return links
	except Exception:
		links.append('Somethings totally messed up...try again later')
		return links
	
		
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	
	results = soup.find('div', attrs={'id' : 'breakingNewsList'})
	if results:
	
		for h in results.find_all('a'):
			link = h.get('href')
			preLink = 'http://www.goal.com/en-us'
			if not str(link).startswith('http://'):
				link = preLink + str(link)
			text = h.contents[0]
			a = {"link":link, "title":text}
			if len(links) < 8:
				links.append(a)
	else:
		links.append('Could not find any links')
	
	return links
"""

def getRSS(url):
	d = feedparser.parse(url)
	links = d.entries[0:8]
	return links
	
class MainHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_topstories.rss')
    	linksCBS = getRSS('http://feeds.cbssports.com/cbssportsline/home_news')
    	self.render('nav.html', pageTitle = 'All Sports')
    	getVideos(self,'sports+highlights')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


class NBAHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/nba/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_nba.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/nba_news')
    	self.render('nav.html', pageTitle = 'NBA', scoreLink = 'http://espn.go.com/nba/scoreboard')
    	getVideos(self,'NBA+highlights')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


    	
class BballHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/ncb/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_ncaab.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/cb_news')
    	self.render('nav.html', pageTitle = 'College Basketball', scoreLink = 'http://scores.espn.go.com/ncb/scoreboard')
    	getVideos(self,'college+basketball')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )



class FootballHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/nfl/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_nfl.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/nfl_news')
    	self.render('nav.html', pageTitle = 'NFL', scoreLink = 'http://scores.espn.go.com/nfl/scoreboard')
    	getVideos(self,'NFL+highlights')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


    	
class NCAAFootballHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/ncf/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_ncaaf.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/cfb_news')
    	self.render('nav.html', pageTitle = 'College Football', scoreLink = 'http://scores.espn.go.com/college-football/scoreboard')
    	getVideos(self,'college+football+BCS')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


    	
class SoccerHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://soccernet.espn.go.com/rss/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_soccer.rss')
    	linksCBS = getRSS('http://www.goal.com/en/feeds/news fmt=rss')
    	self.render('nav.html', pageTitle = 'Soccer', scoreLink='http://espnfc.com/scores')
    	getVideos(self,"soccer goals")
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


class MLBHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/mlb/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_mlb.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/mlb_news')
    	
    	self.render('nav.html', pageTitle = 'Baseball', scoreLink='http://scores.espn.go.com/mlb/scoreboard')
    	getVideos(self,"MLB Baseball")
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


class HockeyHandler(Handler):
    def get(self):
    	errorESPN = ''
    	errorSI = ''
    	errorCBS = ''
    	links = getRSS('http://sports.espn.go.com/espn/rss/nhl/news')
    	linksSI = getRSS('http://rss.cnn.com/rss/si_hockey.rss')
    	linksCBS = getRSS('http://cbssports.com/partners/feeds/rss/nhl_news')
    	self.render('nav.html', pageTitle = 'Hockey', scoreLink='http://scores.espn.go.com/nhl/scoreboard')
    	getVideos(self,'NHL+highlights')
    	
    	if len(linksSI) <1:
    		errorSI = "Couldn't load feed...Try again later."
    		
    	if len(links) <1:
    		errorESPN = "Couldn't load feed...Try again later."
    		
    	if len(linksCBS) <1:
    		errorCBS= "Couldn't load feed...Try again later."
    		
    	self.render('sports_links.html', links= links, linksSI = linksSI,linksCBS = linksCBS, errorCBS = errorCBS, errorESPN = errorESPN, errorSI = errorSI )


    	
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/collegebball', BballHandler),
    ('/collegefootball', NCAAFootballHandler),
    ('/profootball', FootballHandler),
    ('/soccer', SoccerHandler),
    ('/probasketball', NBAHandler),
    ('/baseball', MLBHandler),
    ('/hockey', HockeyHandler)
], debug=True)
