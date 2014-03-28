import praw
from collections import deque
from time import sleep
import re


r = praw.Reddit("binaryToTextBot by /r/thirdegree")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

done = deque(maxlen=200)

Trying = True
while Trying:
	try:
		USERNAME = _login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

def main():
	comments = praw.helpers.comment_stream(r,'all', limit = 1000)
	for i in comments:
		if i.id in done:
			continue
		done.append(i.id)
		translated = translate(i.body)
		if translated != "":
			print translated
			i.reply(translated)
			sleep(2)

def translate(body):
	try:	
		pattern = r"((\s|^)[10 ]+)+"
		matches = re.findall(pattern, body)
		matches = [re.sub("[\s]", "",i[0]) for i in matches]
		translated = ""
		if all([i == '' for i in matches]):
			return ""
		for word in matches:
			word_fixed = re.sub(" ", "", word)
			if len(word_fixed) == 0:
				continue
			if len(word_fixed)%8 == 0 and all([k in ["0","1"] for k in word_fixed]):
				translated += ("> "+ word+"\n\n")
				translated += (''.join(chr(int(word_fixed[l:l+8], 2)) for l in xrange(0, len(word_fixed), 8)) + "\n\n")
		return "".join(translated)
	except UnicodeEncodeError as e:
		r.send_message('thirdegree', e, "%s, %s, %s, %s"%(translated, i.body, matches, word_fixed)) 
		raise e


try: 
	main()
except Exception as e:
	print e
	sleep(100)
