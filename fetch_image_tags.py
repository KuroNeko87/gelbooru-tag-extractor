import os
import json
import requests
import shutil

allowed_characters = set('abcdefghijklmnopqrstuvwxyz0123456789')

def load_restricted_tags(json_files):
    """Load restricted tags from multiple JSON files."""
    restricted_tags = set()
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            restricted_tags.update(data.get("restricted_tags", []))
    return restricted_tags

def fetch_tags_for_hash(hash, restricted_tags):
    url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=md5:{hash}"
    try:
        req = requests.get(url)

        # Check if the response is empty
        if not req.text.strip():
            raise ValueError("Empty response from API")

        data = req.json()

        if data["@attributes"]["count"] > 1:
            return "No image found with that hash..."
        else:
            post = data.get("post")
            if not post:
                raise ValueError("Error fetching tags: 'post'")

            tags = post[0]["tags"]
            parsed = []
            for tag in tags.split():
                if tag not in restricted_tags:
                    parsed.append(tag)
            parsed = ", ".join(parsed)
            return parsed
    except ValueError as ve:
        print(f"Error fetching tags for hash {hash}: {ve}")
        return None
    except requests.exceptions.RequestException as re:
        print(f"Request error fetching tags for hash {hash}: {re}")
        return None
    except json.JSONDecodeError as je:
        print(f"JSON decode error fetching tags for hash {hash}: {je}")
        return None

def process_images_in_directory(directory, restricted_tags):
    invalid_hashes_dir = os.path.join(directory, 'invalid_hashes')
    os.makedirs(invalid_hashes_dir, exist_ok=True)

    for root, dirs, files in os.walk(directory):
        # Skip the invalid_hashes directory
        if os.path.basename(root) == 'invalid_hashes':
            continue

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4')):
                image_path = os.path.join(root, file)
                hash = os.path.splitext(file)[0]  # Get the hash from the filename

                # Check if the file name is 32 characters long and contains only allowed characters
                if len(hash) == 32 and all(c in allowed_characters for c in hash):
                    txt_filename = os.path.join(root, f"{hash}.txt")

                    # Skip tag retrieval if a text file for the hash already exists
                    if os.path.exists(txt_filename):
                        print(f"Tag file already exists for {hash}, skipping tag retrieval.")
                        continue

                    tags = fetch_tags_for_hash(hash, restricted_tags)
                    if tags:
                        with open(txt_filename, 'w') as txt_file:
                            txt_file.write(tags)
                        print(f"Tags written to {txt_filename}")
                else:
                    print(f"Invalid hash for file {file}, moving to {invalid_hashes_dir}.")
                    shutil.move(image_path, os.path.join(invalid_hashes_dir, file))

if __name__ == "__main__":
    current_directory = os.getcwd()

    # Define the paths to the restricted tags JSON files
    json_files = [
        os.path.join(current_directory, 'restricted_artists.json'),
        os.path.join(current_directory, 'restricted_copyrights.json'),
        os.path.join(current_directory, 'restricted_meta.json'),
        os.path.join(current_directory, 'restricted_tags.json')
    ]

    # Load restricted tags from the three files
    restricted_tags = load_restricted_tags(json_files)

    # Process images and filter tags based on the restricted tags
    process_images_in_directory(current_directory, restricted_tags)
    print("Process completed.")
