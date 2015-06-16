#!/usr/bin/python
import re
import sweetiebot as sb
import datetime

MIN_REQUIRED_POSTCOUNT = 50

def getPromoCodesMessage():
	message = ""
	codelist = sb.config['code']['codelist']
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
		expirationMessage = sb.invisible("---- ") + ("Expired" if expired else "Expires")
		expirationMessage += " on %s" % codelist[code]['expires'] if codelist[code]['expires'] else " on ????"
		result = "[color=%s][b]%s[/b][/color] - [color=white]%s[/color]\n%s Added by %s on %s" %('cyan' if not expired else 'pink',
			code, 
			codelist[code]['item'],
			expirationMessage,
			sb.decorateName(codelist[code]['author']),
			codelist[code]['addedon'])
		return result + "\n\n"
	
	if len(current) > 0:
		message += "[color=cyan][b]Current Code List[/b][/color]\n\n"		
		for code in current:
			message += messageForCode(code[0], codelist, False)
		
	if len(expired) > 0:
		message += "\n\n[color=pink][b]Recently Expired Code List[/b][/color]\n\n"	
		for code in expired:
			message += messageForCode(code[0], codelist, True)
	return message


def promoCodeCommand(post, command, args):
	print "Got Promo Code Command", command,"-", args
	match = re.search ('add +code +(.{8}) +for +(?:a |the )?(.+?)(?: +which +expires +on +([0-9\-/]+))?$', command)
	errorMessage = "Please use this exact command:\n"
	errorMessage += "Sweetiebot add code <CODE> for <ITEM(s)> [which expires on YYYY-MM-DD]\n"
	errorMessage += "[color=white]Example[/color]: Sweetiebot add code 75HtYCE6 for a Jones Blessing which expires on 2016-01-01"
		
	if not match:
		message = "Can't quite understand that :( " + errorMessage
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return		
	code = match.group(1)
	item = match.group(2)
	if re.search('expir', match.group(2)):
		message = "There's some issue with the expiration, it needs to say 'which expires on' :(\n" + errorMessage
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return	
	date = match.group(3) 
	date = date if date else ""
	if date:
		try:
			datetime.datetime.strptime(date, "%Y-%m-%d")
		except:
			message = "The date has to be ISO-8601 format, YYYY-MM-DD\n" + errorMessage
			reply = sb.quotePost(post, command) + sb.decorate(message)
			sb.doReply(post.postId, reply)
			return	
	author = post.name
	print 'code is '+'|'.join((code,item,date,author))
	if int(post.postCount.replace(',', '')) < int(sb.config['code']['minpostcount']):
		message = "Sorry but you need to have at least %s posts to be able to set codes" % sb.config['code']['minpostcount']
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return		
	
	sb.config['code']['codelist'][code] = {}
	sb.config['code']['codelist'][code]['item'] = item	
	sb.config['code']['codelist'][code]['expires'] = date
	sb.config['code']['codelist'][code]['author'] = author
	sb.config['code']['codelist'][code]['addedon'] = sb.getPostTime(post.time).date()
	
	if int(sb.config['code']['postId']) > 0:
		sb.updatePost(sb.config['code']['postId'], {"CODES" : getPromoCodesMessage()})
	sb.config.write()
	
	message = "Added code [color=cyan]%s[/color] - [color=white]%s[/color]%s!\n" %(code, item, ("which expires on [color=white]%s[/color]"%date) if date else "")
	message = "If this is a mistake say [color=white]Sweetiebot remove code %s[/color]" % code
	reply = sb.quotePost(post, command) + sb.decorate(message)
	sb.doReply(post.postId, reply)

def removeCodeCommand(post, command, args):
	print "Got Remove Code Command", command,"-", args

	if int(post.postCount.replace(',', '')) < int(sb.config['code']['minpostcount']):
		message = "Sorry but you need to have at least %s posts to be able to remove codes" % sb.config['code']['minpostcount']
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		return	
	
	code = args
	if code in sb.config['code']['codelist']:
		codeValue = sb.config['code']['codelist'][code] 
		sb.config['code']['codelist'].remove(code)
		message = "Removing promo code %s\n" % code
		message += "This can be undone with the command: [color=white]Sweetiebot add code %s for %s%s[/color]" % (code,
			codeValue['item'],
			(" which expires on " + codeValue['expires']) if codeValue['expires'] else '')
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)
		
		if int(sb.config['code']['postId']) > 0:
			sb.updatePost(sb.config['code']['postId'], {"CODES" : getPromoCodesMessage()})
	else:
		message = "I don't think %s is a code, maybe it was already removed or expired?"
		reply = sb.quotePost(post, command) + sb.decorate(message)
		sb.doReply(post.postId, reply)

if __name__=="__main__":
	sb.config['code'] = {}
	sb.config['code']['postId'] = '22362671'
	sb.config['code']['codelist'] = {}	
	sb.config['code']['minpostcount'] = '50'
	sb.config.write()