import requests
import concurrent.futures

# Define the URL of the translation service
translation_url = "http://localhost:8000/translate"

# Function to perform the translation request
def translate(text):
    response = requests.post(translation_url, json={"text": text, "should_translate": True})
    if response.status_code == 200:
        translated_text = response.text
        return f"Original: {text}\nTranslation: {translated_text}\n----\n"
        # return "Original: " + text + " \nTranslation: " + translated_text + " \n----\n"
    else:
        return f"Error translating text: {text}\n"
        # return "Error translating text: " + text

# Open and read the input file
with open('inputtext2.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Open an output file for writing
with open('translated_strings2.txt', 'w', encoding='utf-8') as output_file:
    # Create a thread pool with 50 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Use the map function to apply the translate function to each line in parallel
        translated_results = executor.map(translate, (line.strip() for line in lines))

        # Write the results to the output file
        for result in translated_results:
            output_file.write(result)
