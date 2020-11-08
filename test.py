

#Tumblr API
import os
from mimetypes import guess_type
from __init__ import tumblrLogin
from tumblpy import Tumblpy
import tumblr_photoset_upload

api = Tumblpy(tumblrLogin["consumerkey"] , tumblrLogin["consumersecret"], 
            tumblrLogin["oauthtoken"], tumblrLogin["oauthtokensecret"])

from pytumblr import TumblrRestClient
api = TumblrRestClient(tumblrLogin["consumerkey"] , tumblrLogin["consumersecret"], 
            tumblrLogin["oauthtoken"], tumblrLogin["oauthtokensecret"])



blog_url = api.info()
print(blog_url)
blogName = blog_url['user']['blogs'][0]['name']
def posts(directory, caption, tags, state):
    print ("Posting to: " + blog_url)
    photo = open(directory, 'rb')
    params = {'type':'photo', 'caption': caption, 
    'data': [photo, photo], 'state': state, 'tags': tags}
    post = api.post('post', blog_url=blog_url, params=params)
    print ("Post ID: " + str(post['id']))  # returns id if posted  successfully

#Creates a photo post using a source URL
api.create_photo(blogName, state="draft", tags=["testing", "ok"],
                    source="https://68.media.tumblr.com/b965fbb2e501610a29d80ffb6fb3e1ad/tumblr_n55vdeTse11rn1906o1_500.jpg")
imgs = []
imgs.append("D:\\Documents\\Liclipse Workspace\\AutoMadohomu\\files\\65263118_p0.jpg")
imgs.append("D:\\Pictures\\Saved Pictures\\Drawn\\lain\\20180528_165503.jpg")

#Creates a photo post using a local filepath
api.create_photo(blogName, state="draft", tags=["testing", "ok"],
                    tweet="Woah this is an incredible sweet post [URL]",
                    data="D:\\Pictures\\Saved Pictures\\Drawn\\lain\\20180528_165503.jpg")

#Creates a photoset post using several local filepaths
api.create_photo(blogName, state="draft", tags=["jb is cool"], ,
                    data=imgs,
                    caption="## Mega sweet kittens")
