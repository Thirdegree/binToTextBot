import praw
from collections import deque
from time import sleep


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
	comments = r.get_comments('all')
	for i in comments:
		translate = ""
		if i.id in done:
			continue
		done.append(i.id)
		for j in i.body.split():
			j = j.strip()
			if len(j)%8 == 0 and all([k in ["0","1"] for k in j]):
				translate += "> " + j + "\n\n"
				translate += ''.join(chr(int(j[l:l+8], 2)) for l in xrange(0, len(j), 8)) + "\n\n"
		if translate != "":
			print translate
			i.reply(translate)
			sleep(2)


while True:
	try: 
		main()
		sleep(10)
	except Exception as e:
		print e
		sleep(100)
