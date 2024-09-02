Stable Diffusion Image Tagging Script

This script is designed to assist users in generating AI images using Stable Diffusion by automating the process of retrieving tags from Gelbooru. The script extracts relevant tags for images, which can be used as a base for diffusion creation.
How It Works

  1. Visit Gelbooru: Browse the Gelbooru website and find an image or a set of images that you'd like to use as a base for your Stable Diffusion creations.
  2. Download Images: Download the full image(s) to a folder on your computer. Ensure that the image filename is left as the original 32-character string. Images starting with _sample or those that do not conform to this naming convention will not be processed correctly.
  3. Run the Script: Place the script in the folder containing your images and run it.
  4. Generate Tag Files: The script will generate a text file for each valid image, containing all the tags associated with that image.

Features

  - Tag Filtering: The script uses three JSON files (restricted_artists.json, restricted_copyrights.json, restricted_meta.json, restricted_tags.json) that contain tags to be ignored. If you want to disable any of these filters, simply rename the corresponding JSON file by adding .disabled to the end of the filename.
  - Invalid Filenames: Images that do not have the correct filename format (i.e., a valid 32-character hash) will be moved to a folder named invalid_hashes.
  - Unavailable Images: If an image has a valid hash but is no longer available on Gelbooru, it will be skipped, and a message will be logged in the console.
  - Skipping Existing Tags: If a text file already exists for an image, the script will skip that image, preventing duplicate work.
  - Supported File Types: The script processes the following file types: .png, .jpg, .jpeg, .gif, .mp4.

Dependencies

This script requires the requests library. You can install it via pip:

    pip install requests

Usage

  1. Download and place your images in a folder.
  2. Ensure the script and any necessary JSON files are in the same folder.
  3. Run the script within the folder.


    python fetch_image_tags.py

Notes

  - JSON Files: You can customize the restricted_tags JSON file to include or exclude specific tags by editing their contents. If you wish to disable a particular category of restricted tags, simply rename the corresponding JSON file (e.g., restricted_artists.json to restricted_artists.json.disabled).
  - Error Handling: The script logs any errors or skipped images in the console, allowing you to track which images were not processed.

This script simplifies the process of preparing images for Stable Diffusion by automatically fetching and filtering relevant tags, helping you focus on creativity.
