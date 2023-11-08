import requests
import concurrent.futures

summarization_url = "http://localhost:8000/summarize"

def summarize(text):
    response = requests.post(summarization_url, json={"text": text, "should_translate": False})
    if response.status_code == 200:
        summarized_text = response.text
        return f"Original: {text}\nTranslation: {summarized_text}\n----\n"
    else:
        return f"Error translating text: {text}\n"

with open('./input/input.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Open an output file for writing
with open('./output/output_summarize.txt', 'w', encoding='utf-8') as output_file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=75) as executor:
        translated_results = executor.map(summarize, (line.strip() for line in lines))

        for result in translated_results:
            output_file.write(result)
