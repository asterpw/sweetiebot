#!/usr/bin/python
from sweetiebot import *
import time
import datetime
import re
import random
import sys

url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fpwi-forum.perfectworld.com%2Fshowthread.php%3Ft%3D1585581%26page%3D836%22&diagnostics=true"


post = Post(22369071)
#print post.getThreadId()
#print Thread(post.getThreadId()).title
#post.text = 'Sweetiebot add code 75HtYCE6 for a Jones Blessing which expires on 2016-05-01'

scanPostForCommand(post)
exit()
post.text = 'Sweetiebot add code asdfasdf for a Jones Blessing which expires on 2015-05-01'

scanPostForCommand(post)
post.text = 'Sweetiebot add code fdasfdas for a Jones Blessing which expires on 2016-01-01'

scanPostForCommand(post)
post.text = 'Sweetiebot add code EXPIREDD for a Jones Blessing which expires on 2014-01-01'
scanPostForCommand(post)
post.text = 'Sweetiebot add code dsfddddd for a Omalley'

scanPostForCommand(post)
post.text = 'Sweetiebot remove code fdasfdas'

scanPostForCommand(post)
sys.exit()
#html = htmlOpen(url)

#soup = BeautifulSoup(html, "html5lib")
#tag = soup.find("div",{"class": "bigusername"})
#print tag

#checkForNecros()

results = searchForThreadByTitle('patch', False, 'only Cabbage Patch Notes');
print results
print results[0].title
for result in results:
	print "hmm", result.title
curVersion = re.search('Patch Notes.*?([0-9]+)', results[0].title).group(1)
oldVersion = re.search('Patch Notes.*?([0-9]+)', results[1].title).group(1)
print curVersion
linkAddress = "http://pwi-ns.perfectworld.com/patches/manual/ec_patch_"+oldVersion+"-"+curVersion+".cup"
print linkAddress

#print getFindManualPatchMessage()

#scanPostForCommand(21508191)
#print getFindManualPatchMessage()
settings.spiderSearch = True
#scanPostForCommand(18778311)
settings.spiderSearch = False
#handleUserUpdate()
#handleUserUpdate()
#scanPostForCommand(18813611)
#scanPostForCommand(19523431)
#getRecentThreads()
#print getServerStatusMessage()
#print getFindManualPatchMessage()

#rewardPointsCommand(Post(18779191), 'give Asterelle 1 point', '')
#analyzeCommand(Post(18779191), "analyze", "me but not in Off-Topic Discussion")
#analyzeCommand(Post(18779191), "analyze", "this thread")
#print getTopPosterOldRanking()
#updateTopPosters()
#farmCommand(Post(18779191), "farm", "Blizzard King Effigy 100000 times please!")
#forgeCommand(Post(18779191), 'forge', 'a Firmament Bow, Adversity Daggers, and Requiem Magic Sword please.')
#config.write()
#print decorate(getTopPosterMessage(getTopPosterOldRanking()))
'''for user in config['users']:
	if 'avatar' not in config['users'][user] or not config['users'][user]['avatar']:
		samplePost = ''
		try:
			samplePost = Post(config['users'][user]['samplePost'])
		except:
			print "Deleted?", user, config['users'][user]['samplePost']
			postResult = findPostByName(user)
			if postResult:
				samplePost = postResult.getFullPost()
				config['users'][user]['samplePost'] = samplePost.postId
			else:
				print "CAN'T FIND AN UPDATE FOR USER:", user
		if samplePost:
			print samplePost.avatar
			config['users'][user]['avatar'] = samplePost.avatar
config.write()
'''


#getTopPosterMessage(getTopPosterOldRanking())
#doReply(18813171, )

#print getTopPosterChart()

#print re.search(regex, "SweetieBot -4 points from Quilue - Sanctuary", re.IGNORECASE).groups()
#scanPostForCommand(18829011)
#print Post(18748821).text
#getPartialPostsFromSearchPage(doSearch("Asterelle - Sanctuary", "Archer"))
#analyzeCommand(Post(18774501), 'analyze', 'me but only for forum Archer.')
#print Post(14739561).text
#print getTextForName("Asterelle - Sanctuary", True)

	
chartApiHour = "http://chart.googleapis.com/chart?chf=bg,s,1E1713&chxr=1,0,23&chxs=0,EFEFEF,12,0,lt,EFEFEF&chxt=x&chbh=a&chs=440x200&cht=bvg&chco=76A4FB&chtt=Posts+by+Hour&chts=EFEFEF,11.5&chds=a&chd=t:"

#result = getTextForName("Asterelle - Sanctuary")
'''
print chartApi + ",".join([str(x) for x in result['postByHour']])

chartApiHour = "http://chart.googleapis.com/chart?chf=bg,s,1E1713&chxr=1,0,23&chxs=0,EFEFEF,12,0,lt,EFEFEF&chxt=x&chbh=a&chs=440x200&cht=bvg&chco=76A4FB&chtt=Posts+by+Hour&chts=EFEFEF,11.5&chds=a&chd=t:"
chartAPIWeekday = "http://chart.googleapis.com/chart?chf=bg,s,1E1713&chxr=1,0,7&chxs=0,EFEFEF,12,0,lt,EFEFEF&chxt=x&chbh=a&chs=440x200&cht=bvg&chco=76A4FB&chtt=Posts+by+Day&chts=EFEFEF,11.5&chds=a&chxl=0:|Mon|Tue|Wed|Thu|Fri|Sat|Sun&chd=t:"
print chartAPIWeekday + ",".join([str(x) for x in result['postByWeekday']])
'''

#print getMessageForThreadStats(getThreadStats("1566451"))

#print decorate(getTopPosterMessage())

