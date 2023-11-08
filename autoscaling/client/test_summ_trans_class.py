import requests
import concurrent.futures

translation_url = "http://localhost:8000/summarize"

def translate(text):
    response = requests.post(translation_url, json={"text": text, "should_translate": True})
    if response.status_code == 200:
        translated_text = response.text
        return f"Original: {text}\nTranslation: {translated_text}\n----\n"
    else:
        return f"Error translating text: {text}\n"

with open('./input/input.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

with open('./output/output.txt', 'w', encoding='utf-8') as output_file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        translated_results = executor.map(translate, (line.strip() for line in lines))

        for result in translated_results:
            output_file.write(result)
