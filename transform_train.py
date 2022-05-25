from api.perspective import Detector
import pandas as pd

df = pd.read_csv("./data/train.csv")
out = pd.read_csv("./data/new_train.csv")

logged = list(df.loc[:,"comment_text"].array)
processed = list(out.loc[:,"Comment"].array)

to_process = [comment for comment in logged if comment not in processed]

detector = Detector()
for text in to_process:
	detection = detector.detect(text)
	if detection:
		created = pd.DataFrame(data=[detection], columns=out.columns)
		out = pd.concat([out, created], ignore_index=True)
		out.to_csv("./data/new_train.csv", index=False)
