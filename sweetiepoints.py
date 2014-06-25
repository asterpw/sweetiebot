#!/usr/bin/python
import re
import sweetiebot as sb

MAX_DAILY_POINTS = 30
MAX_POINT_REWARD = 10
MAX_NEG_DAILY_POINTS = 5
MAX_NEG_POINT_REWARD = 2
MIN_REQUIRED_POSTCOUNT = 50

def ordinal(value):
	val = value % 100
	suffix = ''
	if val in [11, 12, 13]:
		suffix = 'th'
	elif val % 10 == 1:
		suffix = 'st'
	elif val % 10 == 2:
		suffix = 'nd'
	elif val % 10 == 3:
		suffix = 'rd'
	else:
		suffix = 'th'
	return str(value) + suffix

def isValidUser(name):
	if len(name) == 0:
		return False
	if name in sb.config['points']['scorelist']:
		return True
	if sb.findPostId(name) != 0:
		return True
	return False
	
def getPointUsage(name):
	if int(sb.config['points']['usage']['date']) != sb.dayCount():
		sb.config['points']['usage']['date'] = sb.dayCount()
		sb.config['points']['usage']['users'] = {}
	if not name in sb.config['points']['usage']['users']:
		sb.config['points']['usage']['users'][name] = [0, 0]
	return [int(x) for x in sb.config['points']['usage']['users'][name]]

def rewardPointsCommand(post, command, args):
	print "Got Reward Points Command", command, args
	points = re.search("([0-9]+)\s+points?", command, re.IGNORECASE).group(1)
	target = re.sub("[,.?;!]+.*$", "", args.strip()).strip()
	target = re.sub(" for .*$", "", target)
	message = ""
	isNegative = re.search("[0-9]+\s+points?\s+(from|to)", command, re.IGNORECASE).group(1) == 'from'
	if not isValidUser(target):
		message = "Umm, is '"+target+"' really the right name for this?" if len(target) > 0 else "Umm, whom did you want to give points to?"
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return
	elif target == post.name:
		message = "Nice try! You can't give points to yourself!"
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return
	elif int(post.postCount.replace(',', '')) < MIN_REQUIRED_POSTCOUNT:
		message = "Aww sorry but you need to have at least 50 posts to be able to award points."
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return		
	try:
		points = int(points.replace(",", ""))
		print "Points is now %d" %(points)
	except:
		message = "Sorry but "+sb.BOTNAME+" can't figure out how many points that is :(\nNo weird numbers please! Do 1-10"
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return
	usage = getPointUsage(post.name)
	if ((isNegative and usage[1] == MAX_NEG_POINT_REWARD) or (not isNegative and usage[0] == MAX_POINT_REWARD)) and post.admin == '0':
		message = "Sorry but you've already reached your daily limit for that.  Just wait until tomorrow."
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return
	print "Points is ", points, isNegative, target, usage
	
	
	maxAllowedPoints = min(MAX_POINT_REWARD, MAX_DAILY_POINTS - usage[0])
	maxAllowedNegPoints = min(MAX_NEG_POINT_REWARD, MAX_NEG_DAILY_POINTS - usage[1])
	
	if not isNegative and points > maxAllowedPoints and post.admin == '0':
		if maxAllowedPoints == MAX_POINT_REWARD:
			message = "You are limited to awarding only " + str(MAX_POINT_REWARD) + " points per request!\n"
		else:
			message = "You only had " + str(maxAllowedPoints) + " points left to award today!\n"
		points = maxAllowedPoints
	
	if isNegative and points > maxAllowedNegPoints and post.admin == '0':
		if maxAllowedNegPoints == MAX_NEG_POINT_REWARD:
			message = "You can't remove more than "+str(MAX_NEG_POINT_REWARD)+" point!\n"
		else:
			message = "You only had " + str(maxAllowedNegPoints) + " point left to remove today!\n"
		points = maxAllowedNegPoints
	
	delta = [0, points] if isNegative else [points, 0]
	sb.config['points']['usage']['users'][post.name] = [usage[0] + delta[0], usage[1] + delta[1]]
	sb.config['points']['scorelist'][target] = int(sb.config['points']['scorelist'].get(target, 0)) + delta[0] - delta[1]
	
	def pointStr(value):
		text = "point" if value*value == 1 else "points"
		text = "[color=white]"+str(value)+"[/color] " + text
		return text
	if isNegative:
		message += "[b]%s[/b] removes [size=4]%s[/size] from [b]%s[/b]!\n" % (post.name, pointStr(points), target)
	else:
		message += "[b]%s[/b] awards [size=4]%s[/size] to [b]%s[/b]!\n" % (post.name, pointStr(points), target)
	message += "[b]%s[/b] now has a total of %s and is in %s place!\n" % (target, pointStr(sb.config['points']['scorelist'][target]), getRankForName(target))
	if post.admin == '0':
		pointsLeft = [MAX_DAILY_POINTS - getPointUsage(post.name)[0], MAX_NEG_DAILY_POINTS -  getPointUsage(post.name)[1]]
		if not isNegative:
			if pointsLeft[0] > 0:
				message += "\n[b]%s[/b] can still award another %s today." % (post.name, pointStr(pointsLeft[0]))
			else:
				message += "\n[b]%s[/b] can't award any more points until tomorrow." % (post.name)
		else:
			if pointsLeft[1] > 0:
				message += "\n[b]%s[/b] can still remove another %s today." % (post.name, pointStr(pointsLeft[1]))
			else:
				message += "\n[b]%s[/b] can't remove any more points until tomorrow." % (post.name)			
	
	if int(sb.config['points']['postId']) > 0:
		message +="\nCheck [url=%s]this thread[/url] for the current high scores!" % (sb.showthreadurlforpost + sb.config['points']['postId'])
	
	reply = sb.quotePost(post, command) + sb.decorate(message)
	sb.doReply(post.postId, reply)
	
	if int(sb.config['points']['postId']) > 0:
		sb.updatePost(sb.config['points']['postId'], {"SCORES" : getTopPointsMessage()})
	sb.config.write()
	
	
def getRankForName(name):
	users = sb.config['points']['scorelist'].keys()
	users.sort(key=lambda x: int(sb.config['points']['scorelist'][x])*-1)
	index = users.index(name)
	return ordinal(index + 1)

def getTopPointsMessage():
	users = sb.config['points']['scorelist'].keys()
	users.sort(key=lambda x: int(sb.config['points']['scorelist'][x])*-1)
	message = '\n[B][SIZE="4"]PWI Forum High Scores:[/SIZE][/B]\n\n'
	for i,user in enumerate(users):
		message +="%d) [b]%s[/b]  (%d)\n" % (i+1, user, int(sb.config['points']['scorelist'][user])) 
	return message
	

if __name__=="__main__":
	sb.config['points']['scorelist']['SweetieBot - Lothranis'] = 42
	sb.config.write()