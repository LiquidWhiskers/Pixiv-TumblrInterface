from csv import reader
from pixiv import pixivImage

#Tumblr API
from __init__ import tumblrLogin
from pytumblr import TumblrRestClient
from docutils.nodes import caption

#Queue for pixivImages
class Queues():
    #Either blog name or url
    def __init__(self, *args):
        self.api = TumblrRestClient(tumblrLogin["consumerkey"] , tumblrLogin["consumersecret"], 
            tumblrLogin["oauthtoken"], tumblrLogin["oauthtokensecret"])
        self.clientInfo = self.api.info()
        self.blogs= self.clientInfo['user']['blogs']
        for arg in args:
            if arg.find("http", 0, len(arg)) != -1:
                self.blog = self.findBlog(arg, True)
            else:
                self.blog = self.findBlog(arg, False)
        self.queue = []
        self.batch = []
        self.state = "draft"
        self.number = 0
        self.name = ""
        
        

    def findBlog(self, arg, url):
        blogNumber = 0
        read = True
        while read == True:
            try:
                if url:
                    if self.blogs[blogNumber]['url'] == arg:
                        return self.blogs[blogNumber]['name']
                else:
                    if self.blogs[blogNumber]['name'] == arg:
                        return self.blogs[blogNumber]['name']
                blogNumber = blogNumber + 1
            except IndexError:
                read = False
                print("Blog not found, check your URL or name")
                
    #Add CSV to queue            
    def csvQueue(self, csvFile):
        with open(csvFile, newline='',encoding='utf-8') as csvfile:
            reader = reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row == "":
                    print("Skipping Empty Row")
                else:
                    self.addImages(row[0])
                self.numberImages = self.numberImages + 1
    def addImages(self, overwrite=False, *args, **kwargs):
        for arg in args:
            if isinstance(arg, pixivImage):
                if overwrite:
                    self.queue = [arg]
                else:
                    self.queue.append(arg)
        for kwarg in kwargs.keys():
            self.csvQueue(kwargs[kwarg])
            
    #Adds caption text, or keyworded text to be added when posted
    def link(self, text, link):
        return "<a href={}>{}</a>".format(link, text)
    
    #Takes dictionary or csv as {"trigger":"Tag to be added when triggered"}
    def tagTriggers(self, triggers, csv=False, overwrite=False, batch=None,):
        tempTags = []
        if batch == None:
            batch = self.queue
        if csv:
            with open(triggers, newline='',encoding='utf-8') as csvfile:
                csvReader = reader(csvfile, delimiter=',', quotechar='|')
                triggers = {}
                for row in csvReader:
                    triggers[row[0]] = row[1]
        for image in batch:
            image.importIllustJSON()
            totaltags = image.tags
            for tag in image.userTags:
                totaltags.append(tag)
                
            for trigger in triggers.keys():
                for tag in totaltags:
                    if trigger == tag:
                        tempTags.append(triggers[tag])
                        
            if overwrite:
                image.setCustomTags(tempTags)
            else:
                for tag in image.userTags:
                    tempTags.append(tag)
                image.setCustomTags(tempTags)    
        
    #Adds default caption       
    def addCaption(self):
        for image in self.queue:
            image.setCaption("{} by {}".format(self.link(image.title,image.URL),
                                          self.link(image.name, image.user_URL)))
    def formatCaptions(self, text, *args):
        caption_format = args
        for image in self.queue:
            try:
                print(text)
                print(caption_format)
                print(text.format(caption_format))
                image.setCaption(text.format(caption_format))
            except AttributeError:
                try:
                    self.getArtist(pixivImage)
                    image.setCaption(text.format(caption_format))
                except:
                    print("Invalid arguments for caption")
    #Manually artist information for pixivImage
    def getArtistWebsite(self, pixivImage):
        website = pixivImage.webpage
        if website.find("twittee") != -1:
            return "https://twitter.com/intent/follow?user_id=" + pixivImage.twitter_id
        elif website.find("tumblr") != -1:
            username = self.api.blog_info(website)['name']
            return "https://www.tumblr.com/follow/" + username
        else: 
            pass;
    def postList(self, images, blogName, state):
        rowcurrent = 0
        rowsum = len(images)
        for image in images:
            rowcurrent = rowcurrent + 1
            try:
                imageCaption = image.caption 
            except AttributeError:
                imageCaption = ""
            print ("({}/{}) Downloading: {} by {}".format(
                rowcurrent, rowsum, image.title, image.name))
            if image.directories == []:
                image.download()
            print ("Posting to " + blogName + " as " + state)  
            print ("Caption: " + imageCaption)  
            print ("Tags: " + str(image.userTags))
            self.api.create_photo(blogName, state=state, format="markdown", tags=image.userTags,
                    caption=str(image.caption), data=image.directories)
            print ("")
            if rowcurrent == rowsum:
                print("Done!")
        
    def postAll(self, state):
        self.postList(self.queue, self.blog, state)
                
        