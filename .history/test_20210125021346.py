import requests


url = 'http://127.0.0.1:5000/apis/conversation/'
myobj = {
    "conversation_id":1,
    "message_question":"như nào đây anh"
}
x = requests.post(url, data = myobj)

print(x.text)