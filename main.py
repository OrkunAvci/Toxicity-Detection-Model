import pandas as pd

from api.youtube import Youtube
from api.perspective import Detector

video_ids = [
	""
]

scored_texts = []
for id in video_ids:
	print("Session ID: ", id)
	yt = Youtube(id)
	scored_texts.extend(yt.process_comments(yt.get_comments()))

df = pd.DataFrame(scored_texts)
df.to_csv("./data/df.csv")
