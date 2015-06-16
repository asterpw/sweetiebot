#!/usr/bin/python
import random
import mechanize
import re
import bs4 as BeautifulSoup
from bs4.element import NavigableString
from urllib import quote

br=mechanize.Browser()
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def getColorForName(colorname):
	colors = {'item_color0': '#ffffff', 'item_color1': '#8080ff', 'item_color2': '#ffdc50', 'item_color3': '#aa32ff', 'item_color4': '#ff6000', 'item_color5': '#ffffff', 'item_color6': '#b0b0b0', 'item_color7': '#00ffae', 'item_color8': '#6cfb4b', 'item_color9': '#ff0000', 'item_color10': '#80ffff'}
	return colors[colorname]

class Item:
	def __init__(self, name, id, color, quantity, chance):
		self.name = name.encode('ascii', 'xmlcharrefreplace') 
		self.id = int(id)
		self.quantity = quantity
		self.chance = chance
		self.color = getColorForName(color)
	def __hash__(self):
		return hash((self.name, self.id))
	def __eq__(self, other):
		return (self.name, self.id) == (other.name, other.id)

class Mob:
	def __init__(self, name, id, level, defDropChances, defDrop, addDropChance, addDrop, moneyDrop):
		self.name = name.encode('ascii', 'xmlcharrefreplace') 
		self.id = int(id)
		self.level = level
		self.defDropChances = defDropChances
		self.defDrop = defDrop
		self.addDropChance = addDropChance
		self.addDrop = addDrop
		self.moneyDrop = moneyDrop


def findQuest(html):
	match = re.search('<a href="quest/([0-9]+)">Activate Task</a>', html)
	if match:
		return match.group(1)
	return False

def searchItem(itemname):
	br.open('http://www.pwdatabase.com/pwi/search_item')
	br.select_form(nr=1)
	br.form['name'] = itemname
	print "Searching for item:", itemname
	html = br.submit().read().decode('utf-8')
	return html

def searchMob(mobname):
	br.open('http://www.pwdatabase.com/pwi/search_mob')
	br.select_form(nr=1)
	br.form['name'] = mobname
	html = br.submit().read().decode('utf-8')
	mobIds = re.findall('href="mob/([0-9]+)">', html)
	if len(mobIds) == 0:
		return False
	print 'Found mob', mobIds[0], 'for mobname', mobname
	return mobIds[0]

def getMob(mobId):
	html = br.open('http://www.pwdatabase.com/pwi/mob/' + str(mobId)).read().decode('utf-8')
	soup = BeautifulSoup.BeautifulSoup(html, "html5lib")
	mainTable = soup.find('table', {'class': 'tablePlain'})
	name = mainTable.find('th').text.strip()
	leftText = mainTable.findAll('tr')[1].findAll('td')[0].text
	
	chances = [0, [0,0,0,0]]
	match = re.search("How many times .*?([0-9]+)", leftText, re.MULTILINE | re.DOTALL | re.IGNORECASE)
	if match:
		chances[0] = int(match.group(1))
	match = re.search("Drop rate of several.*?0: ([0-9.]+)%\s*1: ([0-9.]+)%\s*2: ([0-9.]+)%\s*3: ([0-9.]+)%\s*", leftText, re.MULTILINE | re.DOTALL | re.IGNORECASE)
	if match:
		chances[1][0] = float(match.group(1))/100
		chances[1][1] = float(match.group(2))/100
		chances[1][2] = float(match.group(3))/100
		chances[1][3] = float(match.group(4))/100
		
	addDropChance = 0
	match = re.search("Probability of addit.*?1: ([0-9.]+)%", leftText, re.MULTILINE | re.DOTALL | re.IGNORECASE)
	if match:
		addDropChance = float(match.group(1))/100
	
	moneyDrop = [0, 0]
	match = re.search("Money.*?([0-9]+) \(\+\-([0-9]+)\)", leftText, re.MULTILINE | re.DOTALL | re.IGNORECASE)
	if match:
		moneyDrop[0] = int(match.group(1)) - int(match.group(2))
		moneyDrop[1] = int(match.group(1)) + int(match.group(2))
	
	level = 150
	match = re.search("Level.*?([0-9]+)", leftText, re.MULTILINE | re.DOTALL | re.IGNORECASE)
	if match:
		level = int(match.group(1))
	
	ddrops = []
	dropHead = soup.find('div', {'id':'mob_ddrop'})
	if dropHead:
		ddrops = getDropsFromTable(dropHead.nextSibling.nextSibling)
	
	adrops = []
	addDropHead = soup.find('div', {'id':'mob_adrop'})
	if addDropHead:
		adrops = getDropsFromTable(addDropHead.nextSibling.nextSibling)
	
	return Mob(name, mobId, level, chances, ddrops, addDropChance, adrops, moneyDrop)

def killMob(mob, quantity, playerlevel, bonusDrop):
	result = {}
	for i in range(quantity):
		oneKill = killMobOnce(mob, playerlevel, bonusDrop)
		for item in oneKill:
			result[item] = result.get(item, 0) + oneKill[item]
	return result

def chanceOfGettingItems(playerlevel, moblevel):
	if playerlevel - moblevel >= 40:
		return 0.2
	if playerlevel - moblevel >= 30:
		return 0.25
	if playerlevel - moblevel >= 25:
		return 0.30
	if playerlevel - moblevel >= 20:
		return 0.40
	if playerlevel - moblevel >= 15:
		return 0.5
	if playerlevel - moblevel >= 11:
		return 0.6
	if playerlevel - moblevel >= 8:
		return 0.7
	if playerlevel - moblevel >= 5:
		return 0.8
	if playerlevel - moblevel >= 3:
		return 0.9
	return 1

def getMobNameColor(playerlevel, moblevel):
	if playerlevel - moblevel >= 20:
		return '#0A0'
	if playerlevel - moblevel >= 10:
		return '#4C4'
	if playerlevel - moblevel >= 3:
		return '#AEA'
	if playerlevel - moblevel > -3:
		return '#FFF'
	if playerlevel - moblevel > -10:
		return '#FDA'
	if playerlevel - moblevel > -20:
		return '#FB5'
	return '#F90'


def killMobOnce(mob, playerlevel, bonusDrop):
	result = {}
	if random.random() < mob.addDropChance and len(mob.addDrop) > 0:
		item = selectItem(random.random(), mob.addDrop)
		result[item] = result.get(item, 0) + 1
	coinItem = Item('Coin(s)', '3044', 'item_color0', 1, 1)
	coins = random.randint(mob.moneyDrop[0], mob.moneyDrop[1])
	if coins:
		result[coinItem] = coins
	if random.random() > chanceOfGettingItems(playerlevel, mob.level):
		return result
	for i in range(mob.defDropChances[0]*bonusDrop):
		roll = random.random()
		for times,chance in enumerate(mob.defDropChances[1]):
			if roll < chance  and len(mob.defDrop) > 0:
				for j in range(times):
					item = selectItem(random.random(), mob.defDrop)
					result[item] = result.get(item, 0) + 1
				break
			else:
				roll -= chance
	return result
		

def selectItem(roll, items):
	defitem = items[0]
	for item in items:
		if roll < item.chance:
			return item
		roll -= item.chance
	return defitem

def getDropsFromTable(table):
	items = []
	rows = table.findAll('tr')
	for row in rows:
		if row.find('th'):
			continue
		link = row.findAll('td')[2].find('a')
		itemName = link.text.strip().encode('ascii', 'xmlcharrefreplace')
		itemId = re.search('items/([0-9]+)', link['href']).group(1)
		span = link.find('span')
		itemColor = span['class'][0] if span else 'item_color0'
		chanceText = row.findAll('td')[3].text
		itemChance = float(re.search('([0-9.]+)%', chanceText).group(1))/100
		items.append(Item(itemName, itemId, itemColor, 1, itemChance))
		print itemName, itemId, itemColor, 1, itemChance
	return items


def getQuestFromItemId(itemId):
	html = br.open('http://www.pwdatabase.com/pwi/items/' + str(itemId)).read().decode('utf-8')
	return findQuest(html)


def getQuestFromHtml(html):
	items = re.findall('href="items/([0-9]+)">', html)
	if items:
		quest = getQuestFromItemId(items[0])
		return quest
	return False	
	
def getQuestFromItem(itemname):
	html = searchItem(itemname)
	items = re.findall('href="items/([0-9]+)">', html)
	if items:
		quest = getQuestFromItemId(items[0])
		return quest
	return False

def getCardPackFromItemHtml(html):
	soup = BeautifulSoup.BeautifulSoup(html, "html5lib")
	table = soup.find('table', {'id': 'mobs_drop', 'width': '450'})
	if not table:
	    return False
		
	links = table.findAll('a', {'href': re.compile('items/[0-9]+')})
	items = []
	for link in links:
		if not link.text.strip():
			continue
		itemName = link.text.strip().encode('ascii', 'xmlcharrefreplace')
		itemId = re.search('items/([0-9]+)', link['href']).group(1)
		span = link.find('span')
		itemColor = span['class'][0] if span else 'item_color0'
		itemQuant = 1
		itemChance = float(str(link.parent.parent.findAll('td')[2].text)) / 100
		items.append(Item(itemName, itemId, itemColor, itemQuant, itemChance))
	packNameElem = soup.find('div', {'id': 'content'}).find('th', {'class': 'itemHeader'}).contents[0]
	span = packNameElem.find('span')
	packColor = packNameElem['class'][0] if packNameElem.name == 'span' else 'item_color0'
	packName = packNameElem.text.strip() if packNameElem.name == 'span' else str(packNameElem).strip()
	packId = re.search('items/([0-9]+)', html).group(1)
	pack = Item(packName, packId, packColor, 0, 0)
	pack.questId = 0
	pack.payout = items 
	return pack
		

def getPackQuest(quest):
	html = br.open('http://www.pwdatabase.com/pwi/quest/' + str(quest)).read().decode('utf-8')
	soup = BeautifulSoup.BeautifulSoup(html, "html5lib")
	subQuestDiv = soup.find('div', {'class': 'right'})
	items = []
	if subQuestDiv:  #for the packs that have subquests... add the payouts from those
		subQuestLink = subQuestDiv.find('a', {'href': re.compile('quest/[0-9]+')})
		if subQuestLink:
			quest = re.search('quest/([0-9]+)', subQuestLink['href']).group(1)
			print "found subquest", quest
			items = getPackQuest(int(quest)).payout
	
	table = soup.find('table', {'class': 'tablePlain'})
	if not table:
	    return False
	tds = table.findAll('td')
	links = tds[0].findAll('a', {'href': re.compile('items/[0-9]+')})

	for link in links:
		if not link.text.strip():
			continue
		itemName = link.text.strip().encode('ascii', 'xmlcharrefreplace')
		itemId = re.search('items/([0-9]+)', link['href']).group(1)
		itemtext = unicode(link.nextSibling).strip().encode('ascii', 'xmlcharrefreplace')
		print itemName, itemId, itemtext
		span = link.find('span')
		itemColor = span['class'][0] if span else 'item_color0'
		itemQuant = 1
		itemChance = 1
		if itemtext:
			match = re.search("\(([0-9.]+)%\)?", itemtext)
			if match:
				itemChance = float(match.group(1))/100 
			match = re.search("- ([0-9]+)", itemtext)
			if match:
				itemQuant = int(match.group(1))
		items.append(Item(itemName, itemId, itemColor, itemQuant, itemChance))
	packLink = tds[1].find('a', {'href': re.compile('items/[0-9]+')})
	if packLink:
		span = packLink.find('span')
		packColor = span['class'][0] if span else 'item_color0'
		packName = packLink.text.strip()
		packId = re.search('items/([0-9]+)', packLink['href']).group(1)
		pack = Item(packName, packId, packColor, 0, 0)
	else:  #dummy pack for subquest payout
		pack = Item("", 0, "item_color0", 0, 0)
	pack.questId = int(quest)
	pack.payout = items
	return pack

def getPackFromName(packname):
	pack = None
	message = ''
	namesToTry = ['"%s"' % (packname), packname]
	if packname.endswith('es'):
		namesToTry.append('"'+packname[:-2]+'"')
		namesToTry.append(packname[:-2])
	elif packname.endswith('s'):
		namesToTry.append('"'+packname[:-1]+'"')
		namesToTry.append(packname[:-1])
	
	for packNameCandidate in namesToTry:
		html = searchItem(packNameCandidate)
		items = re.findall('href="items/([0-9]+)">', html)
		if items:
			itemId = items[0]
			itemHtml = br.open('http://www.pwdatabase.com/pwi/items/' + str(itemId)).read().decode('utf-8')
			pack = getCardPackFromItemHtml(itemHtml)
			if not pack:
				quest = getQuestFromItemId(itemId)
				if not quest:
					message = "Sorry but '%s' doesn't look like a pack to me :(\nTry again with the exact spelling." % (packname)
					continue
				pack = getPackQuest(quest)
			if pack and pack.payout:
				pack.payout.sort(key=lambda x: x.chance*-1)
				packCache[packname] = pack
				return pack, ''
	return 0, "Sorry but I can't find a pack called '%s' on [url=http://pwdatabase.com]pwdb[/url] :(\nIt might not be there yet.  Try again with the exact spelling." % (packname)

	
packCache = {}

def openPacks(packname, quantity):
	pack = None
	message = ''
	result = {}
	if packname in packCache:
		pack = packCache[packname]
	else:
		pack,message = getPackFromName(packname)
		if message:
			return message,0,0
		
	totalChance = sum(x.chance for x in pack.payout if x.chance != 1)
	for item in pack.payout:
		if item.chance != 1:
			item.chance /= totalChance
	
	for i in range(quantity):
		roll = random.random()
		for item in pack.payout:
			if roll <= item.chance:
				result[item] = result.get(item, 0) + item.quantity
				if item.chance != 1:
					break
			if item.chance != 1:
				roll -= item.chance
	return message, pack, result
	
def getGearHtml(gearname):
	match = re.search('^(?:item )?([0-9]+)', gearname)
	if match:
		html = br.open('http://www.pwdatabase.com/pwi/items/' + match.group(1)).read().decode('utf-8')
		return html
	html = searchItem(gearname)
	match = re.search('href="items/([0-9]+)">', html)
	if match:
		html = br.open('http://www.pwdatabase.com/pwi/items/' + match.group(1)).read().decode('utf-8')
		return html
	return False

def getInfoText(soup):
	infotag = soup.find('div', {'class': 'iteminfo'})
	infoText = ''
	def getTextForSpan(tag):
		text = ''
		for content in tag.contents:
			text += content.encode('ascii', 'xmlcharrefreplace') if type(content) == NavigableString else '\n'
		return text
	for content in infotag.contents:
		if type(content) == NavigableString:
			infoText += content.encode('ascii', 'xmlcharrefreplace').strip().replace('\n', '').replace('\t', ' ') 
		elif content.name == 'br': 
			infoText += "\n"
		elif content.name == 'span':
			color = re.search("#([0-9a-f]+)", content['style'].lower()).group(1)
			infoText += "[color=#%s]%s[/color]" % (color, getTextForSpan(content))
		elif content.name == 'p':
			break
		else:
			infoText += content.text.encode('ascii', 'xmlcharrefreplace')
	return infoText.strip().replace('\n\n','\n')
	
class Addon:
	def __init__(self, pretext, low, high, posttext, chance):
		self.text = pretext
		if low: 
			self.text = self.text + "#ROLL#" + posttext
		self.low = int(low) if low != None else 0
		self.high = int(high) if low != None else 0
		self.chance = chance
	
	def __str__(self):
		randval = ''
		if self.low != 0 and self.high != 0:
			randval = str(random.randint(self.low, self.high))
		text = self.text.replace("#ROLL#", randval)
		return text

def getItemAddons(soup):
	uniquestats = []
	itemstats = []
	currentstat = itemstats
	addontag = soup.find('div', {'id': 'ia_addons'})
	numAddons = ''
	uniqueChance = 0
	if addontag:
		for content in addontag.contents:
			if type(content) == NavigableString:
				text = content.encode('ascii', 'xmlcharrefreplace').strip()
			else:
				text = content.text.strip()
			if not len(text): continue
			print "AddOn:", text
			amatch = re.search("Amount:(.*)", text)
			bmatch = re.search("Probability to have an unique addon: ([0-9.]+)%", text)
			cmatch = re.search("(.*?)(?:([0-9]+)~([0-9]+)(.*?))?(?: - ([0-9.]+)%)?$", text, re.DOTALL)
			if text == "Items Addons:":
				currentstat = itemstats
			elif text == "Unique Addon:":
				currentstat = uniquestats
			elif text == "Extra Addons:":
				break
			elif amatch:
				numAddons = amatch.group(1)
			elif bmatch:
				uniqueChance = float(bmatch.group(1))/100
			elif cmatch:
				chance = 1;
				if cmatch.group(5): 
					chance = float(cmatch.group(5))/100
				currentstat.append(Addon(cmatch.group(1), cmatch.group(2), cmatch.group(3), cmatch.group(4), chance))

	return numAddons, uniqueChance, itemstats, uniquestats


class Gear:
	def __init__(self, name, color, itemid, iteminfo, socketChances, numAddons, itemstats, uniqueChance, uniquestats):
		self.name = name.encode('ascii', 'xmlcharrefreplace') 
		self.itemid = int(itemid)
		self.color = getColorForName(color)
		self.iteminfo = iteminfo
		self.socketChances = socketChances
		self.numAddons = numAddons
		self.itemstats = itemstats
		self.uniquestats = uniquestats
		self.uniqueChance = uniqueChance
		self.fullStat = False
	
	def __str__(self):
		sockets = self.getSockets()
		text = "[url][img]http://www.pwdatabase.com/images/icons/generalm/%d.gif[/img][/url][url=http://pwdatabase.com/items/%d][color=%s]%s[/color][/url] %s\n" % (self.itemid, self.itemid, self.color, self.name, sockets)
		text += self.iteminfo
		match = re.search("Price:.*", text)
		if match:
			statText = self.getStats().strip()
			if statText: statText += "\n"
			text = re.sub("Price:.*", statText + match.group(0), text)
			text = re.sub("Stacked:.*", "[color=#6cfb4b]Manufactured by ##NAME##[/color]\n", text)
		else:
			text += self.getStats()
		return text.strip()

	def getSockets(self):
		roll = random.random()
		for i in range(len(self.socketChances)):
			if roll < self.socketChances[i]:
				return "(%d socket(s))" % (i) if i > 0 else ""
			roll -= self.socketChances[i]
	
	def getAddonCount(self):
		if len(self.itemstats) <= 3:
			self.fullStat = True
			return len(self.itemstats)
		if re.match("^[0-9]$", self.numAddons):
			numAdds = int(self.numAddons)
			if numAdds == len(self.itemstats):
				self.fullStat = True
			return numAdds
		elif self.numAddons == "3+":
			if self.allAddonsSameChance():
				self.fullStat = True
				return len(self.itemstats)
			else:
				return 3
		chances = {
		"0-3": [0.4, 0.4, 0.15, 0.05],
		"1-3": [0, 0.7, 0.225, 0.075],
		"2-3": [0, 0, 0.65, 0.35],
		}
		addonChance = chances.get(self.numAddons, chances["0-3"])
		roll = random.random()
		for i in range(len(addonChance)):
			if roll < addonChance[i]:
				return i
			roll -= addonChance[i]
		return len(self.itemstats)
		
	def allAddonsSameChance(self):
		chance = self.itemstats[0].chance
		for stat in self.itemstats:
			if stat.chance != chance:
				return False
		return True
	
	def getStats(self):
		numAdds = self.getAddonCount()
		if self.fullStat:
			return "\n".join(["[color=%s]%s[/color]" % (getColorForName('item_color1'), str(addon)) for addon in self.itemstats])
		text = ""
		if numAdds > 0:
			if random.random() < self.uniqueChance:
				text += self.getRandomStat(self.uniquestats)
				numAdds -= 1
			for i in range(numAdds):
				text += self.getRandomStat(self.itemstats)
		return text
	
	def getRandomStat(self, stats):
		stats.sort(key=lambda x: x.chance)
		roll = random.random()
		for stat in stats:
			if roll < stat.chance:
				name = str(stat)
				if name.startswith("Unidentified"):
					return self.getRandomStat(stats)
				return "[color=%s]%s[/color]\n" % (getColorForName('item_color1'), name)
			roll -= stat.chance
		return ''
	
def getGear(html):
	soup = BeautifulSoup.BeautifulSoup(html, "html5lib")
	if not re.search('href="key/[369]"', str(soup.find('div', {'class': 'iteminfo'}))):
		return False
	infoText = getInfoText(soup)
	socketChances = [1.0, 0, 0, 0, 0]
	chances = re.findall("Craft Rate with ([0-4]) socket\(s\): ([0-9.]+)%", infoText)
	for sock in chances:
		if socketChances[0] == 1: socketChances[0] = 0
		socketChances[int(sock[0])] = float(sock[1])/100
	if infoText.find("Craft Rate with") != -1: infoText = infoText[:infoText.find("Craft Rate with")].strip()
	numAddons, uniqueChance, itemstats, uniquestats = getItemAddons(soup)
	tag = soup.find("th")
	name = ''
	color = 'item_color0'
	if type(tag.contents[0]) == NavigableString:
		name = tag.contents[0].encode('ascii', 'xmlcharrefreplace').strip()
	else:
		name = tag.contents[0].text.strip()
		color = tag.contents[0]['class'][0]
	itemid = re.search("images/icons/generalm/([0-9]+).gif", html).group(1)
	gear = Gear(name, color, itemid, infoText, socketChances, numAddons, itemstats, uniqueChance, uniquestats)
	return gear

gearCache = {}

def rollGear(gearname, username='SweetieBot'):
	print "Forging", gearname
	#gearname = BeautifulSoup.BeautifulSoup(gearname).text.encode('utf-8')
	gear = None
	if gearname in gearCache:
		gear = gearCache[gearname]
	else:	
		html = getGearHtml(gearname)
		if br.geturl().find('items') == -1:
			return "Can't find any gear called '%s' on pwdb :( \nIs that the right way to spell it?" % (gearname)
		gear = getGear(html)
		if not gear:
			return "Umm, is '%s' really a gear you can forge?\nIt has to be a weapon, armor, or accessory." % (gearname)
		gearCache[gearname] = gear
	gearStr = str(gear).replace("##NAME##", username)
	#refine link uses a url encoded version of the infotext but with image tags and url tags removed/stripped
	gearRefineLink = re.sub("\[img\].*?\[\/img\]",'',gearStr) 
	gearRefineLink = re.sub("\[url(=.*?)?\](.*?)\[\/url\]",'\\2',gearRefineLink)
	gearRefineLink = quote(gearRefineLink).replace('%20', '+') #%20->+ saves url length
	
	return "Here you go!\n\n" + gearStr +"\n[size=1][url=http://aster.ohmydays.net/pw/refiningsimulator.html#id=%s&tip=%s]Refine this gear![/url]\nIf this is wrong try using the item ID: [color=white]SweetieBot please forge item ####.[/color][/size]" % (gear.itemid, gearRefineLink) 

def getOpenPackMessage(packname, quantity):
	print "Got Open Pack CMD:", packname, quantity
	packnameutf = BeautifulSoup.BeautifulSoup(packname).text.encode('utf-8')
	while True:
		message, pack, results = openPacks(packname, quantity)
		if message and packname.endswith('s'):
			packname = packname[:-1]
		else:
			break
	if message:
		return message.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
	items = results.keys()
	items.sort(key=lambda x: -1*results[x])
	packNameLink = "[url=http://pwdatabase.com/quest/%d][color=%s]%ss[/color][/url]" % (pack.questId, pack.color, pack.name)
	if pack.questId == 0:
		packNameLink = "[url=http://pwdatabase.com/items/%d][color=%s]%ss[/color][/url]" % (pack.id, pack.color, pack.name)
	message = "You've opened [color=white]%d[/color] [url][img]http://www.pwdatabase.com/images/icons/generalm/%d.gif[/img][/url] %s!\n\n" % (quantity, pack.id, packNameLink)
	message += "You've won:\n"
	for item in items:
		message += '[color=white]%d[/color] [url=http://pwdatabase.com/items/%d][color=%s]%s[/color][/url]\n' % (results[item], item.id, item.color, item.name)
	return message

mobCache = {}

def getMobKillMessage(mobname, quantity, playerlevel=0, bonusDrop=1):
	if mobname in mobCache:
		mob = mobCache[mobname]
	else:
		mobid = searchMob(mobname)
		if not mobid:
			return "Ehh, is '%s' really the right name of the mob?" % mobname
		mob = getMob(mobid)
		mobCache[mobname] = mob
	results = killMob(mob, quantity, playerlevel, bonusDrop)
	items = results.keys()
	items.sort(key=lambda x: -1*results[x])
	bonusMessage = " during %dx" % bonusDrop if bonusDrop != 1 else ''
	message = "You've killed [url=http://www.pwdatabase.com/pwi/mob/%d][color=%s]%s[/color][/url] %d times%s!\n\n" % (mob.id, getMobNameColor(playerlevel, mob.level), mob.name, quantity, bonusMessage)
	itemChance = chanceOfGettingItems(playerlevel, mob.level)
	if itemChance < 1:
		message += "Since you are level [color=white]%d[/color] and the mob is level [color=white]%d[/color], there is an added [color=white]%.0f[/color]%% chance of the mob not dropping :(\n\n" % (playerlevel, mob.level, (1-itemChance)*100)
	message += "You've farmed:\n"
	for item in items:
		message += '[color=white]%d[/color] [url=http://pwdatabase.com/items/%d][color=%s]%s[/color][/url]\n' % (results[item], item.id, item.color, item.name)
	return message

if __name__ == "__main__":
	#print getMobKillMessage('Twilight Emperor - Vacuity', 10, 0, 2)
	#print getMobKillMessage('Horrorbite', 100, 105)	
	#print getMobKillMessage('Horrorbite', 100, 105)	
	#print getMobKillMessage('Horrorbite', 100, 105)	
	#print rollGear('Ceremonial Magic Sword')
	#print rollGear('item 28420')
	#print rollGear('Reincarnation')
	#print rollGear('Reincarnation')
	#print rollGear('Reincarnation')
	#print rollGear('Dream of Reality')
	#print rollGear('Blashpheme Shot')
	#print rollGear('Solar Strike Bow')
	#print rollGear('Firmament')
	print getOpenPackMessage("Rainbow Eggs", 10)
	#print getOpenPackMessage("Brawler Fashion Pack", 1)
	#print getOpenPackMessage("Tiger Packs", 3)
	print getOpenPackMessage("Drake Mirror Pack", 10)
	print getOpenPackMessage("Horselords' Bounty", 300)
	print getOpenPackMessage("War Avatar Pack S", 10000)