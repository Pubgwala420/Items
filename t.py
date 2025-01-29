import json
import os
import requests

# Load the existing log if available
if os.path.exists('Items/log.json'):
    with open('Items/log.json', 'r') as log_file:
        processed_items = json.load(log_file)
else:
    processed_items = {}

# Load JSON data
with open('Upto OB47 Item ID.json', 'r') as file:
    data = json.load(file)

# Create directories if they don't exist
os.makedirs('Items/ob', exist_ok=True)
os.makedirs('Items/bb', exist_ok=True)

# Iterate through each item in the JSON
for item in data:
    item_id = item.get('Item_ID')
    icon_name = item.get('Icon_Name')

    # Skip already processed items
    if item_id in processed_items:
        print(f"Skipping Item_ID: {item_id}, already processed.")
        continue

    # Construct the API URL
    api_url = f"https://ff-community-api.vercel.app/icons?id={item_id}"

    try:
        # Fetch the image
        response = requests.get(api_url)
        response.raise_for_status()

        # Save image as {item_id}.png in Items/ob
        with open(f'Items/ob/{item_id}.png', 'wb') as ob_file:
            ob_file.write(response.content)

        # Save image as {icon_name}.png in Items/bb
        with open(f'Items/bb/{icon_name}.png', 'wb') as bb_file:
            bb_file.write(response.content)

        # Log the processed item
        processed_items[item_id] = {
            "Icon_Name": icon_name
        }

        # Save the updated log to Items/log.json
        with open('Items/log.json', 'w') as log_file:
            json.dump(processed_items, log_file, indent=4)

        print(f"Downloaded and saved images for Item_ID: {item_id}, Icon_Name: {icon_name}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image for Item_ID: {item_id}. Error: {e}")
