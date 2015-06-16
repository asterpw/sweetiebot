#!/usr/bin/python
from sweetiebot import *

AFK_MESSAGE = "\n\nStatus: b:cry AFK AFK AFK b:cry"
NOT_AFK_MESSAGE = "\n\nStatus: ONLINE"
settings.testMode = False;
doLogin()
br.open('http://pwi-forum.perfectworld.com/profile.php?do=editsignature')
br.select_form("vbform")
text = br['message']
if text.find(AFK_MESSAGE.strip()) > -1:
	text = text[:text.find(AFK_MESSAGE.strip())].strip() + NOT_AFK_MESSAGE
	print "Setting to not AFK", text
else:
	if text.find(NOT_AFK_MESSAGE.strip()) > -1:
		text = text[:text.find(NOT_AFK_MESSAGE.strip())].strip()
	text += AFK_MESSAGE
	print "Setting to AFK", text
br['message'] = text
for control in br.form.controls:
	if control.type == 'submit':
		control.disabled = control.get_labels()[0].text != "Save Signature"
br.submit()
print "done"