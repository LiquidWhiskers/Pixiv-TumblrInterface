import os
from configparser import ConfigParser

#Import Config
config = ConfigParser()
if os.path.exists('config') != True:    
    sections = {"Pixiv":{}, "Tumblr":{}, "Downloading":{}, 
            "Directories":{}, "Formatting":{}, "Extras":{}}
    for section in sections:
        print(section)
    config.add_section(section)
    for option in sections[section]:
        config.set(section,option,sections[section][option])
        
config.read('config')
pixivLogin = config.items("Pixiv")
pixivLogin = dict(pixivLogin)
tumblrLogin = config.items("Tumblr")
tumblrLogin = dict(tumblrLogin)

