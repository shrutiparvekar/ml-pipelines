import requests

# Define the URL of the translation service
translation_url = "http://localhost:8000/summarize"

# Open and read the random_strings.txt file
with open('input.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Open an output file for writing
with open('translated_strings.txt', 'w', encoding='utf-8') as output_file:
    # Iterate through each line and make API calls for translation
    for line in lines:
        text = line.strip()  # Remove leading/trailing whitespace
        response = requests.post(translation_url, json={"text": text, "should_translate": True})

        if response.status_code == 200:
            translated_text = response.text
            output_file.write(f"Original: {text}\n")
            output_file.write(f"Translation: {translated_text}\n")
            output_file.write("----\n")
        else:
            output_file.write(f"Error translating text: {text}\n")
