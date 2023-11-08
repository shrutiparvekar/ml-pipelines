import requests
import concurrent.futures

translation_url = "http://localhost:8000/classify"

def classify(text):
    response = requests.post(translation_url, json={"text": text, "should_translate": True})
    if response.status_code == 200:
        translated_text = response.text
        return f"Original: {text}\nTranslation: {translated_text}\n----\n"
    else:
        return f"Error translating text: {text}\n"

with open('./input/input.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Open an output file for writing
with open('./output/output_classify.txt', 'w', encoding='utf-8') as output_file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        translated_results = executor.map(classify, (line.strip() for line in lines))

        for result in translated_results:
            output_file.write(result)
