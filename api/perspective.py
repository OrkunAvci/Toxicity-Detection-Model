from asyncio import to_thread
from time import sleep
from googleapiclient import discovery, errors
import json
import pprint


class Detector:
	__api_key = None
	__client = None

	def __init__(self) -> None:
		with open("config.json", "r") as f:
			config = json.loads(f.read())
			self.__api_key = config["PERSPECTIVE_API_KEY"]
			self.__req_attr = config["REQUEST_ATTRIBUTES"]
		self.__client = discovery.build(
			"commentanalyzer",
			"v1alpha1",
			developerKey=self.__api_key,
			discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
			static_discovery=False,
		)

	def detect(self, text: str):
		request = self.make_request_body(text)
		# print(json.dumps(identity, indent=4))
		# print(json.dumps(request, indent=4))
		try:
			response = self.__client.comments().analyze(body = request).execute()
			return self.handle_response(text, response)
		except errors.HttpError as e:
			if e.status_code == 429:
				print("Waiting for cooldown...")
				sleep(70)
				return self.detect(text = text)
			else:
				pass
				# print(e.error_details[0]["errorType"])

	def make_request_body(self, text: str)-> dict:
		return {
				"comment": {"text": text},
				"requestedAttributes": self.__req_attr
			}

	def handle_response(self, text: str, response: dict):
		scores = []
		for key in self.__req_attr:
			scores.append(response["attributeScores"][key]["summaryScore"]["value"])
		to_return = [text]
		to_return.extend(scores)
		return to_return

