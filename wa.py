#!/usr/bin/python
import wolframalpha
import uploadimage
import re
from pprint import pprint
client = wolframalpha.Client("X4629E-LT7Q4WPWAU")

def getMessageFromPod(pod, title=True):
	if not pod.text:
		return ""
	message = "[b][color=white]%s:[/color][/b] %s" % (pod.title, pod.text) if title else pod.text
	if title:
		message = message.replace("\n", "\n[color=#1e1713]----[/color]")
	return message + "\n"

def getMessageFromPods(pods):
	message = ""
	resultPods = [pod for pod in pods if pod.id == "Result"]
	if len(resultPods) == 1:
		message = getMessageFromPod(resultPods[0], title=False)
	elif len(resultPods) > 1:
		for pod in resultPods:
			message += getMessageFromPod(pod)
	else:
		for pod in pods:
			message += getMessageFromPod(pod)
			
	for pod in pods:
		if not pod.text:
			url = pod.main.node.find('img').attrib['src']
			url = uploadimage.recolorImage(url)
			message += "\n[b][color=white]%s:\n[/color][/b][url][img]%s[/img]%s[/url]" % (pod.title, url, pod.title)
	return message

def getWolframAlphaMessage(query):
	print "Got Query:", query
	try:
		res = client.query(query)
	except Exception:
		return "That's too hard try something else."
	message = getMessageFromPods(res.pods)
	if re.search("(?:Stephen )?Wolfram(?: and his team)?", message):
		return "Asterelle - Sanctuary\n[url][img]http://i.imgur.com/zBLGMzQ.png[/img][/url]\n"#"[url][img]http://i.imgur.com/aJSvcii.gif[/img][/url]\n"
	return message
		

if __name__ == "__main__":
	#print getWolframAlphaMessage("the date of the next solar eclipse in new york?")
	#print getWolframAlphaMessage("3x^3 + 10 if x = 2")
	print getWolframAlphaMessage('the color salmon')