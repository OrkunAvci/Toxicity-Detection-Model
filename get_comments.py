from api.youtube import Youtube
import json
import threading

video_ids = []
comments = {}
lock = threading.Lock()

with open("./data/video_ids.json", "r") as f:
	video_ids = json.loads(f.read())

with open("./data/comments.json", "r") as f:
	comments = json.loads(f.read())

yt = Youtube()
for id in video_ids:
	if id not in comments.keys():
		print("Session ID: ", id)
		comments[id] = yt.get_comments(id)
		with open("./data/comments.json", "r+") as f:
			with lock:
				f.write(json.dumps(comments))
	else:
		print("Skipped ", id)
