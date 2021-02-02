import requests


url = 'http://127.0.0.1:5000/apis/conversation/'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, data = myobj)

print(x.text)