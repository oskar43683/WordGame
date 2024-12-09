import json

# Function to read word pairs from a text file and save as JSON
def convert_txt_to_json(input_file, output_file):
    words = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            english, polish = line.strip().split('/')
            words.append({'english': english, 'polish': polish})

    # Write the JSON data to a file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump({'words': words}, json_file, ensure_ascii=False, indent=4)

# Convert word list in words.txt to words.json
convert_txt_to_json('from_txt_to_json.txt', 'levels/39level.json')
