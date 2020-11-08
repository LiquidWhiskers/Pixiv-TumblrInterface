from pixiv import pixivImage
from tumblr import Queues
import os
cwd = os.getcwd()
image = pixivImage(59901002)

PMMMM = {"Madoka Magica":"puella magi madoka magica, mahou shoujo madoka magica, pmmm, pmmm rebellion, pixiv",
    "madohomu":"Madohomu, Madoka Kaname, Homura Akemi, yuri",
    "kyosaya":"Kyosaya,Kyoko Sakura, Sayaka Miki, yuri",
    "godoka":"Goddess Madoka, Godoka",
    "homucifer":"Homucifer, Devil Homura"} 

batch = Queues("mamiayame")
batch.addImages(False, image)
batch.tagTriggers('D:\\Documents\\Liclipse Workspace\\AutoMadohomu\\tags.csv', csv=True, overwrite=True)
batch.tagTriggers(PMMMM)
batch.formatCaptions("{link} by {}", batch.link(image.title,image.URL), batch.link(image.name, image.user_URL))
batch.postAll("draft")



