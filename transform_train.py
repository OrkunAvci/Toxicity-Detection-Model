from api.perspective import Detector
import pandas as pd

df = pd.read_csv("./data/train.csv")
out = pd.read_csv("./data/new_train.csv")

detector = Detector()
for text in df.loc[ len(out.loc[:,"Comment"].array) : ,"comment_text"].array:
	detection = detector.detect(text)
	if detection:
		out.loc[out.shape[0]] = dict(zip(out.columns, detection))
		out.to_csv("./data/new_train.csv", index=False)
