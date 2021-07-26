import requests

url = "http://127.0.0.1:5000/"
# x = requests.put(url + "video/1", data = {
#     "name":"I love you",
#     "likes": 4,
#     "views":103566579    
# })

#print(x.json())
print(requests.get(url + "video/1").json())