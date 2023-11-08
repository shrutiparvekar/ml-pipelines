import requests

text = "Hello, the weather is quite fine today!"
resp = requests.post("http://localhost:8000/translate", json={"text": text})

print(resp.text)
# 'Hallo, das Wetter ist heute ziemlich gut!'
