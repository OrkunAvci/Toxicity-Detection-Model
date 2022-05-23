from pprint import pprint
from time import sleep
from googleapiclient import discovery
import json
from .perspective import Detector


class Youtube:
	__api_key = None
	__client = None
	__detector = None

	def __init__(self) -> None:
		with open("config.json", "r") as f:
			config = json.loads(f.read())
			self.__api_key = config["YOUTUBE_API_KEY"]
		self.__client = discovery.build("youtube", "v3", developerKey=self.__api_key)
		self.__detector = Detector()

	def get_comments_batch(self, id):
		response = (
			self.__client.commentThreads()
			.list(
				part= "snippet",
				videoId= id,
				maxResults= 60
			)
			.execute()
		)
		return response["items"]

	def get_comments(self, id)-> list:
		all_comments = []
		request = self.__client.commentThreads().list(
			part= "snippet", 
			videoId= id,
			maxResults= 60
		)
		response = request.execute()

		while response:
			for comment in response["items"]:
				all_comments.append(comment["snippet"]["topLevelComment"])
				if comment["snippet"]["totalReplyCount"] > 0:
					replies = self.get_replies(comment["id"])
					all_comments.extend(replies)
			
			if "nextPageToken" in response:
				response = (
					self.__client.commentThreads()
					.list(
						part= "snippet",
						videoId= id,
						pageToken= response["nextPageToken"]
					)
					.execute()
				)
			else:
				break
		
		print("Total number of comments returned: ", len(all_comments))
		return [comment["snippet"]["textOriginal"] for comment in all_comments]
	
	def get_replies(self, parent_id: str)-> list:
		replies = []
		request = self.__client.comments().list(
			part= "snippet", 
			parentId= parent_id
		)
		response = request.execute()

		while response:
			replies.extend(response["items"])
			
			if "nextPageToken" in response:
				response = (
					self.__client.comments()
					.list(
						part= "snippet",
						parentId= parent_id,
						pageToken= response["nextPageToken"]
					)
					.execute()
				)
			else:
				break

		return replies

	def process_comments(self, comments):
		out = []
		for comment in comments:
			if comment["kind"] == "youtube#commentThread":
				comment = comment["snippet"]["topLevelComment"]
			text = comment["snippet"]["textOriginal"]
			detection = self.__detector.detect(text)
			if detection:
				out.append(detection)
		return out
