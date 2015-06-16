#!/usr/bin/python
import cookielib
import re
import mechanize
import time
from pprint import pprint as pp
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from imagesearch import imageSearch
from chatterbotapi import ChatterBotFactory, ChatterBotType
import os
import random
import textanalyzer
from configobj import ConfigObj
import socket
import urllib
import datetime
import maketagcloud
import logging
from dateutil import relativedelta
import poker
import pwdb
import cats
import wa
from urllib2 import URLError
import socks
import urllib2

loginurl = "http://www.perfectworld.com/login"
accounturl = 'https://account.perfectworld.com/login'
searchurl = 'http://pwi-forum.perfectworld.com/search.php'
showposturl = 'http://pwi-forum.perfectworld.com/showpost.php?p='
#showposturl = "http://aster.ohmydays.net/pw/forumfetch.php?link=showpost.php%3Fp%3D"
#showthreadurl = 'http://aster.ohmydays.net/pw/forumfetch.php?link=showthread.php%%3Ft%%3D%s%%26page%%3D%s'
showthreadurl = 'http://pwi-forum.perfectworld.com/showthread.php?t=%s&page=%s'
showthreadurlforpost = 'http://pwi-forum.perfectworld.com/showthread.php?p='
#showthreadurlforpostproxy = 'http://aster.ohmydays.net/pw/forumfetch.php?link=showthread.php%3Fp%3D'
#showarchivethreadurl = "http://aster.ohmydays.net/pw/forumfetch.php?link=archive%2Findex.php%2Ft-"
showarchivethreadurl = "http://pwi-forum.perfectworld.com/archive/index.php/t-"
#getdailythreadurl = "http://aster.ohmydays.net/pw/forumfetch.php?link=search.php%3Fdo%3Dgetdaily"
getdailythreadurl = "http://pwi-forum.perfectworld.com/search.php?do=getdaily"


chartApiHour = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxr=1,0,23&chxs=0,EFEFEF,12,0,lt,EFEFEF&chxt=x&chbh=a&chs=440x130&cht=bvg&chco=76A4FB&chtt=Posts+by+Hour:&chts=EFEFEF,13,l&chds=a&chd=t:"
chartApiWeekday = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxr=1,0,7&chxs=0,EFEFEF,12,0,lt,EFEFEF&chxt=x&chbh=a&chs=440x130&cht=bvg&chco=76A4FB&chtt=Posts+by+Day:&chts=EFEFEF,13,l&chds=a&chxl=0:|Mon|Tue|Wed|Thu|Fri|Sat|Sun&chd=t:"
chartApiThread = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxs=0,EFEFEF,12,0,lt,EFEFEF&chbh=a&chs=440x110&cht=bvg&chco=76A4FB&chts=EFEFEF,13,l&chds=a&chd=t:"
chartApiPieForums = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxs=0,EFEFEF,11.5&chxt=x&chs=600x245&cht=p3&chco=19B7B4|76A4FB|3072F3|7777CC|7FD1FA&chds=a&chl=%s&chd=t:%s&chp=6&chtt=Posts+by+Forum:&chts=EFEFEF,13,l"
chartApiPieServers = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxs=0,EFEFEF,11.5&chxt=x&chs=600x245&cht=p3&chco=19B7B4|76A4FB|3072F3|7777CC|7FD1FA&chds=a&chl=%s&chd=t:%s&chp=6&chtt=Posters+by+Server:&chts=EFEFEF,13,l"
chartApiWordsVsPostsScatter = "http://chart.googleapis.com/chart?chxt=x,x,y,t&chf=bg,s,1b1c1f&chxs=0,EFEFEF,12,0,lt,EFEFEF|1,EFEFEF,12,0,lt,EFEFEF|2,EFEFEF,12,0,lt,EFEFEF|3,EFEFEF,12,0,lt,EFEFEF&chs=440x310&cht=s&chco=19B7B4|76A4FB|3072F3|7777CC|7FD1FA&chxl=1:||Posts+Per+Day||3:|Words+Per+Post|&chm=o,0000FF,0,,5&chts=EFEFEF,13,l&chds=a&chd=t:"
chartApiWeeklyTopPosters = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxs=0,EFEFEF,12,1,lt,EFEFEF&chxl=0:|%s&chxt=y&chbh=a&chs=440x430&cht=bhs&chco=19B7B4|76A4FB|3072F3|7777CC|7FD1FA&chtt=Weekly+Top+Posters:&chts=EFEFEF,13,l&chds=a&chd=t:%s"

chartApiWeeklyTopPosters = "http://chart.googleapis.com/chart?chf=bg,s,1b1c1f&chxs=0,EFEFEF,12,1,lt,EFEFEF|1,EFEFEF,12,0,l,EFEFEF|2,EFEFEF,12,0,_,EFEFEF&chxl=2:||0:|%s&chxt=y,t,x&chbh=a&chs=440x430&cht=bhs&chco=19B7B4|76A4FB|3072F3|7777CC|7FD1FA&chtt=Weekly+Top+Posters:&chts=EFEFEF,13,l&chds=a&chd=t:%s"


baseurl = 'http://pwi-forum.perfectworld.com/'
#proxybaseurl = "http://aster.ohmydays.net/pw/forumfetch.php?link="

MAX_SLEEP_INTERVAL = 400
TOP_USER_COUNT = 200
ACTIVE_USER_DAY_LIMIT = 31

chatBots = {
	ChatterBotType.PANDORABOTS: ChatterBotFactory().create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477'),
	ChatterBotType.CLEVERBOT: ChatterBotFactory().create(ChatterBotType.CLEVERBOT),
	ChatterBotType.JABBERWACKY: ChatterBotFactory().create(ChatterBotType.JABBERWACKY)
}


br=mechanize.Browser()

config = ConfigObj('sweetiebot.ini')

print "name is", __name__

class TimeZone(datetime.tzinfo):
    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(hours = offset)
        self.__name = name
    def utcoffset(self, dt):
        return self.__offset
    def tzname(self, dt):
        return self.__name
    def dst(self, dt):
        return datetime.timedelta(0)
PST = TimeZone(-8, 'PST')

#non-persistent settings
class Settings:
	def __init__(self):
		self.chatbotSessions = {}
		self.recentThreadId = 0
		self.notNecroThreads = {}
		self.cookies = None
		self.testMode = True
		self.sleeptime = 60
		self.spiderSearch = False
		self.lastReplyTime = 0
		self.allTimeTopPosters = []
		self.activeTopPosters = []
		self.minPostCountAllTime = 0
		self.minPostCountActive = 0
		
settings = Settings()
		
def getTextContentForTag(tag):
	if (tag.name == "a" or tag.name == "img") and tag.text.startswith("http"):
		return ""
	text = u""
	for content in tag.contents:
		if type(content) == NavigableString:
			text += unicode(content)
		elif content.name == "div" and content.get('style') and content.get('style').startswith("margin:20px; margin-top:5px"):
			continue
		else:
			text += getTextContentForTag(content)
	return text
	
	
def htmlOpen(url):
	print "Opening URL:", url
	try:
		html = br.open(url).read()
		soup = BeautifulSoup(html, "html5lib")
		html = soup.prettify()
		#print html
		return html
		#some stupid soup bug makes me do this.
	except:
		return urllib.urlopen(url).read()

class Post:
	def __init__(self, postId, html=""):
		self.postId = postId
		self.forumId = None
		retry_count = 0
		if html=="":
			print "Reading post:", postId, baseurl + 'showpost.php?p='+ str(postId)
			#SPIDER TIME!!
			if settings.spiderSearch and self.doSpider():
				return
			html = htmlOpen(showposturl+ str(postId))
		soup = BeautifulSoup(html, "html5lib")
		tag = soup.find("div",{"class": "bigusername"})
		if type(tag) == type(None):
			raise Exception("ERRROR IS " + html)
		self.name = tag.text.strip().encode('ascii', 'xmlcharrefreplace')
		self.time = soup.find("div",{"class": "time"}).text.strip()
				
		self.admin = '0'

		if self.name == "Asterelle - Sanctuary": self.admin = '1'
		elif re.search("color: turquoise", str(tag)): self.admin = '2'
		elif re.search("color: red", str(tag)): self.admin = '3'
		
		tag = soup.find("div",{"id": "post_message_"+str(postId)})
		self.text = getTextContentForTag(tag)
		self.text = self.text.encode('ascii', 'xmlcharrefreplace') + "\n"
		#print "POST", postId, "\n", self.text
		
		try:
			self.postCount = re.search("<div class=\"smallfont\">\s*Posts: (.*?)\s*</div>", html).group(1).replace(',','')
			self.joinDate = re.search("<div class=\"smallfont\">\s*Join Date: (.*?)\s*</div>", html).group(1)
		except:
			self.postCount = '0'
			self.joinDate = 'Jan 1969'
			print "Error Reading!", postId
		
		self.avatar = ''
		match = re.search("templates/main/images/avatars/([A-Za-z]+[0-9]+)\.jpg", html)
		if match:
			self.avatar = match.group(1)
		
		if int(self.postCount) > settings.minPostCountAllTime:
			if not self.name in settings.allTimeTopPosters and not self.name in config['usersToAnalyze']:
				print "Found new top poster:", self.name, "with", self.postCount,'>', settings.minPostCountAllTime, config['usersToAnalyze']
				config['usersToAnalyze'][self.name] = int(self.postCount)
		
		elif self.admin != '0': 
			if self.name not in config['users'] and self.name not in config['usersToAnalyze']:
				print "Found new Admin poster:", self.name, "with", self.postCount
				config['usersToAnalyze'][self.name] = 9999999
		
		elif (getToday() - getPostTime(self.time).date()).days < ACTIVE_USER_DAY_LIMIT:
			if int(self.postCount) > settings.minPostCountActive:
				if self.name not in settings.activeTopPosters and self.name not in settings.allTimeTopPosters and self.name not in config['usersToAnalyze']:
					users = config['usersToAnalyze'].keys()
					users.sort(key=lambda x: int(config['usersToAnalyze'][x]))
					userStr = "\n".join([str(config['usersToAnalyze'][user]) + " " + user for user in users])
					print "Found new active top poster:", self.name, "with", self.postCount,'>', settings.minPostCountActive, '\n'+userStr
					config['usersToAnalyze'][self.name] = int(self.postCount)
					
		if self.name in config['users']:
			config['users'][self.name]['postCount'] = self.postCount
			if int(self.postId) > int(config['users'][self.name]['samplePost']):
				print "UpdateLastPost", self.name, self.postId, config['users'][self.name]['samplePost']
				registerLastPost(self)

				
	def getThreadId(self):
		html = htmlOpen(showthreadurlforpost+ str(self.postId))
		match = re.search("forumdisplay\.php\?(?:s=[0-9a-f]+&a?m?p?;?)?f=([0-9]+)", html)
		self.forumId = match.group(1)
		match = re.search("showthread\.php\?(?:s=[0-9a-f]+&a?m?p?;?)?mode=hybrid&amp;t=([0-9]+)", html)
		return match.group(1)

	def doSpider(self):
		html = htmlOpen(showthreadurlforpost+ str(self.postId))
		match = re.search("showthread\.php\?(?:s=[0-9a-f]+&a?m?p?;?)?t=([0-9]+)", html)
		posts = Thread(match.group(1), html=html).posts
		for post in posts:
			if post.postId == self.postId:
				self.name = post.name
				self.time = post.time
				self.admin = post.admin
				self.postCount = post.postCount
				self.joinDate = post.joinDate
				self.text = post.text
				self.avatar = post.avatar
				return True
		return False

class PartialPost:
	def __init__(self, name, postId, postDate, threadId, forum):
		self.name = name
		self.postId = postId
		self.postDate = postDate
		self.threadId = threadId
		self.forum = forum
		
	def getFullPost(self):
		return Post(self.postId)


def makeThreadResultFromTag(tag):
	fields = tag.findAll('td')
	postCount = int(fields[3].text.strip().replace(',', '')) + 1
	lastPostTime = getPostTime(fields[2].text.split('by')[0].strip())
	lastPostId = re.search("#post([0-9]+)", str(fields[2])).group(1)
	threadLink = tag.find('a', {'id': re.compile('thread_title_[0-9]+')})
	threadUrl = threadLink['href']
	title = threadLink.text.strip()
	threadId = re.search('t=([0-9]+)', threadUrl).group(1)
	name = fields[2].text.split('by')[1].strip()
	
	author = fields[1].find('div', {'class': 'smallfont'}).text.strip()	
	lastPost = PartialPost(name, lastPostId, lastPostTime, threadId, "")
	isSticky = True if re.search('Sticky:', fields[1].text) else False
	forum = fields[5].text.strip() if len(fields) > 5 else ""
	return ThreadResult(threadId, postCount, lastPost, isSticky, forum, author, title)

class ThreadResult:
	def __init__(self, threadId, postCount, lastPost, isSticky, forum, author, title):
		self.postCount = postCount
		self.threadId = threadId
		self.lastPost = lastPost
		self.isSticky = isSticky
		self.forum = forum
		self.author = author
		self.title = title

	def getFullThread(self, offset=1):
		replynumber = (self.postCount + offset - 1) % self.postCount + 1
		page = int((replynumber - 1) / 10) + 1
		return Thread(self.threadId, page)

class Thread:
	def __init__(self, threadId, page=1, html=''):
		self.threadId = threadId
		retry_count = 0
		print "scanning thread", threadId, showthreadurl%(str(threadId),page)
		if html == '':
			html = htmlOpen(showthreadurl%(str(threadId),page))
		soup = BeautifulSoup(html, "html5lib")
		tags = soup.findAll("div",{"class": "PW-postbit"})
		self.posts = [Post(re.search("showpost\.php\?.*p=([0-9]*)", str(tag)).group(1), 
			str(tag)) for tag in tags]
		tag = soup.find('img', {'alt': "Reload this Page"})		
		self.title = tag.parent.parent.find('strong').text.strip()

def doLogin():
	print 'Doing Login'
	if settings.testMode == True:
		print "No Login During Test Mode"
		return
	response = br.open(loginurl)
	br.select_form("frm_login")
	for control in br.form.controls:
		if control.type == 'text':
			br.form[control.name] = config['login']
		if control.type == 'password':
			br.form[control.name] = config['password']
	br.form.action = accounturl
	response = br.submit()
	settings.cookies.save()
	# SWITCH TO THE PROXY!!
	#if __name__ == "__main__":
	#	socks.set_default_proxy(socks.SOCKS5, "proxy-nl.privateinternetaccess.com",1080,True,"x2341981","KbTTFR4nFU")
	#	socket.socket = socks.socksocket  #dont add ()!!!


def init():
	settings.cookies = cookielib.MozillaCookieJar('./cookies.txt')

	def setup():	
		br.set_cookiejar(settings.cookies)
		#br.set_handle_equiv(True)
		#br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		socket.setdefaulttimeout(30)
		# Want debugging messages?
		#br.set_debug_http(True)
		#br.set_debug_redirects(True)
		#br.set_debug_responses(True)
	
	if os.path.isfile('./cookies.txt'):
		settings.cookies.load('./cookies.txt')
	
	setup()
	settings.cookies.save()
	
	updateTopPosterRanks()

def doSearch(name, subforum='', exactname=True, query=''):
	br.open(searchurl)
	br.select_form("vbform")
	br.form['searchuser'] = name
	br.find_control("exactname").items[0].selected = exactname
	br.find_control("childforums").items[0].selected = False
	br.form['query'] = query #+ " " + str(random.randint(0,999)) + " " + str(random.randint(0,999))
	br.form['showposts'] = ['1']
	doSubForumSelection(subforum)
	response = br.submit()
	return response.read()

def findPostsByName(name, exactname=True):
	return getPartialPostsFromSearchPage(doSearch(name, exactname=exactname))
		
def findPostByName(name, exactname=True):
	posts = findPostsByName(name, exactname=exactname)
	if len(posts) == 0:
		print "Can't Find: ", name
		return 0
	else: 
		print "Found", name, posts[0].postId
		return posts[0]

def getPostIdsFromSearchPage(html):
	matches = re.findall('#post([0-9]*)"', html)
	return matches

def getPartialPostsFromSearchPage(html):
	posts = []
	soup = BeautifulSoup(html, "html5lib")
	tags = soup.findAll("table", id=re.compile('post[0-9]+'))
	for tag in tags:
		links = tag.findAll('a')
		#forum = re.search('<a href="forumdisplay\.php\?f=[0-9]+">(.*?)</a>', taghtml).group(1)
		#forum = tag.find("a", href=re.compile('forumdisplay\.php\?f=[0-9]+')).text
		forum = links[0].text
		name = links[2].text
		threadId = re.search('showthread\.php\?(?:s=[0-9a-f]+&)?t=([0-9]+)', links[1]['href']).group(1)
		dateStr = tag.tbody.tr.td.contents[-1].strip()
		postId = re.search('post([0-9]+)', tag['id']).group(1)
		posts.append(PartialPost(name, postId, getPostTime(dateStr), threadId, forum))
	return posts

def getThreadIdsFromSearchPage(html):
	matches = re.findall('thread_title_([0-9]*)"', html)
	return matches

def extractText(postId):
	try:
		return Post(postId).text
	except:
		return ""
	
def getNextPageLinkFromSearchPage(page):
	for link in br.links(text_regex='^>$'):
		return link.url
	return ""

def getPostTime(timeStr):
	today = getToday().strftime("%m-%d-%Y")
	yesterday = (getToday() - datetime.timedelta(days=1)).strftime("%m-%d-%Y")
	timeStr = timeStr.replace("Today", today).replace("Yesterday", yesterday).replace(",", "")
	posttime = datetime.datetime.strptime(timeStr, "%m-%d-%Y %I:%M %p")
	return posttime

def getTextForName(name, subforum='', doFullSearch=False):
	page = doSearch(name, subforum)
	partialPosts = getPartialPostsFromSearchPage(page)
	nextPageLink = getNextPageLinkFromSearchPage(page)
	
	MAX_CHAR_COUNT = 35000
	MAX_POST_COUNT = 150
	if settings.testMode == True:
		MAX_POST_COUNT = 30
	
	result = {}
	
	result['postByHour'] = [0]*24
	result['postByWeekday'] = [0]*7
	result['postByForum'] = {}
	result['postCount'] = 0
	result['textSample'] = ""
		
	while True:
		for partialPost in partialPosts:
			if partialPost.threadId in config['sweetiebotthreadid'] and not name.startswith(config['botname']):
				continue
			if len(result['textSample']) <= MAX_CHAR_COUNT and result['postCount'] < MAX_POST_COUNT:
				currentPost = partialPost.getFullPost()
				if len(result['postByForum']) == 0: #first item
					result['post'] = currentPost
					result['lastPostDate'] = partialPost.postDate
				#print "reading", currentPost.text
				result['textSample'] += currentPost.text
				result['postCount'] += 1
				currentPost = None
			postDate = partialPost.postDate
			result['postByHour'][postDate.hour] += 1
			result['postByWeekday'][postDate.weekday()] += 1
			result['postByForum'][partialPost.forum] = result['postByForum'].get(partialPost.forum, 0) + 1

		if (len(result['textSample']) > MAX_CHAR_COUNT or result['postCount'] >= MAX_POST_COUNT) and not doFullSearch:
			break
		if nextPageLink != "":
			print " Going to " + nextPageLink
			#page = br.open(proxybaseurl + urllib.quote(nextPageLink)).read()
			page = br.open(nextPageLink).read()
			partialPosts = getPartialPostsFromSearchPage(page)
			nextPageLink = getNextPageLinkFromSearchPage(page)
		else:
			break
	return result

def birthDayFlavor(): 
	text = "\n[url][img]http://i.imgur.com/zbeqXlx.png[/img][/url]"
	
	colors = ['pink', 'wheat', 'LemonChiffon']
	celebrating = ['Celebrating', 'Commemorating', 'Marking the occasion of']
	time = ['2 years', 'two years','two full years', 'my second anniversary']
	chatting = ['replying', 'chatting', 'talking', 'trolling', 'helping']
	here = ['on the forums', 'in the PWI forums', 'on these forums']
	r = random.choice
	
	text += " [color=%s]%s %s of %s %s![/color]\n" % (r(colors), r(celebrating), r(time), r(chatting), r(here))
	
	return text
	
def doReply(postId, text, appendAble=True):
	url = baseurl + "newreply.php?do=newreply&p=" + str(postId)
	print "REPLYING WITH: ", text.encode('ascii', 'xmlcharrefreplace')
	if config["quietmode"] == 'True':
		print "QUIET MODE DETECTED"
		return False
	if settings.testMode == True:
		print "No Reply For Test Mode"
		return False
	html = ''
	try:
		html = br.open(url).read()
		if re.search('<div style="margin: 10px">Sorry! (This forum is not accepting new posts.|This thread is closed!)</div>', html):
			print "CLOSED THREAD! can't respond to", postId
			return False
		br.select_form(name="vbform")
	except:
		doLogin()
		html = br.open(url).read()
		br.select_form(name="vbform")
	
	soup = BeautifulSoup(html, "html5lib")
	tags = soup.findAll("tr", title=re.compile('Post [0-9]+'))
	#text = text + birthDayFlavor()
	text = formatImgText(text, canPostImages(soup))

	if appendAble and tags[0].findAll('td')[0].text == (config['botname'] + " - Lothranis"):
		if not (re.search("General Stats:", text) and re.search("General Stats:", tags[0].text)):
			lastPostId = re.search('Post ([0-9]+)', tags[0]['title']).group(1)
			print "Going to Update %s instead of replying to %s" % (lastPostId, str(postId))
			if doAppendReply(lastPostId, text):
				return lastPostId
			else:
				br.open(url)
				br.select_form(name="vbform")
	br.form['message'] = text.encode('ascii', 'xmlcharrefreplace')
	
	if time.time() - settings.lastReplyTime < 46:
		waittime = 46 + settings.lastReplyTime - time.time()
		print "Posting too fast, waiting %.1fs" % waittime
		time.sleep(waittime)
	br.submit()
	settings.lastReplyTime = time.time()
	print "Reply sent"
	print "Posted", br.geturl()
	time.sleep(5)
	match = re.search("#post([0-9]+)", br.geturl())
	replyId = match.group(1) if match else ''
	return replyId
	
def formatImgText(text, canPostImg):
	if canPostImg:
		text = re.sub('\[url\](\[img\].*?\[/img\])(.*?)\[/url\]', lambda x: x.group(1), text, 5)
	return re.sub('\[url\]\[img\](.*?)\[/img\](.*?)\[/url\]', lambda x: '[url=%s]%s[/url]'%(x.group(1), x.group(2)), text)
	
def canPostImages(soup):
	rules = soup.find('tbody', id='collapseobj_forumrules').text
	return bool(re.search("\[IMG\] code is On", rules, re.IGNORECASE))
	
def doAppendReply(postId, text):
	url = baseurl + "editpost.php?do=editpost&postid=" + str(postId)
	print "APPENDING:", postId
	if config["quietmode"] == 'True':
		print "QUIET MODE DETECTED"
		return False
	if settings.testMode == True:
		print "No Update For Test Mode"
		return False
	try:
		html = br.open(url).read()
		if re.search('<div style="margin: 10px">Sorry! This thread is closed!</div>', html):
			print "CLOSED THREAD! can't respond to", postId
			return False
		br.select_form(name="vbform")
	except:
		doLogin()
		br.open(url)
		br.select_form(name="vbform")	
	currentText = br.form['message'].decode('iso-8859-1').encode('ascii', 'xmlcharrefreplace') + "\n"
	newText = text.encode('ascii', 'xmlcharrefreplace')
	br.form['message'] = currentText + newText
	if len(re.findall('\[img\]', br.form['message'])) > 5:
		return False
	br.submit()
	print "Append sent"
	time.sleep(5)
	return True

		
def updatePost(postId, updates={}, appends={}):
	url = baseurl + "editpost.php?do=editpost&postid=" + str(postId)
	print "UPDATING:", postId, updates.keys(), appends.keys()
	if config["quietmode"] == 'True':
		print "QUIET MODE DETECTED"
		return
	if settings.testMode == True:
		print "No Update For Test Mode"
		return
	try:
		html = br.open(url).read()
		if re.search('<div style="margin: 10px">Sorry! This thread is closed!</div>', html):
			print "CLOSED THREAD! can't respond to", postId
			return
		br.select_form(name="vbform")
	except:
		doLogin()
		br.open(url)
		br.select_form(name="vbform")
	text = br.form['message'].encode('ascii', 'xmlcharrefreplace')
	for updateKey in updates:
		openKey = invisible("<"+updateKey+">")
		closeKey = invisible("</"+updateKey+">")
		text = text[:text.index(openKey) + len(openKey)] + updates[updateKey] + text[text.index(closeKey):]
	for appendKey in appends:
		closeKey = invisible("</"+appendKey+">")
		text = text[:text.index(closeKey)] + appends[appendKey] + text[text.index(closeKey):]

	br.form['message'] = text
	#if __name__=="__main__":
	br.submit()
	print "Update sent"
	time.sleep(5)
	

def invisible(text):
	return "[color=#1b1c1f]" + text + "[/color]"

def quotePost(post, text):
	return "[QUOTE=" + post.name + ";" + str(post.postId) +"]" + text + "[/QUOTE]\n"

def renderDifference(oldvalue, newvalue, swap=False):
	difference = oldvalue - newvalue if swap else newvalue - oldvalue
	if oldvalue == -1:
		return " ([color=DeepSkyBlue]?[/color])"
	if difference > 0:
		return " ([color=palegreen]+%d[/color])" % (difference)
	if difference < 0:
		return " ([color=orange]%d[/color])" % (difference)
	return ""

	
def getAdjustedPostCountForUser(user):
	postCount = int(config['users'][user]['postCount'])
	if user in config['topposters']['postcountadjustments']:
		postCount = postCount + int(config['topposters']['postcountadjustments'][user])
	return postCount
	
def getTopPosterChart():
	message = '\n[B][SIZE="4"]Random Charts:[/SIZE][/B]\n\n'
	users = config['users'].keys()
	users.sort(key=lambda x: -1*getAdjustedPostCountForUser(x))
	users = [user for user in users if user != "SweetieBot - Lothranis"]
	topusers = users[:150]
	xvals = ",".join(["%.2f" %(float(getAdjustedPostCountForUser(user)) / float(config['users'][user]['totalDays'])) for user in topusers])
	yvals = ",".join(["%.2f" %(float(config['users'][user]['analyzed words'])/float(config['users'][user]['analyzed posts'])) for user in topusers])
	url = chartApiWordsVsPostsScatter + xvals + "|"+yvals
	message += "[img]%s[/img]\n" % (getPieChartForPosters())
	message += "[img]%s[/img]\n" % (url)
	return message 
	
def getPieChartForPosters():
	servers = {}
	for user in config['users']:
		fields = user.split(" - ")
		server = fields [1] if len(fields) > 1 else "None"
		servers[server] = servers.get(server, 0) + 1 #int(config['users'][user]['postCount'])
	serverNames = servers.keys()
	labelField = "|".join([urllib.quote(name) for name in serverNames])
	forumData = ','.join([str(servers[name]) for name in serverNames])
	return chartApiPieServers % (labelField, forumData)

def getWeeklyPosterChart(weeklyPosts):
	users = weeklyPosts.keys()
	users.sort(key=lambda x: -1*weeklyPosts[x])
	users = users[:20]
	names = "|".join([name.replace(' ', '+') for name in users[::-1]])
	postdata = ",".join([str(weeklyPosts[user]) for user in users])
	url = chartApiWeeklyTopPosters % (names,postdata)
	return "[img]%s[/img]\n" % (url)

def getTopPosterMessage(oldRanking={}):
	print "doing Top Poster message"
	users = config['users'].items()
	users.sort(key=lambda x: -1*getAdjustedPostCountForUser(x[0]))
	topusers = users[:TOP_USER_COUNT]	
	otherusers = users[TOP_USER_COUNT:] #add in admins not in top 100
	topusers.extend([user for user in otherusers if (user[1]['admin'] != '0')])
	message = ""
	
	message += '\n[B][SIZE="4"]PWI All-time Top Forum Posters:[/SIZE][/B]\n\n'
	newUserCount = 0
	weeklyPosts = {}
	
	def decoratePostCount(user):
		message = str(getAdjustedPostCountForUser(user))
		if user in config['topposters']['postcountadjustments']:
			message = "[color='turquoise']"+message+"[/color]"
		return message
	
	for i,user in enumerate(topusers):
		oldrank = oldRanking.get(user[0], [-1,-1])[0]
		oldposts = oldRanking.get(user[0], [-1,-1])[1]
		if i == TOP_USER_COUNT: 
			newUserCount = 0
		if oldrank == -1:
			newUserCount += 1
		else:
			weeklyPosts[user[0]] = getAdjustedPostCountForUser(user[0]) - oldposts
			oldrank += newUserCount
		
		message +="[b]%s)[/b] %s:%s " % (i+1, decorateName(user[0]), renderDifference(oldrank, i+1, True)) 
		message += "[color=white]%s[/color]" % (getCharacterDescription(user[0]))
		message += "\n[color=#1b1c1f]----[/color]"
		message += " Posts: [url=%s]%s[/url]%s," % (baseurl+"showthread.php?p="+user[1]['samplePost'], decoratePostCount(user[0]), renderDifference(oldposts, getAdjustedPostCountForUser(user[0])))
		message += " Join Date: [color=white]%s[/color]," % (user[1]['joinDate'])
		message += " Last Post: [color=white]%s[/color]," % (datetime.datetime.strptime(user[1]['lastPostDate'], "%Y-%m-%d %H:%M:%S").strftime("%b %Y"))
		message += " Favorite Forum: [color=white]%s[/color]" % (user[1]['favorite forum'])
		message += "\n[color=#1b1c1f]----[/color]"
		message += " Words/Post: [color=white]%.1f[/color]," % (float(user[1]['analyzed words'])/float(user[1]['analyzed posts'])) 
		message += " Posts/Day: [color=white]%.1f[/color]," % (float(getAdjustedPostCountForUser(user[0]))/float(user[1]['totalDays'])) 
		message += " Favorite Word: [color=white]%s[/color]\n" % (user[1]['favorite word'].replace("#", "'"))
	message += getTopPosterChart()
	if len(weeklyPosts):
		message += getWeeklyPosterChart(weeklyPosts)
	message += "\nLast Updated: " + str(getToday()) 
	return message
		

def getCharacterForAvatar(avatar):
	classes = {"Archer" : "A([FM])", "BM" : "B([FM])", "Barb" : "B([LPTW])", "Cleric": "C([FM])", "Assassin" : "([FM])A", "Psychic" : "([FM])P", "Mystic" : "M([FM])", "Seeker" : "S([FM])", "Wiz" : "W([FM])", "Veno" : "V([ACF]|B[au])"}
	for name in classes:
		match = re.match(classes[name] + "([0-9]+)", avatar)
		if match:
			sex = 'female'
			if match.group(1) == "M" or name == "Barb":
				sex = 'male'
			return name, sex, match.group(2)
	return "WtF", avatar

def getCharacterDescription(user):
	if config['users'][user]['avatar']: 

		character = getCharacterForAvatar(config['users'][user]['avatar'])
		sexicon = {'male': "[color=lightblue]&#9794;[/color]", 'female': "[color=lightpink]&#9792;[/color]"}
		return character[2] + " " + character[0] + " " +sexicon[character[1]]
	return ""

def getThreadStats(threadid):
	print "thread id is", threadid
	stats = {"threadid":threadid, "users": {}, "posts": 0}
	page = 1
	maxPage = 1
	
	posttext = ""
	dates = []
	while page <= maxPage:
		print "Loading thread", threadid, "page", page
		html = htmlOpen(showarchivethreadurl + threadid + "-p-" + str(page) +".html")
		soup = BeautifulSoup(html, "html5lib")
		users = soup.findAll("div", {"class" : "username"})
		if len(users) == 0:
			return stats
		for user in users:
			stats["users"][user.text.strip()] = stats["users"].get(user.text.strip(),0) + 1
			stats["posts"] += 1
		tags = soup.findAll("div", {"class":"posttext"})
		posttext += "\n".join([getTextContentForTag(tag) for tag in tags])
		
		dates.extend([datetime.datetime.strptime(date.text.strip(), "%m-%d-%Y, %I:%M %p") for date in soup.findAll("div", {"class" : "date"})])
		if page == 1:
			stats['title'] = soup.find('p', {"class":"largefont"}).find('a').text.strip()
		tag = soup.find("div", {"id":"pagenumbers"})
		if type(tag) != type(None):
			maxPage = int(tag.findAll("a")[-1].text.strip())
		page += 1
	stats['startdate'] = dates[0]
	stats['enddate'] = dates[-1]
	def toSeconds(delta):
		return float(delta.days*86400+delta.seconds)
	timedifference = toSeconds(dates[-1] - dates[0])
	normalizedDates = [toSeconds(date - dates[0])/timedifference for date in dates]
	buckets = max(min(100, stats['posts']/10), min(10, stats['posts']))
	activity = [0]*buckets
	for value in normalizedDates:
		activity[int(value*(len(activity) - 1))] += 1
	stats['activity'] = activity
	stats['textanalysis'] = textanalyzer.calcStats(posttext)
	return stats
	
def getMessageForThreadStats(stats):
	startdate = stats['startdate']
	enddate = stats['enddate']
	age = (enddate - startdate).days
	message = "[b]"+config['botname'] + "[/b] has finished reading the thread: [b][url="+showthreadurl%(stats['threadid'],1)+"]"+stats['title']+"[/url][/b]!\n\n"
	message += "[b]General Stats:[/b]\n"
	message += "First Post: [color=white]%s[/color]\n" % (startdate.strftime("%m-%d-%Y"))
	message += "Last Post: [color=white]%s[/color]\n" % (enddate.strftime("%m-%d-%Y"))
	message += "Thread Lifetime: [color=white]%d days[/color]\n" % (age + 1)
	message += "Total Posts: [color=white]%d[/color]\n" % (stats['posts'])
	message += "Average Posts Per Day: [color=white]%.1f[/color]\n\n" % (float(stats['posts'])/float(age + 1))
	
	message += "[b]Activity[/b]:\n"
	message += "[url][img]%s[/img]Thread Activity[/url]\n\n" % (chartApiThread + ",".join([str(a) for a in stats['activity']])) 
	
	users = stats['users'].items()
	users.sort(key=lambda x: -x[1])
	message += "[b]Top "+str(min(20,len(users)))+" Frequent Posters (count):[/b]\n"
	message += "\n".join(["%s ([color=white]%d[/color])" % item for item in users[:20]]) + "\n\n"
	results = stats['textanalysis']
	message += "[b]Writing Stats:[/b]\n"
	message += "Total Words: [color=white]%d[/color] \n" % (results['words'])
	message += "Total Sentences: [color=white]%d[/color] \n" % (results['sentences'])
	message += "Average Words per Post: [color=white]%5.1f[/color]\n" % (float(results['words'])/float(stats['posts']))
	message += "Average Words per Sentence: [color=white]%5.1f[/color]\n" % (float(results['words'])/float(results['sentences']))
	message += "Average Sentences per Post: [color=white]%5.1f[/color]\n" % (float(results['sentences'])/float(stats['posts']))
	message += "Average Syllables per Word: [color=white]%5.1f[/color]\n" % (float(results['syllables'])/float(results['words']))
	message += "Average Letters per Word: [color=white]%5.1f[/color]\n" % (float(results['characters'])/float(results['words']))
	message += "\n"
	message += "[b]Most Used Words (count): [color=gray](common words excluded)[/color][/b]\n"
	imageCloud = maketagcloud.getImageCloudForText(results['favoritewords0'])
	message += "[url][img]%s[/img]Word Cloud[/url]\n" % (imageCloud)
	message += "\n".join(["%s ([color=white]%d[/color])" % (word[0], word[1]) for word in results['favoritewords0'][:10]]) + "\n"
	
	for i in range(3):
		message += "\n[b]Most Used "+str(i+3)+"-Word Phrases (count):[/b]\n"
		message += "\n".join(['"%s ([color=white]%d[/color])"' % (word[0], word[1]) for word in results['favoritewords'+str(i+2)][:3]])
	
	return message
	
def doAnalyzeThreadErrorReply(post, command, title, threadid): 
	message = config['botname'] + " couldn't find the thread you're talking about :(\n"
	if len(threadid):
		message += "Is the thread's id really: '"+ threadid +"'?\n"	
	if len(title):  
		message += "Is the thread's title really: '"+ title +"'?\n"
	message += "You should try typing either: \n'" +config['botname']+ " analyze this thread' or \n'" \
		+config['botname']+ " analyze thread <Thread Title>' or\n'" \
		+config['botname']+ " analyze thread <Thread ID>'"
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)	
	return

def analyzeThreadCommand(post, command, args):
	print "ANALYZE THREAD from " , post.name, post.postId, command, ":", args
	starttime = time.time()
	threadid = ""
	title = ""
	if args.startswith("this thread"):
		threadid = post.getThreadId()
	else:
		match = re.search("(?:the )?thread +([0-9]+)", args)
		if match:
			threadid = match.group(1)
		if not match or int(threadid < 300):
			match = re.search("(?:the )?thread (.*)", args)
			if match:
				title = match.group(1).strip()
				print "Searching thread title", title
				results = searchForThreadByTitle(title)
				if len(results) > 0:
					threadid = results[0].threadId
	
	if len(threadid) == 0:
		doAnalyzeThreadErrorReply(post, command, title, threadid)
		return
	stats = getThreadStats(threadid)
	if len(stats['users']) == 0:
		try:
			refpost = Post(threadid)
			threadid = refpost.getThreadId()
			stats = getThreadStats(threadid)
		except:
			doAnalyzeThreadErrorReply(post, command, title, threadid)
			return
		
		
	message = getMessageForThreadStats(stats)
	message += "\n\n This took me [color=white]%5.1f[/color] s to finish" % (time.time() - starttime)
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)
	
def getPieChartForForumPosting(forumItems):
	sortedItems = forumItems[:]
	sortedItems.sort(key=lambda x: -1*x[1])
	labelField = "|".join([urllib.quote(item[0]) if item in sortedItems[:10] else '' for item in forumItems])
	labelField = labelField.replace("%20", "+")
	forumData = ','.join([str(item[1]) for item in forumItems])
	return chartApiPieForums % (labelField, forumData)
	
def getAnalyzeStats(target, subforum=''):
	result = getTextForName(target, subforum, True)
	if result['postCount'] != 0:
		target = result['post'].name
		result['textanalysis'] = textanalyzer.calcStats(result['textSample'])
		forums = result['postByForum'].keys()
		forums.sort(key=lambda x: -1*result['postByForum'][x])
		totalDays = (result['lastPostDate'].date() - datetime.datetime.strptime(result['post'].joinDate, "%b %Y").date()).days + 1	
		if target not in config['users']:
			config['users'][target] = {}
		favWord = "?"
		if result['textanalysis']['favoritewords0']:
			favWord = result['textanalysis']['favoritewords0'][0][0].replace("'", "#").replace('"', "#")
			if favWord == config['botname'].lower():
				favWord = result['textanalysis']['favoritewords0'][1][0].replace("'", "#").replace('"', "#")
			
		print "Finished for", target, result['post'].postCount
			
		config['users'][target]['samplePost'] = result['post'].postId
		config['users'][target]['analyzed posts'] = result['postCount']
		config['users'][target]['favorite word'] = favWord
		config['users'][target]['favorite forum'] = forums[0]
		config['users'][target]['analyzed words'] = result['textanalysis']['words']
		config['users'][target]['postCount'] = int(result['post'].postCount.replace(',',''))
		config['users'][target]['lastScanPostCount'] = config['users'][target]['postCount']
		config['users'][target]['joinDate'] = result['post'].joinDate
		config['users'][target]['lastPostDate'] = str(result['lastPostDate'])
		config['users'][target]['totalDays'] = totalDays	
		config['users'][target]['admin'] = result['post'].admin
		config['users'][target]['avatar'] = result['post'].avatar  
		config.write()
		return result
	return False
	

def analyzeCommand(post, command, args):	
	print "GOT COMMAND TO ANALYZE from " , post.name, post.postId, command, ":", args
	starttime = time.time()
	possessive = "your"
	if args.startswith("me"):
		target = post.name
	elif re.search("^(this |the )?thread", args.strip(), re.IGNORECASE):
		analyzeThreadCommand(post, command, args)
		return
	else:
		target = args.strip()
		target = re.sub("[,.?;!]+.*$", "", target)
		target = re.sub(" (but )?(only|not).*$", "", target)
		possessive = target + "'s"
	if len(target) == 0:
		message = "Umm, exactly who did you want " + config['botname'] + " to analyze?"
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return
	subforum = ''
	match = re.search("(?: but)? (only |not )(?:for|in) (?:forum )?([^,.?;!]+)(?:\s*$|[,.?;!])", args, re.MULTILINE)
	if match:
		subforum = match.group(1) + match.group(2)
		print "SUBFORUM:", subforum

	#	samplePost, postCount, postByHour, text = getTextForName(target)
	target = target.strip()
	print "EXTRACTING TEXT FOR", target
	fixedName = re.search("\s*(\S+(?: - (Sanctuary|Archosaur|Lost City|Heavens Tear|Dreamweaver|Harshlands|Raging Tide|Momaganon|Lothranis|Morai))?)", target, re.IGNORECASE).group(1)
	if fixedName != target:
		print "Something fishy?", fixedName, target
		
	result = getAnalyzeStats(fixedName, subforum)
	if not result:
		message = config['botname'] + " couldn't find any posts belonging to '"+target+"' :(\nCan you try again with their exact name please?\n"
		if len(subforum):
			message +=  "Also, is the forum really supposed to be '%s'?\n" % (subforum)
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return

	target = result['post'].name
	if possessive != 'your':
		possessive = decorateName(target)+"'s"
	postingHourUrl = chartApiHour + ",".join([str(x) for x in result['postByHour']])
	postingWeekdayUrl = chartApiWeekday + ",".join([str(x) for x in result['postByWeekday']])
	postingForumUrl = getPieChartForForumPosting(result['postByForum'].items())

	totalDays = (result['lastPostDate'].date() - datetime.datetime.strptime(result['post'].joinDate, "%b %Y").date()).days + 1

	imageCloud = maketagcloud.getImageCloudForText(result['textanalysis']['favoritewords0'])
	
	subforumMessage = ''
	if len(subforum): 
		if subforum.lower().startswith('not '):
			subforumMessage = " in forums other than " + subforum[4:] #"not subforum"
		else:
			subforumMessage = " in forum " + subforum[5:] #"only subforum"
	
	message = "[b]"+config['botname'] + " has read "+possessive+" last "+str(result['postCount'])+" posts"+subforumMessage+"![/b]\nHere's some neat stuff "+config['botname']+" has learned.\n\n"
	message += "[b]General Stats:[/b]\n"
	message += "Forum name: [color=white]%s[/color]\n" % (target)
	message += "Join Date: [color=white]%s[/color]\n" % (result['post'].joinDate)
	message += "Last Post Date: [color=white]%s[/color]\n" % (result['lastPostDate'].strftime("%m-%d-%Y"))
	message += "Total Posting Days: [color=white]%d[/color]\n" % (totalDays)
	message += "Total Posts: [color=white]%s[/color]\n" % (result['post'].postCount)
	message += "Average Posts per Day: [color=white]%.1f[/color]\n\n" % (float(result['post'].postCount.replace(',',''))/float(totalDays))
	message += "[b]Activity:[/b]\n"
	message += "[url][img]%s[/img]Posting By Hour Chart[/url]\n" % (postingHourUrl) 
	message += "[url][img]%s[/img]Posting By Day Chart[/url]\n" % (postingWeekdayUrl) 
	if len(result['postByForum']) > 1:
		message += "[url][img]%s[/img]Posting By Subforum Pie Chart[/url]\n\n" % (postingForumUrl) 

	message += "[b]Writing Stats (what "+config['botname']+" read):[/b]\n"
	message += "Total Words: [color=white]%d[/color] \n" % (result['textanalysis']['words'])
	message += "Total Sentences: [color=white]%d[/color] \n" % (result['textanalysis']['sentences'])
	message += "Average Words per Post: [color=white]%5.1f[/color]\n" % (float(result['textanalysis']['words'])/float(result['postCount']))
	message += "Average Words per Sentence: [color=white]%5.1f[/color]\n" % (float(result['textanalysis']['words'])/float(result['textanalysis']['sentences']))
	message += "Average Sentences per Post: [color=white]%5.1f[/color]\n" % (float(result['textanalysis']['sentences'])/float(result['postCount']))
	message += "Average Syllables per Word: [color=white]%5.1f[/color]\n" % (float(result['textanalysis']['syllables'])/float(result['textanalysis']['words']))
	message += "Average Letters per Word: [color=white]%5.1f[/color]\n" % (float(result['textanalysis']['characters'])/float(result['textanalysis']['words']))
	message += "\n"
	message += "[b]Most Used Words (count): [color=gray](common words excluded)[/color][/b]\n"
	message += "[url][img]%s[/img]Word Cloud[/url]\n" % (imageCloud)
	message += "\n".join(["%s ([color=white]%d[/color])" % (word[0], word[1]) for word in result['textanalysis']['favoritewords0'][:10]]) + "\n"
	
	for i in range(3):
		message += "\n[b]Most Used "+str(i+3)+"-Word Phrases (count):[/b]\n"
		message += "\n".join(['"%s ([color=white]%d[/color])"' % (word[0], word[1]) for word in result['textanalysis']['favoritewords'+str(i+2)][:3]])
	
	message += "\n\n This took me [color=white]%5.1f[/color] s to finish" % (time.time() - starttime)

	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)



MAX_DAILY_POINTS = 30
MAX_POINT_REWARD = 10
MAX_NEG_DAILY_POINTS = 5
MAX_NEG_POINT_REWARD = 2
MIN_REQUIRED_POSTCOUNT = 50

def ordinal(value):
	val = value % 100
	suffix = 'th'
	if val in [11, 12, 13]:
		suffix = 'th'
	elif val % 10 == 1:
		suffix = 'st'
	elif val % 10 == 2:
		suffix = 'nd'
	elif val % 10 == 3:
		suffix = 'rd'
	return str(value) + suffix

def isValidUser(name):
	if len(name) == 0:
		return False
	if name in config['points']['alltime']['scorelist'] or name in config['users']:
		return name
	postResults = findPostsByName(name, exactname=False)
	if postResults:
		for result in postResults:
			if result.name != postResults[0].name:
				return False
		return postResults[0].name
	return False

def getPointUsage(name, target=''):
	if int(config['points']['usage']['date']) != dayCount():
		config['points']['usage']['date'] = dayCount()
		config['points']['usage']['users'] = {}
	if not name in config['points']['usage']['users']:
		config['points']['usage']['users'][name] = [0, 0]
	return [int(x) for x in config['points']['usage']['users'][name]]

#	if not target in config['points']['usage']['users'][name]:
#		config['points']['usage']['users'][name][target] = {}
#	return [int(x) for x in config['points']['usage']['users'][name][target]]

def getMultiUsers(target, noMulti=False):
	target = re.sub("[.?;!]+.*$", "", target.strip()).strip()
	target = re.sub("\s+(for|because|cause|so)\s.*$", "", target)

	message = ""
	items = re.split(' and |,', target)
	if noMulti:
		items = items[:1]
	names = []
	for item in items:
		match = re.search("\s*(?:and\s+)?(\S+(?: - (?:Sanctuary|Archosaur|Lost City|Heavens Tear|Dreamweaver|Harshlands|Raging Tide|Momaganon|Lothranis|Morai))?)", item, re.IGNORECASE)
		if match:
			name = isValidUser(match.group(1))
			if not name:
				message += "Umm, is '"+match.group(1)+"' really the right name for this?\nTry using their exact name with server." if len(target) > 0 else "Umm, whom did you want to give points to?\n"
			else:
				names.append(name)
	return message, names
				

def rewardPointsCommand(post, command, args):
	print "Got Reward Points Command", command, args
	points = re.search("([0-9]+)\s+points?", command, re.IGNORECASE).group(1)
	message = ""
	target = ""
	match = re.search("[0-9]+\s+points?\s+((?:away )?from|off|to)\s+(.*)", command, re.IGNORECASE)
	print command, match
	isNegative = False
	if match:
		isNegative = match.group(1).lower().endswith('from') or match.group(1).lower().endswith('off') 
		target = match.group(2)
	else:
		match = re.search("(?:give|grant|award|reward|add)\s+(\S.+)\s+[0-9]+\s+points?", command, re.IGNORECASE)
		if not match:
			message = "I'm having problems figuring out whom to give points to :(\nIt's not you it's me."
			reply = quotePost(post, command) + decorate(message)
			doReply(post.postId, reply)
			return
		target = match.group(1)
			
	message, names = getMultiUsers(target, noMulti=post.admin == '0')
	print "Names are:", names	
	if len(message) > 0:
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return
	
	target = names[0]
	if names[0] == post.name and post.admin == '0':
		message = "Why would you want to do that anyway? :( Seek help!" if isNegative else "Nice try! You can't give points to yourself!"
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return
	elif int(post.postCount) < MIN_REQUIRED_POSTCOUNT and post.admin == '0':
		message = "Aww sorry but you need to have at least 50 posts to be able to award points."
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return		
	try:
		points = int(points.replace(",", ""))
		print "Points is now %d" %(points)
	except:
		message = "Sorry but "+config['botname']+" can't figure out how many points that is :(\nNo weird numbers please! Do 1-10"
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return
	usage = getPointUsage(post.name, names[0])
	if ((isNegative and usage[1] >= MAX_NEG_DAILY_POINTS) or ((not isNegative) and usage[0] >= MAX_DAILY_POINTS)) and post.admin == '0':
		message = "Sorry but you've already reached your daily limit for that.  Just wait until tomorrow."
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return
	print "Points is ", points, isNegative, names, usage
	
	maxAllowedPoints = min(MAX_POINT_REWARD, MAX_DAILY_POINTS - usage[0])
	maxAllowedNegPoints = min(MAX_NEG_POINT_REWARD, MAX_NEG_DAILY_POINTS - usage[1])

	def pointStr(value, color='white', size=''):
		pointval = "point" if value*value == 1 else "points"
		text = str(value)
		if size:
			text = "[size="+str(size)+"]"+text+"[/size]"
		text = "[color="+color+"]"+text+"[/color] " + pointval
		return text

	if not isNegative and points > maxAllowedPoints and post.admin == '0':
		if maxAllowedPoints == MAX_POINT_REWARD:
			message = "You are limited to awarding only %s per request.\n" % (pointStr(MAX_POINT_REWARD))
		else:
			message = "You only had %s left to award for today.\n" % (pointStr(maxAllowedPoints))
		points = maxAllowedPoints

	if isNegative and points > maxAllowedNegPoints and post.admin == '0':
		if maxAllowedNegPoints == MAX_NEG_POINT_REWARD:
			message = "You can't remove more than %s per request.\n" % (pointStr(MAX_NEG_POINT_REWARD))
		else:
			message = "You only had %s left to remove for today.\n"% (pointStr(maxAllowedNegPoints))
		points = maxAllowedNegPoints

	delta = [0, points] if isNegative else [points, 0]
	config['points']['usage']['users'][post.name] = [usage[0] + delta[0], usage[1] + delta[1]]
	
	for name in names:
		config['points']['alltime']['scorelist'][name] = int(config['points']['alltime']['scorelist'].get(name, 0)) + delta[0] - delta[1]
		config['points']['monthly']['scorelist'][name] = int(config['points']['monthly']['scorelist'].get(name, 0)) + delta[0] - delta[1]

		if isNegative:
			message += "%s removes %s from %s!\n" % (decorateName(post.name), pointStr(points, color='orange', size='4'), decorateName(name))
		else:
			message += "%s awards %s to %s!\n" % (decorateName(post.name), pointStr(points, color='palegreen', size='4'), decorateName(name))
		message += "%s is now in [color=white]%s[/color] place for [url=%s]%s[/url] with %s (%s [url=%s]overall[/url]).\n" % \
			(decorateName(name), 
			getRankForName(name, 'monthly'),
			showthreadurlforpost + config['points']['monthly']['postId'], 
			config['points']['monthly']['month'],
			pointStr(config['points']['monthly']['scorelist'][name]), 
			pointStr(config['points']['alltime']['scorelist'][name]),
			showthreadurlforpost + config['points']['alltime']['postId'])
	
	if post.admin == '0':
		pointsLeft = [MAX_DAILY_POINTS - getPointUsage(post.name)[0], MAX_NEG_DAILY_POINTS -  getPointUsage(post.name)[1]]
		if not isNegative:
			if pointsLeft[0] > 0:
				message += "%s can still award another %s today.\n" % (decorateName(post.name), pointStr(pointsLeft[0]))
			else:
				message += "%s can't award any more points until tomorrow.\n" % (decorateName(post.name))
		else:
			if pointsLeft[1] > 0:
				message += "%s can still remove another %s today.\n" % (decorateName(post.name), pointStr(pointsLeft[1]))
			else:
				message += "%s can't remove any more points until tomorrow.\n" % (decorateName(post.name))			

	if int(config['points']['postId']) > 0:
		message +="\nCheck [url=%s]this thread[/url] for the current [color=white]high scores[/color] and to learn how to award points to others." % (showthreadurlforpost + config['points']['postId'])

	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

	updateRewardPoints()

def getRankForName(name, listname='alltime'):
	users = getSortedPointsUsers(listname)
	index = users.index(name)
	return ordinal(index + 1)

def getSortedPointsUsers(listname='alltime'):
	users = config['points'][listname]['scorelist'].keys()
	users.sort(key=lambda x: int(config['points'][listname]['scorelist'][x])*-1)
	return users
	
def updateRewardPoints():
	if int(config['points']['monthly']['postId']) > 0:
		updatePost(config['points']['monthly']['postId'], {
			"MONTHLY" : getTopPointsMessage(config['points']['monthly']['scorelist'], title="%s PWI Forum High Scores" % config['points']['monthly']['month'])})
	if int(config['points']['alltime']['postId']) > 0:
		updatePost(config['points']['alltime']['postId'], {
			"SCORES" : getTopPointsMessage(config['points']['alltime']['scorelist'], title="All-Time PWI Forum High Scores")})
			
def doMonthlyPointsReset():
	print "Doing Monthly Points Reset"
	message = getTopPointsMessage(config['points']['monthly']['scorelist'], 
		title="%s PWI Forum High Scores" % config['points']['monthly']['month'])
	postId = doReply(config['points']['postId'], decorate(message))
	users = getSortedPointsUsers('monthly')
	winner = "%s ([color=white]%d[/color])" % (decorateName(users[0]), int(config['points']['monthly']['scorelist'][users[0]])) if users else 'nobody'
	updatePost(config['points']['monthly']['postId'], appends={ 
		"PREVIOUS" : "\n[url=%s]%s PWI Forum High Scores[/url] - winner: %s" % (showposturl+postId, config['points']['monthly']['month'], winner)})
	config['points']['monthly']['month'] = getServerDateTime().strftime("%B %Y")
	config['points']['monthly']['scorelist'] = {}
	config.write()

def getTopPointsMessage(scorelist, title="PWI Forum High Scores", limit=-1):
	if limit == -1:
		limit = len(scorelist)
	users = scorelist.keys()
	users.sort(key=lambda x: int(scorelist[x])*-1)
	message = '\n[B][SIZE="4"][color=white]%s:[/color][/SIZE][/B]\n\n' % title
	for i,user in enumerate(users[:limit]):
		message +="%d) %s ([color=white]%d[/color])\n" % (i+1, decorateName(user), int(scorelist[user])) 
	return message

def getPromoCodesMessage():
	message = "\n"
	codelist = config['code']['codelist']
	codes = codelist.keys()
	codes.sort(key = lambda x: codelist[x]['expires'])
	
	current = []
	expired = []
	
	for code in codes[::-1]:
		days = 1000
		if codelist[code]['expires']:
			days = (datetime.datetime.strptime(codelist[code]['expires'], "%Y-%m-%d") - datetime.datetime.now()).days
		print code, days
		if days < 0:
			if days < 700:
				expired.append((code,days))
		else:
			current.append((code,days))
	
	def messageForCode(code, codelist, expired):
		expirationMessage = invisible("---- ") + ("Expired" if expired else "Expires")
		expirationMessage += " on %s" % codelist[code]['expires'] if codelist[code]['expires'] else " on ????"
		result = "[color=%s][b]%s[/b][/color] - [color=white]%s[/color]\n%s Added by %s on %s" %('cyan' if not expired else 'pink',
			code, 
			codelist[code]['item'],
			expirationMessage,
			decorateName(codelist[code]['author']),
			codelist[code]['addedon'])
		return result + "\n"
	
	if len(current) > 0:
		message += "[b][SIZE=4]Current Code List[/size][/b]\n\n"		
		for code in current:
			message += messageForCode(code[0], codelist, False)
		
	if len(expired) > 0:
		message += "\n\n[color=pink][b]Recently Expired Code List[/b][/color]\n\n"	
		for code in expired:
			message += messageForCode(code[0], codelist, True)
	return message


def promoCodeCommand(post, command, args):
	print "Got Promo Code Command", command,"-", args
	match = re.search ('(?:modify|add) +code +(.{8}) +for +(?:a |the )?(.+?)(?: +which +expires +on +([0-9\-/]+))?$', command)
	errorMessage = "Please use this exact command:\n"
	errorMessage += "Sweetiebot add code <CODE> for <ITEM(s)> [which expires on YYYY-MM-DD]\n"
	errorMessage += "[color=white]Example[/color]: Sweetiebot add code 75HtYCE6 for a Jones Blessing which expires on 2016-01-01"
	message = ""
	if not match:
		message = "Can't quite understand that :( " + errorMessage
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return		
	code = match.group(1)
	item = match.group(2)
	if re.search('expir', match.group(2)):
		message = "There's some issue with the expiration, it needs to say 'which expires on' :(\n" + errorMessage
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return	
	date = match.group(3) 
	date = date if date else ""
	if date:
		try:
			datetime.datetime.strptime(date, "%Y-%m-%d")
		except:
			message = "The date has to be ISO-8601 format, YYYY-MM-DD\n" + errorMessage
			reply = quotePost(post, command) + decorate(message)
			doReply(post.postId, reply)
			return	
	author = post.name
	print 'code is '+'|'.join((code,item,date,author))
	if int(post.postCount.replace(',', '')) < int(config['code']['minpostcount']):
		message = "Sorry but you need to have at least %s posts to be able to set codes" % config['code']['minpostcount']
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return		
	
	if code in config['code']['codelist']:
		message += "This changed an existing code.\nThis can be undone with: [color=white]Sweetiebot modify code %s for %s%s[/color]\n" % (
			code,
			config['code']['codelist'][code]['item'],
			(" which expires on [color=white]%s[/color]"%config['code']['codelist'][code]['expires']) if config['code']['codelist'][code]['expires'] else ""
			)
	
	config['code']['codelist'][code] = {}
	config['code']['codelist'][code]['item'] = item	
	config['code']['codelist'][code]['expires'] = date
	config['code']['codelist'][code]['author'] = author
	config['code']['codelist'][code]['addedon'] = getPostTime(post.time).date()
	
	if int(config['code']['postId']) > 0:
		updatePost(config['code']['postId'], {"CODES" : getPromoCodesMessage()})
	
	message = "Added code [color=cyan]%s[/color] - [color=white]%s[/color]%s!\n\n" %(code, item, (" which expires on [color=white]%s[/color]"%date) if date else "") + message
	message += "If this code is expired or not valid remove it with:\n[color=white]Sweetiebot remove code %s[/color]" % code
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def removeCodeCommand(post, command, args):
	print "Got Remove Code Command", command,"-", args

	if int(post.postCount.replace(',', '')) < int(config['code']['minpostcount']):
		message = "Sorry but you need to have at least %s posts to be able to remove codes" % config['code']['minpostcount']
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		return	
	
	code = args.split(' ')[0]
	if code in config['code']['codelist']:
		codeValue = config['code']['codelist'][code] 
		config['code']['codelist'].pop(code, None)
		message = "Removing promo code [color=cyan]%s[/color]\n" % code
		message += "If this was a mistake and you can confirm the code is still valid this can be undone with:\n[color=white]Sweetiebot add code %s for %s%s[/color]" % (code,
			codeValue['item'],
			(" which expires on " + codeValue['expires']) if codeValue['expires'] else '')
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
		
		if int(config['code']['postId']) > 0:
			updatePost(config['code']['postId'], {"CODES" : getPromoCodesMessage()})
	else:
		message = "I don't think %s is a code, maybe it was already removed or expired?" % code
		reply = quotePost(post, command) + decorate(message)
		doReply(post.postId, reply)
	
def doChat(name, message):
	bots = [ChatterBotType.PANDORABOTS, ChatterBotType.JABBERWACKY, ChatterBotType.CLEVERBOT]
	
	annoyingPhrases = ["Pardon me?", "What are you talking about?", "Please explain", "I would like to talk about", "I am bored", "I don't understand",  "I do not understand"]
	
	for bot in bots:
		try:
			session = getChatSessionForName(name, bot)
			reply = session.think(message)
			if bot == ChatterBotType.PANDORABOTS or bot == ChatterBotType.JABBERWACKY:
				annoying = False
				for phrase in annoyingPhrases:
					if reply.find(phrase) != -1:
						annoying = True
						break
				if annoying:
					continue
			if bot == ChatterBotType.CLEVERBOT:
				reply = reply.replace("Cleverbot", config['botname']).replace("cleverbot", config['botname'])
			reply = re.sub('<[^<]+?>', '', reply) #strip HTML
			return reply
		except:
			continue
	return "Sorry, I'm having trouble talking at the moment :("

def getChatSessionForName(name, bottype=ChatterBotType.PANDORABOTS):
	key = str(bottype) + name
	if key in settings.chatbotSessions:
		return settings.chatbotSessions[key]
	else:
		keys = settings.chatbotSessions.keys()
		if len(keys) > 7:
			del settings.chatbotSessions[keys[0]]
			del settings.chatbotSessions[keys[1]]
		session = chatBots[bottype].create_session()
		print "MAKING NEW SESSION for", name, bottype, key
		settings.chatbotSessions[key] = session
		return session

def askBotCommand(post, command):
	print "matching", command
	text = re.search("^\s*" + config['botname'] + "\W*\s*(.*)$", command, re.IGNORECASE | re.MULTILINE)
	print "ASKING CHATBOT ", text.group(1)
	reply = doChat(post.name, text.group(1))
	if not reply:
		reply = "Something's wrong and I can't talk good at the moment :("
	
	if len(reply) < 5:
		reply += invisible("(5char)")
	
	reply = quotePost(post, command) + decorate(reply)
	doReply(post.postId, reply)
	
def checkServerStatusCommand(post, command, args):
	servers, message = getServerStatusMessage()
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def getServerStatusMessage():
	#Simply change the host and port values
	servers = [("Sanctuary (PVE)", "pwigc2.perfectworld.com"), 
		("Heaven's Tear (PVE)", "pwigc4.perfectworld.com"), 
		("Lost City (PvP)", "pwigc3.perfectworld.com"),
		("Archosaur (PvE)", "pwiwest4.perfectworld.com"),
		("Harshlands (PvP)", "pwieast1.perfectworld.com"),
		("Dreamweaver (PvE)", "pwieast2.perfectworld.com"),
		("Raging Tide (PvE)", "pwieast3.perfectworld.com"),
		("Morai (PvE)", "pwieu3.en.perfectworld.eu")
	]
	port = 29000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	number_servers_up = 0
	server_message = []
	for server in servers:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1.5)
			milli = int(round(time.time() * 1000))
			s.connect((server[1], 29000))
			milli = int(round(time.time() * 1000)) - milli
			data = s.recv(100) #during maint is only 51 bytes
			s.shutdown(2)
			number_servers_up += 1
			server_message.append("[B]"+server[0] +"[/B] [color=gray](" + server[1] +")[/color]: [color=Lime]ONLINE[/color] (Ping: " + str(milli) +"ms)")
		except:
			server_message.append("[B]"+server[0] +"[/B] [color=gray](" + server[1] +")[/color]: [color=RED]OFFLINE[/color]")
			
	message = "Here's the server status:\n\n[B][color=white]West Coast Servers:[/color][/B]\n" + "\n".join(server_message[:4]) + "\n\n"
	message += "[B][color=white]East Coast Servers:[/color][/B]\n" + "\n".join(server_message[4:7]) + "\n\n"
	message += "[B][color=white]European Servers:[/color][/B]\n" + "\n".join(server_message[7:]) + "\n"
	
	return number_servers_up, message
	

def checkForMorePatches(url):
	patchurl = "http://pwi-ns.perfectworld.com/patches/manual/ec_patch_"
	result = ""
	
	SCANRANGE = 20
	
	match = re.search("ec_patch_([0-9]+)-([0-9]+)", url)
	if not match:
		return result
	currentPatch = int(match.group(2))
	
	while True:
		for i in range(1,SCANRANGE+1):
			testurl = "%s%d-%d.cup" % (patchurl, currentPatch, currentPatch+i)
			print "checking##", testurl
			try:
				response = br.open(testurl)
				result = [response.info().getheader("Content-length"), testurl]
				currentPatch = currentPatch+i
				break
			except:
				if i == SCANRANGE:
					return result
			
	return result
		
def findManualPatchCommand(post, command, args):
	message = getFindManualPatchMessage()
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def getFindManualPatchMessage(forMaint=False):
	#return "With the new website layout I'm not sure where to find the manual patch these days, that's something I need to figure out."
	"""html = htmlOpen(techsupportUrl)
	soup = BeautifulSoup(html, "html5lib")
	patchLinks = soup.findAll("a", href=re.compile('perfectworld\.com/patches/manual'))
	patchLinks.sort(key=lambda link: int(re.search('([0-9]+)-',link.text).group(1)))
	currentPatchLink = patchLinks[-1]
	print 'found patch url', currentPatchLink['href']
	
	currentpatch = currentPatchLink['href']
	patchText = currentPatchLink.text.strip()
	results = searchForThreadByTitle('patch', False, 'only Cabbage Patch Notes');
	curVersion = re.search('Patch Notes.*?([0-9]+)', results[0].title).group(1)
	oldVersion = re.search('Patch Notes.*?([0-9]+)', results[1].title).group(1)
	currentpatch = "http://pwi-ns.perfectworld.com/patches/manual/ec_patch_"+oldVersion+"-"+curVersion+".cup"""
	techsupportUrl = 'http://pwi-forum.perfectworld.com/forumdisplay.php?f=142'
	currentpatch = config['maintenance']['currentPatch']
	patchText = "Patch %s" % (re.search("([0-9]+-[0-9]+)", currentpatch).group(0))
	nextpatch = checkForMorePatches(currentpatch)
	message = ''
	if nextpatch == "":
		if forMaint:
			message = "There doesn't seem to be any new manual patch for this maintenance.\nAt least not yet."
		else:
			message = 'The latest manual patch is here: [URL="'+currentpatch+'"]'+patchText+"[/URL]\n"
			message += "This is the newest one that's [URL="+techsupportUrl+"]officially listed[/URL] and I don't see anything newer."
	else:
		patchText = "Patch " + re.search("([0-9]+-[0-9]+)", nextpatch[1]).group(0)
		size = nextpatch[0]
		message = 'The latest manual patch appears to be: [URL="%s"]%s[/URL] %.1fMB (%s bytes)\n' % (nextpatch[1], patchText, float(size)/1048576.0, size)
		if int(size) < 5000000:
			message += "It is weirdly small for some reason. \n\n"
		elif int(size) < 19000000:
			message += "That's average-sized. \n\n"
		elif int(size) < 35000000:
			message += "It is somewhat bigger than average. \n\n"
		else:
			message += "Wow this thing is big! \n\n"
		message += "This patch hasn't been [URL="+techsupportUrl+"]officially listed[/URL] yet."
		
		if forMaint:
			config['maintenance']['currentPatch'] = nextpatch[1]
			config.write()
		 
	return message	
	
def decorate(chatText):
	return '[COLOR="Silver"]' + chatText + '[/COLOR]'

def decorateName(name):
	if name in config['users'] and config['users'][name]['admin'] == '2':
		return "[color='turquoise'][b]%s[/b][/color]" % (name) 
	if name in config['users'] and config['users'][name]['admin'] == '3':
		return "[color='red'][b]%s[/b][/color]" % (name) 
	return "[b]%s[/b]" % (name)

def showMeCommand(post, command, args):
	print "Doing image search for", args
	image = imageSearch(args)
	reply = quotePost(post, command)
	if image == '':
		reply += decorate(config['botname'] + " has no idea what you're talking about.")
	else:
		reply += decorate("Sure, no problem.\n\n" )
		reply += "[url][img]%s[/img]Image of %s[/url]" % (image, args)
	
	doReply(post.postId, reply)

def requestDeniedReply(post, command, args):
	message = "Hey that's an admin-only request.  "+config['botname']+" doesn't have to listen to you!"
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def isBeingIgnored(user):
	if user in config['ignorelist']:
		if float(config['ignorelist'][user]) == -1 or time.time() < float(config['ignorelist'][user]):
			return True
		else:
			del config['ignorelist'][user]
	return False
	
def strFromTimeStamp(timestamp):
	timestamp = float(timestamp)
	if timestamp == -1:
		return 'forever'
	return datetime.datetime.strftime(datetime.datetime.fromtimestamp(timestamp, PST), "%m-%d-%Y, %I:%M %p")

def addToIgnoreCommand(post, command, args):
	if post.admin == '0':
		requestDeniedReply(post, command, args)
		return
	print "Gonna ignore", args
	
	message = ''
	#if re.search('this +thread|thread +[0-9]+', args):
	#	
	#else:
	message, users = getMultiUsers(args)
	expiration = -1
	match = re.search(' +for +([0-9]+) +days?', args)
	if match:
		days = int(match.group(1))
		expiration = time.time() + days*24*3600
	for user in users:
		message += "Sure thing!  I'll be ignoring %s from now until %s.\n" % (user, strFromTimeStamp(expiration))
		config['ignorelist'][user] = expiration
	config.write()
	reply = quotePost(post, command) + decorate(message)
	print reply
	doReply(post.postId, reply)

def removeFromIgnoreCommand(post, command, args):
	if post.admin == '0':
		requestDeniedReply(post, command, args)
		return
	print "Gonna unignore", args
	message, users = getMultiUsers(args)
	for user in users:
		if isBeingIgnored(user):
			message += "Anything you say!  I'm removing " + user + " from my ignore list.\n"
			del config['ignorelist'][user]
			config.write()
		else:
			message += "Hmm, are you sure I was ignoring " + user + "?  Maybe their ignore already expired...\n"
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)
	
def listIgnoreCommand(post, command, args):
	if post.admin == '0':
		requestDeniedReply(post, command, args)
		return
	print "Gonna list ignores"
	message = "I am ignoring the following trolls:\n\n"
	for user in config['ignorelist']:
		if isBeingIgnored(user):
			message += "%s until %s\n" % (user, strFromTimeStamp(config['ignorelist'][user]))
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def startTalkingCommand(post, command, args):
	if post.admin == '0':
		requestDeniedReply(post, command, args)
		return
	message = "Yay! Sweetiebot is so happy now! Being quiet is no fun at all :("
	config['quietmode'] = 'False'
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def beQuietCommand(post, command, args):
	if post.admin == '0':
		requestDeniedReply(post, command, args)
		return
	print "got bequiet", post.admin, args
	
	expiration = -1
	match = re.search('for +([0-9]+) +hours?', args)
	if match:
		hours = int(match.group(1))
		expiration = time.time() + hours*3600
	
	message = "Aww ok, you're the boss! I'll be quiet from now until %s.\n If you find it in yourself to forgive me just tell me 'you can start talking again'" % strFromTimeStamp(expiration)
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)
	config['quietmode'] = 'True'
	config['quietmodeexpiration'] = expiration
	config.write()
	
def pokerCommand(post, command, args):
	reply = quotePost(post, command) + decorate(poker.getPokerMessage())
	doReply(post.postId, reply)
	
def annoyingPostingLocationMessage(post, threadId):
	if not post.forumId:
		post.getThreadId()
	if post.forumId == "4":  #General Discussion
		return "[color=white][b]Please consider posting requests like this in [url=%s]this thread[/url] instead of in General Discussion.[/b][/color]\n\n" % (showthreadurl % (threadId, "99999"))
	return ""
	
def doRestrictedLocationPost(post, command, message, threadId, newLocationPostId):
	header = quotePost(post, command)
	reply = header + decorate(message)
	
	if post.getThreadId() != threadId:
		postid = doReply(newLocationPostId, reply)
		redirectMessage = "[url=%s]Here is where I posted the result.[/url]\nPlease use that thread for future requests like this.\n" % (showthreadurlforpost + postid)
		redirectReply = header + decorate(redirectMessage)
		doReply(post.postId, redirectReply)
	else:
		doReply(post.postId, reply)

def packCommand(post, command, args):
	pack = re.sub("[.?!]+.*$", "", args.strip()).strip().lower()
	pack = re.sub("\s+(for|because|if|cause|so)\s.*$", "", pack)
	pack = re.sub("\s+(please).*$", "", pack)
	pack = re.sub("pack((?:s|age| s| c| b| a)?).*$", "pack\\1", pack)
	match = re.search("([0-9,]+) (.+)", pack)
	message = ''
	quantity = 1
	try:
		if match:
			quantity = int(match.group(1).replace(',', ''))
			packname = match.group(2)
			print "Quantity,pack", quantity, packname
			if quantity > 10000:
				message = "You can only open up to 10000 packs at a time.\n"
				quantity = 10000	
			if quantity < 1:
				message = "You should open up at least 1 pack.\n"
				quantity = 1
			message += pwdb.getOpenPackMessage(packname, quantity)
		else:
			message += "Open what exactly?  You have to say it like:\n "+config['botname']+" open 1000 Anniversary Packs"
	except URLError:
		message = config['botname'] + " thinks [url]http://pwdatabase.com[/url] is down at the moment. :(\n Try again later."
	
	doRestrictedLocationPost(post, command, message, config['pwdbspamthread'], config['pwdbspampost'])

def farmCommand(post, command, args):
	args = re.sub("[.?!]+.*$", "", args.strip()).strip().lower()
	args = re.sub("\s+(for|because|if|cause|so)\s.*$", "", args)
	args = re.sub("\s+(please).*$", "", args)
	bonusDrop = 1
	match = re.search("(?:during|on|in) ([0-9]+)x", args)
	bonusDrop = int(match.group(1)) if match else 1
	match = re.search("([^0-9]+)(?:([0-9]+) +times?)?", args)
	playerlevel = int(getCharacterForAvatar(post.avatar)[2]) if post.avatar else 0
	message = ''
	try:
		if match:
			quantity = int(match.group(2).replace(',', '').strip()) if match.group(2) else 1
			mobname = match.group(1).strip()
			print "Quantity,name,level", quantity, mobname, playerlevel
			if quantity > 10000:
				message = "You can only kill the mob 10000 times per request.\n"
				quantity = 10000	
			if quantity < 1:
				message = "You should kill the mob at least once.\n"
				quantity = 1
			if bonusDrop > 10:
				message += "Don't you think 10x is enough?  Don't go crazy!"
				bonusDrop = 10
			message += pwdb.getMobKillMessage(mobname, quantity, playerlevel, bonusDrop)
		else:
			message += "Farm which mob exactly?  You have to say it like:\n "+config['botname']+" farm Twilight Emperor: Vacuity 1000 times"
	except URLError:
		message = config['botname'] + " thinks [url]http://pwdatabase.com[/url] is down at the moment. :(\n Try again later."
	
	doRestrictedLocationPost(post, command, message, config['pwdbspamthread'], config['pwdbspampost'])

	
def forgeCommand(post, command, args):
	print "Got FORGE comamnd", args
	if not args: 
		args = ''
	gear = re.sub("[.?!+]+.*$", "", args.strip()).strip().lower()
	gear = re.sub("\s+(for|because|if|cause|so)\s.*$", "", gear)
	gear = re.sub("\s+(please).*$", "", gear).strip()
	gear = re.sub("^a ", "", gear).strip()
	message = ''
	try:
		if len(gear):
			message += pwdb.rollGear(gear, post.name.split()[0])
		else:
			message += "Where's the name of the gear you want to forge?  You have to say it like:\n "+config['botname']+" forge a Traceless Dimension"
	except URLError:
		message = config['botname'] + " thinks [url]http://pwdatabase.com[/url] is down at the moment. :(\n Try again later."
	
	doRestrictedLocationPost(post, command, message, config['pwdbspamthread'], config['pwdbspampost'])

	
def catsCommand(post, command, args):
	print "Got CATS comamnd", args
	message = cats.getCatMessage()
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def wolframAlphaCommand(post, command, args):
	print "Got Wolfram comamnd", command, args
	match = re.search("(?:what|where|who|when|how).*", command, re.IGNORECASE)
	if match:
		text = match.group(0)
		text = re.sub("what(?: +is|\'?s)", "", text)
		message = wa.getWolframAlphaMessage(text)
	else:
		message = ""
	if not message.strip():
		askBotCommand(post, command)
		return
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)
	
def doTag(isPost, color, note, post):
	colorMessage = ""
	noteMessage = ""
	if color: 
		colorMessage = " as " + color.lower() 
	else: 
		color = "default"
	if note: noteMessage = "\n[i]Note: " + note + "[/i]"
	thread = Thread(post.getThreadId())
	if not isPost:
		url = showthreadurl % (str(thread.threadId), '1')
	else:
		url = showposturl + str(post.postId)
	message = "\n\n[url=%s]%s[/url]" % (url, thread.title)
	message += "\nTagged by %s on %s" % (decorateName(post.name), str(getPostTime(post.time))) + noteMessage
	
	print "C: %s N: %s M: %s" % (color, note, message)
	
	tagPostList = Post(config['tagtrackpost'])
	if tagPostList.text.find("<tag-"+color+">") == -1:
		tagCategory = invisible("<tag-"+color+">") + "\n\n[color=white]Tag: [color=%s]%s[/color][/color]" % (color,color.upper())
		tagCategory += invisible("</tag-"+color+">")
		doAppendReply(config['tagtrackpost'], decorate(tagCategory))
	
	updatePost(config['tagtrackpost'], appends={"tag-"+color: message})
	
	return "This %s has been [url=%s]tagged[/url]" % ("post" if isPost else "thread", showthreadurlforpost + config['tagtrackpost']) + colorMessage + noteMessage

def untagCommand(post, command, args):
	print "Got untag request", command, args
	if post.admin == '0'  and post.name != 'heero200':
		requestDeniedReply(post, command, args)
		return
	message = "The untag command is not ready at the moment"
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def tagCommand(post, command, args):
	print "Got tag request", command, args
	if post.admin == '0' and post.name != 'heero200':
		requestDeniedReply(post, command, args)
		return
	match = re.search('(post|thread)(?: +as +([^ ]+))?(?: +with +note[;:-]* *(.+))?', args, re.IGNORECASE)
	print match.groups()
	if match:
		isPost = (match.group(1).lower() == 'post')
		color = match.group(2).lower() if match.group(2) else ""
		note = match.group(3) if match.group(3) else ""
		message = doTag(isPost, color, note, post)
	else:
		message = "Error in command :(, the correct format for this is:\n [color=white]Sweetiebot tag this (post|thread) [as (color)] [with note (message)][/color]"
	print message
	reply = quotePost(post, command) + decorate(message)
	doReply(post.postId, reply)

def scanPostForCommand(post):
	print "scanning Post", post.postId
	if post.name.startswith(config['botname']) or (isBeingIgnored(post.name) and post.admin == '0'):
		return False

	text = post.text
	print baseurl + "showthread.php?p=" + str(post.postId) +" : "+post.name+"\n"+ text
	commands = [  
		('(?:modify|add) +code +(?:.{8}) +for +(?:a |the )?(?:.+?)(?: +which +expires +on +(?:[0-9\-/]+))?$', promoCodeCommand),
		('remove +code +', removeCodeCommand),
		('analy[sz]e', analyzeCommand),
		('show me(?: +an? +(?:image|picture) +of)?', showMeCommand),
		('(?:what +is|where +is|find)(?: +the)? +(?:manual +|latest +)+patch', findManualPatchCommand),
		('(?:what +is|what\'?s|report|display|update|show|tell|check)(?: +me)?(?: +the)? +server +status', checkServerStatusCommand),
		('ignore', addToIgnoreCommand),
		('(?:unignore|stop +ignoring)', removeFromIgnoreCommand),
		('(?:be +quiet|stop +talking)', beQuietCommand),
		('who +are +you +ignoring', listIgnoreCommand),
		('you +can +start +talking +again', startTalkingCommand),
		('(?:give|take(?: +away)?|remove|subtract|deduct|award|grant|reward|add)? *[0-9]+ +points? +(?:to|(?:away )?from|off)', rewardPointsCommand),
		('(?:give|award|reward|add|grant) +\S.+ +[0-9]+ +points?', rewardPointsCommand),
		('deal +me', pokerCommand),
		('open(?: +me)?', packCommand),
		('(?:forge|reforge|craft|manufacture)(?: +me)?(?: +a +)?', forgeCommand),
		('(?:farm|kill)(?: +me)?', farmCommand),
		('(?:tell|talk|i +want +to +know)(?: +to)?(?: +me)? +(?:about +cats|(?:a +)?cat +facts?)', catsCommand),
		('(?:what(?: +is|\'?s)?|where|when|who|how +(?:many|much))', wolframAlphaCommand),
		('tag this', tagCommand),
		('untag this', untagCommand)
	]
	keys = [x[0] for x in commands]
	regex = "^\s*" + config['botname'] + "[^a-z0-9\n]* *(?:can you |will you |please |pl[sz] |could you |would you |won't you )*("+"|".join(keys)+"|\S*)[.;!?,]*? *([^ \n].*)?"
	
	found = 0
	for match in re.finditer(regex, text, re.IGNORECASE | re.MULTILINE):
		found += 1
		matched = False
		isPWDB = False
		print "Found",match.groups()
		for command in commands:
			if re.match(command[0], match.group(1), re.IGNORECASE):
				matched = True
				if config['quietmode'] == 'True' and command[1] != startTalkingCommand and post.admin == '0':
					continue
				command[1](post, match.group(0), match.group(2))
				isPWDB = command[1] in [packCommand, forgeCommand, farmCommand]		
				break
		if not matched and config['quietmode'] != 'True':
			askBotCommand(post, match.group(0))
		if post.admin == '0' and ((isPWDB and found >= 5) or (not isPWDB and found >= 2)):
			break
	
	return found > 0

def doMaintenanceReply(post):
	message = "First non-human reply!\n\n"
	manPatchMessage = getFindManualPatchMessage(True)
	message += manPatchMessage
	print post.text
	questionMatch = re.search("^(.*\?)", post.text, re.MULTILINE)
	if questionMatch:
		question = questionMatch.group(1)
		message += quotePost(post, question)
		message += doChat(post.name, question)
		
	reply = decorate(message)
	#print reply
	doReply(post.postId, reply)

def getServerDateTime():
	return datetime.datetime.now(PST)

def getToday():
	return getServerDateTime().date()

def dayCount():
	return (getToday() - datetime.date.min).days
	
def getThreadResults(html):
	soup = BeautifulSoup(html, "html5lib")
	tags = soup.find('table', id='threadslist').findAll('tr')
	threads = [makeThreadResultFromTag(tag) for tag in tags if re.search("showthread.php\\?(s=.+?&amp;)?t=",str(tag))]
	return threads

def getRecentThreads():
	threadResults = []
	address = getdailythreadurl
	nextPageLink = address
	while nextPageLink != '':
		html = htmlOpen(address)
		threadResults.extend(getThreadResults(html))
		if settings.recentThreadId == 0:
			nextPageLink = getNextPageLinkFromSearchPage(html)
			address = nextPageLink
			#address = proxybaseurl + urllib.quote(nextPageLink)
		else:
			break
		break #Just do first page for now
	return threadResults

def checkThreadForNecro(threadResult):
	if threadResult.postCount == 1:
		return False
	threadPage = threadResult.getFullThread(-1)
	print "checking reply", threadResult.threadId, threadResult.postCount - 2, len(threadPage.posts)
	secondToLast = (threadResult.postCount - 2) % 10
	#forum sometimes has bad postcounts
	if secondToLast < len(threadPage.posts):
		post = threadPage.posts[secondToLast]
	else:
		post = threadPage.posts[-1]
	postDate = getPostTime(post.time)
	timeDiff = threadResult.lastPost.postDate - postDate
	print "Checked thread",threadResult.threadId, "for Necro", timeDiff
	return timeDiff
	
def checkForNecros():
	print "Checking for Necros", settings.recentThreadId
	recentThreads = getRecentThreads()
	recentThreads.sort(key=lambda x: -int(x.threadId))
	settings.recentThreadId = recentThreads[0].threadId
	for thread in recentThreads:
		if int(settings.recentThreadId) - int(thread.threadId) < 8000 \
			or (thread.threadId in settings.notNecroThreads and (datetime.datetime.now() - settings.notNecroThreads[thread.threadId]).days < 30) \
			or thread.isSticky \
			or thread.forum in ['Quality Corner', 'The Fanatics Forum', 'Screenshots & Videos'] \
			or thread.author == thread.lastPost.name \
			or (thread.lastPost.name in config['users'] and config['users'][thread.lastPost.name]['admin'] != '0'):
			settings.notNecroThreads[thread.threadId] = thread.lastPost.postDate
			continue
		else:
			timeDiff = checkThreadForNecro(thread)
			if timeDiff.days > 61:
				doNecroReply(thread.lastPost.postId, timeDiff, thread.lastPost.postDate)
			settings.notNecroThreads[thread.threadId] = thread.lastPost.postDate

def doNecroReply(postId, timeDiff, lastPostDate):
	print "Doing Necro Reply!", postId, timeDiff
	post = Post(postId)
	relDiff = relativedelta.relativedelta(lastPostDate, lastPostDate - timeDiff)
	def numMessage(num, word):
		if num == 0: return ""
		if num == 1: return "1 " + word + " "
		return str(num) + " " + word + "s "

	message = "This looks like a [color=cyan]NECRO[/color]!\n\n" 
	message += post.name + " replied to a message that was "
	message += "".join([numMessage(x[0], x[1]) for x in [(relDiff.years, 'year'), (relDiff.months, 'month'), (relDiff.days, 'day'), (relDiff.hours, 'hour'), (relDiff.minutes, 'minute')]])
	message += "old.\n\nAny thread over one month (30 days) old is considered to be a dead thread and you're not supposed to post in them.  The person you are replying to probably doesn't care any more or can no longer be found on the forums.  The topic itself could be out of date.  Next time just make a new thread."
	message = quotePost(post, post.text) + decorate(message)
	doReply(postId, message)

def doSubForumSelection(subforum):
	if len(subforum):
		notToken, subforumName = re.search("(not|only) ?(.*)",subforum.strip(),re.IGNORECASE).groups()
		reverse = notToken.lower() == 'not'
		control = br.form.find_control(name="forumchoice[]")
		forums = []
		print "Doing search in",reverse,subforumName
		for item in control.get_items():
			if item.name in ['0', 'subscribed']:
				continue
			itemText = item.get_labels()[0].text.strip()
			if reverse and not re.search(subforumName.strip(), itemText, re.IGNORECASE):
				forums.append(item.name)
			elif not reverse and re.search(subforumName.strip(), itemText, re.IGNORECASE):
				forums.append(item.name)
		br.form["forumchoice[]"] = forums
		print "Subforum list",forums

def searchForThreadByTitle(title, doQuote=True, subforum=''):
	# Add quotes if needed
	title = '"%s"' % title if doQuote else title
	# Forum bug requires you to html escape these characters
	title = title.replace("&", '&amp;').replace('<', '&lt;').replace('>', '&rt;')
	br.open(searchurl)
	br.select_form("vbform")
	#The added random numbers force a cache miss!
	br.form['query'] = title + " " + str(random.randint(0,999)) + " " + str(random.randint(0,999))
	br.form['titleonly'] = ['1']
	doSubForumSelection(subforum)
	response = br.submit()
	#threadIds = getThreadIdsFromSearchPage(response.read())
	results = getThreadResults(response.read())
	return results

def searchForMaintenanceThread():
	results = searchForThreadByTitle("Maintenance", False)
	print "Scanning maintenance thread minid is", config['maintenance']['threadId']
	for result in results:
		threadId = result.threadId
		if int(threadId) > int(config['maintenance']['threadId']):
			print "Found new maintenance thread mention!"
			maintThread = Thread(threadId)
			if maintThread.posts[0].admin != '0':
				config['maintenance']['threadId'] = int(threadId)
				config['maintenance']['postId'] = int(maintThread.posts[0].postId)
				config['maintenance']['status'] = 'pending'
				config['maintenance']['date'] = dayCount()
				config.write()
				doMaintenanceReply(maintThread.posts[0])

def checkMaintenanceServerStatus():
	servers, message = getServerStatusMessage()
	print "Maint thread up. Checking server status", config['maintenance']['status'], servers
	reply = ""
	if config['maintenance']['status'] == "pending" and servers == 0:
		reply = "The servers are now down! Everyone start panicking!\nOhh wait, this happens every maintenance.\n\n" +message
		config['maintenance']['status'] = "down"
		config.write()
	elif config['maintenance']['status'] == "down" and servers == 8:
		reply = config['botname'] + " can confirm the servers are back up! Yay!\n\n" + message
		config['maintenance']['status'] = "complete"
		config.write()
	if reply != "":
		print "Making reply!"
		maintThread = Thread(config['maintenance']['threadId'])	
		doReply(maintThread.posts[0].postId, decorate(reply), appendAble=False)
		

def searchForCommand():
	if config['quietmode'] == 'True' and time.time() < float(config['quietmodeexpiration']):
		config['quietmode'] = 'False'
	
	br.open(searchurl)
	br.select_form("vbform")
	#The added random numbers force a cache miss
	br.form['query'] = config['botname'] + " " + str(random.randint(0,999)) + " " + str(random.randint(0,999))
	br.form['showposts'] = ['1']
	response = br.submit()
	postIds = getPostIdsFromSearchPage(response.read())[::-1]
	print "Scanning posts minID is", config['minPostId']
	updated = False
	for postId in postIds:
		if int(postId) > int(config['minPostId']):
			print "Found New Post", postId, config['minPostId']
			post = Post(postId)
			updated |= scanPostForCommand(post)
			setMinPostId(postId)
	return updated

def updateLastPostForUser(user, samplePost=None):
	postResult = findPostByName(user)
	if postResult:
		if not samplePost:
			samplePost = postResult.getFullPost()
		registerLastPost(samplePost)
	else:
		print "CAN'T FIND AN UPDATE FOR USER:", user
		
def registerLastPost(post):
	config['users'][post.name]['postCount'] = post.postCount
	config['users'][post.name]['samplePost'] = post.postId
	config['users'][post.name]['avatar'] = post.avatar
	config['users'][post.name]['lastPostDate'] = str(getPostTime(post.time))
	totalDays = (getPostTime(post.time).date() - datetime.datetime.strptime(post.joinDate, "%b %Y").date()).days + 1	
	config['users'][post.name]['totalDays'] = totalDays
		

def updateTopPosters():
	print "Updating Top Posters (shallow scan)"
	topposters = config['users'].keys()
	topposters.sort(key = lambda user: -1*int(config['users'][user]['postCount']))
	updateLimit = int(1.5*TOP_USER_COUNT)
	OLD = getTopPosterOldRanking()
	for user in topposters[:updateLimit] + [user for user in topposters[updateLimit:] if config['users'][user]['admin'] != '0']:
		try:
			samplePost = Post(config['users'][user]['samplePost'])
			if config['users'][user]['postCount'] != samplePost.postCount:
				updateLastPostForUser(user)
			elif user in OLD and int(config['users'][user]['postCount']) != OLD[user][1]:
				updateLastPostForUser(user)
		except:
			print "Deleted?", user, config['users'][user]['samplePost']
			updateLastPostForUser(user)
		if int(config['users'][user]['postCount']) - int(config['users'][user]['lastScanPostCount']) > 300:
			config['usersToAnalyze'][user] = int(config['users'][user]['postCount'])
	
	topposters.sort(key = lambda user: -1*int(config['users'][user]['postCount']))
	setAnalyzePostThreshhold()
	message = getTopPosterMessage(getTopPosterOldRanking())
	updatePost(config['topposters']['postId'], {"CONTENT": message})
	message = '[B][SIZE="4"]Weekly Update:[/SIZE][/B]\n' + message
	doReply(config['topposters']['postId'], decorate(message), appendAble=False)
	#for user in topposters[updateLimit:]:
	#	if config['users'][user]['admin'] == '0' and int(config['users'][user]['postCount']) < 1000:
	#		del config['users'][user] #clean up scrubs
	config['topposters']['scandate'] = dayCount()
	updateWeeklyPostCounts()
	config.write()	

def updateWeeklyPostCounts():
	for user in config['users']:
		config['users'][user]['weeklyPostCount'] = config['users'][user]['postCount']

def updateTopPosterRanks():
	allPosters = config['users'].keys()
	allPosters.sort(key = lambda user: -1*int(config['users'][user]['postCount']))
	updateLimit = int(1.5*TOP_USER_COUNT)
	settings.allTimeTopPosters = allPosters[:updateLimit] 
	settings.minPostCountAllTime = int(config['users'][settings.allTimeTopPosters[-1]]['postCount'])
	#[user for user in allPosters[updateLimit:] if config['users'][user]['admin'] != '0']
	def isRecent(user):
		userPostDate = datetime.datetime.strptime(config['users'][user]['lastPostDate'], "%Y-%m-%d %H:%M:%S").date()
		return (getToday() - userPostDate).days < ACTIVE_USER_DAY_LIMIT
	settings.activeTopPosters = [user for user in allPosters if isRecent(user)][:220]
	settings.minPostCountActive = max(int(config['users'][settings.activeTopPosters[-1]]['postCount']), 300)
	
	
def setAnalyzePostThreshhold():
	topposters = config['users'].keys()
	topposters.sort(key = lambda user: -1*int(config['users'][user]['postCount']))
	updateLimit = int(1.5*TOP_USER_COUNT)
	config['topposters']['lowpostcount'] = config['users'][topposters[:updateLimit][-1]]['postCount']
	
def getTopPosterOldRanking():
	text = Post(config['topposters']['postId']).text
	updateKey = "CONTENT"
	openKey = "<"+updateKey+">"
	closeKey = "</"+updateKey+">"
	text = text[text.index(openKey) + len(openKey): text.index(closeKey)]
	oldScoreList = re.findall("(\d+)\)\s+([^:]+?)\s*:.*?----\s+Posts:\s+(\d+)", text, re.DOTALL | re.MULTILINE)
	oldScores = {}
	for item in oldScoreList:
		oldScores[item[1]] = (int(item[0]), int(item[2]))
	return oldScores

def setMinPostId(postId):
	config['minPostId'] = int(postId)
	config.write()

def handleTopPosters():
	if dayCount() - int(config['topposters']['scandate']) >= 7:
		temp = config['quietmode']
		config['quietmode'] = 'False'
		updateTopPosters()
		config['quietmode'] = temp

def handleAwardPointsMonthly():
	if config['points']['monthly']['month'] != getServerDateTime().strftime("%B %Y"):
		temp = config['quietmode']
		config['quietmode'] = 'False'
		doMonthlyPointsReset()
		updateRewardPoints()
		config['quietmode'] = temp

def handleMaintenance():
	if dayCount() - int(config['maintenance']['date']) > 5:
		searchForMaintenanceThread()
		time.sleep(5)
		if getToday().weekday() == 1 and getServerDateTime().hour >= 11:
			settings.sleeptime = min(settings.sleeptime, 180)
	if dayCount() - int(config['maintenance']['date']) <= 2  and config['maintenance']['status'] in ["pending", "down"]:
		checkMaintenanceServerStatus()
		time.sleep(5)
		settings.sleeptime = min(settings.sleeptime, 240) 
	else:
		config['maintenance']['status'] == "complete"

def handleCommands():
	if searchForCommand():
		settings.sleeptime = 0
	time.sleep(5)

def handleNecros():
	checkForNecros()
	time.sleep(5)

def handleUserUpdate():
	if len(config['usersToAnalyze']):
		users = config['usersToAnalyze'].keys()
		users.sort(key=lambda x: int(config['usersToAnalyze'][x]))
		settings.spiderSearch = True
		print "User", users[-1], "of", len(users), "=", config['usersToAnalyze'][users[-1]]
		if int(config['usersToAnalyze'][users[-1]]) > settings.minPostCountActive:
			print "Running ANALYZE", users[-1], len(config['usersToAnalyze']), users
			getAnalyzeStats(users[-1])
		config['usersToAnalyze'].pop(users[-1])
		config.write()
		settings.sleeptime = 20
		settings.spiderSearch = False
		#setAnalyzePostThreshhold()
		updateTopPosterRanks()

init()
if len(config['usersToAnalyze']) == 0:
	config['usersToAnalyze'] = {}

if __name__=="__main__":
	logging.basicConfig(level=logging.DEBUG, filename='sweetieboterr.log', format='%(asctime)s %(levelname)s %(message)s', filemode='w')
	if config['maintenance']['status'] == "down":
		if getServerStatusMessage()[0] == 8:
			config['maintenance']['status'] == "complete"
	settings.testMode = False
	print 'TestMode is',settings.testMode
	while True:
		try:
			handleAwardPointsMonthly()
			handleTopPosters()
			handleMaintenance()
			handleNecros()
			handleCommands()
			handleUserUpdate()	
			print "Sleeping for ", settings.sleeptime
			time.sleep(settings.sleeptime)
			settings.sleeptime = min(settings.sleeptime + 20, MAX_SLEEP_INTERVAL)
		except Exception as e:
			print "ERRORERRORERROR got", e
			logging.exception("Got error")
			time.sleep(420)
