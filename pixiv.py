import os
from pixivpy3 import PixivAPI, AppPixivAPI
from __init__ import pixivLogin

#Main Pixiv Image Wrapper class
#Supports most of the JSON fields
#
#

class pixivImage:
	#Takes URL or ID as argument
	def __init__(self, *args):
		baseURL = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
		self.image_URLs = [] 
		self.directories = []
		self.caption = ""
		self.userTags = []
		self.userImported = False
		for arg in args:
			length = len(str(arg))
			#If it is an ID, it is 8 digits long and an int
			if length == 8:
				self.ID = int(arg)
				self.URL = baseURL + str(arg) 
			#If it's a url, it's the baseURL plus the int
			elif isinstance(arg, str) & length == len(baseURL) + 8:
				self.URL = arg
				try:
					self.ID = self.url[self.url.find("&illust_id=",0 ,length) + len("&illust_id="):length]
				except TypeError:
					print("URL is malformed")
				#Fix minor bad URL
				self.URL = baseURL + str(arg["ID"])
			else:
				print("URL OR ID is wrong or in bad format")
	#Gets PixixImage attribute
	def __get__(self, obj, objtype):
		#Tries to get attribute, if it does not exist, cycles through imports then outputs error
		try:
			return getattr(obj, self.attr)
		except AttributeError:
			try:
				self.importIllustJSON()
				return self.item 
			except AttributeError:
				try:
					self.importUserJSON()
				except AttributeError:
					print("Image does not have that attribute")
					pass
	def setCustomTags(self, tags):
		self.userTags = tags
	def setCaption(self, caption):
		self.caption = caption
	#Import info using pixivAPI into class from JSON
	def importIllustJSON(self):
		#Login to Pixiv API
		self.api = PixivAPI()
		self.api.login(pixivLogin["pixivusername"], pixivLogin["pixivpassword"])
		userURL = "https://www.pixiv.net/member_id="
		self.JSON = self.api.works(self.ID)['response'][0]
		self.manga = self.JSON['is_manga']
		self.account = self.JSON['user']['account']
		self.name = self.JSON['user']['name']
		self.user_ID = self.JSON['user']['id']
		self.user_URL = userURL + str(self.user_ID)
		self.title = self.JSON['title']
		self.tags = self.JSON['tags']
		self.pages = self.JSON['page_count']
		if self.pages > 1:
			for page in range(self.pages-1):
				self.image_URLs.append(self.JSON['metadata']["pages"][page]["image_urls"]['large'])
		else:
			self.image_URLs.append(self.JSON['image_urls']['large'])
			
	#Imports JSON with user information.
	def importUserJSON(self):
		#Non-authenticated API login
		aapi = AppPixivAPI() 
		self.userJSON = aapi.user_detail(self.user_ID)
		self.webpage = self.userJSON['profile']['webpage']
		self.twitter_name = self.userJSON['profile']['twitter_account']
		self.twitter_URL = self.userJSON['profile']['twitter_url']
		self.pawoo_URL = self.userJSON['profile']['pawoo_url']
		self.userImported = True
	#Manually import JSON information
	def importJSON(self):  
		self.importIllustJSON()
		self.importUserJSON()
	#Downloads images to directory
	def download(self, directory=None):
		for URL in self.image_URLs:
			if directory is None:
				directory = os.path.dirname(os.path.abspath(__file__)) + "\\temp\\"
				if not os.path.exists(directory):
					os.makedirs(os.path.dirname(directory))
				self.api.download(URL,prefix=directory)
			else:
				if not os.path.exists(directory):
					os.makedirs(directory)
				self.api.download(URL,prefix=directory)
				directory = directory + "\\" + str(os.path.basename(URL))
				self.directories.append(directory)
				self.api.download(URL)
			



