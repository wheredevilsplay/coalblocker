import requests
import re
from bs4 import BeautifulSoup
import base64

#TODO
# if last scrapped post doesnt exist default to 1

# get last scrapped post
f = open("lastScrapped.txt", "r")
firstPost = f.read()

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
        md5NotEncoded = negro['src']
        md5NotEncoded = re.findall(r'[0-9a-f]{32}', md5NotEncoded)
        md5NotEncoded = md5NotEncoded[0] 
        md5NotEncoded = bytes.fromhex(md5NotEncoded)
        md5Encoded = base64.b64encode(md5NotEncoded).decode()
        md5Encoded = "/" + md5Encoded + "/"
        print(str(x) + " " + md5Encoded)
        with open("md5.txt", "a") as file_object:
            file_object.write(md5Encoded + "\n")
        with open("lastScrapped.txt", "w") as file_object:
            file_object.write(str(x))
    except:
        pass