import requests

text = "Hello, the weather is quite fine today!"
resp = requests.post("http://localhost:8000/summarize", json={"text": text, "should_translate": False})

print(resp.text)
# 'Hallo, das Wetter ist heute ziemlich gut!'
