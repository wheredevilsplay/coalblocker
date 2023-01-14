import requests
import re
from bs4 import BeautifulSoup
import base64

# get last scrapped post
try: 
    f = open("lastScrapped.txt", "r")
    firstPost = f.read()
except:
    firstPost = 1

# get last post
mainBooru = requests.get("https://booru.soy/post/list")
soup = BeautifulSoup(mainBooru.text, features="lxml")
negro = soup.find("a", class_="shm-thumb-link")
lastPost = negro["data-post-id"]

# scrapper 
for x in range(int(firstPost), int(lastPost)):
    try:
        posts = "https://booru.soy/post/view/" + str(x)
        request = requests.get(posts)
        soup = BeautifulSoup(request.text, features="lxml")
        negro = soup.find("img", class_="shm-main-image")
        md5 = negro['src']
        md5 = re.findall(r'[0-9a-f]{32}', md5)
        md5 = md5[0] 
        md5 = bytes.fromhex(md5)
        md5 = base64.b64encode(md5).decode()
        md5 = "/" + md5 + "/"
        print(str(x) + " " + md5)
        with open("md5.txt", "a") as file_object:
            file_object.write(md5 + "\n")
        with open("lastScrapped.txt", "w") as file_object:
            file_object.write(str(x))
    except:
        pass

# would be better to do what anons said and make a machine learning filter like NSFW Filter extension to effectivly block wojaks