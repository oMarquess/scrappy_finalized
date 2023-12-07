import os
import json

def merge_json_files(folder_path, output_file, ignore_file='banners.json'):
    merged_data = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and filename != ignore_file:
            file_path = os.path.join(folder_path, filename)

            # Open and load the JSON data with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data.extend(data)

    # Write the merged data to the output file with utf-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, indent=4)

    print(f"Merged JSON data written to {output_file}")

# Merge all the products in FrankoTrading call it database_A

#merge_json_files('./data/frankotrading', './demo/database/database_A.json')

# Merge all the products in Compughana call it database_B
merge_json_files('./data/compughana', './demo/database/database_B.json')