from api.perspective import Detector
import pandas as pd
import threading

CHUNK_SIZE = 1000
lock = threading.Lock()

df = pd.read_csv("./data/train.csv")
out = pd.read_csv("./data/new_train.csv")

logged = list(df.loc[:,"comment_text"].array)
processed = list(out.loc[:,"Comment"].array)

to_process = [comment for comment in logged if comment not in processed]

def chunks(seq, size):
    return list(seq[pos:pos + size] for pos in range(0, len(seq), size))

detector = Detector()
for chunk in chunks(to_process, CHUNK_SIZE):
	detections = []
	for text in chunk:
		detection = detector.detect(text)
		if detection:
			detections.append(detection)
	created = pd.DataFrame(data=detections, columns=out.columns)
	out = pd.concat([out, created], ignore_index=True)
	with lock:
		out.to_csv("./data/new_train.csv", index=False)
