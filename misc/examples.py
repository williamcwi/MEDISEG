import json
import os
import random
import shutil
from collections import defaultdict

# Paths (UPDATE THESE)
annotation_file = "annotations.json"  # Path to COCO annotation file
image_dir = "./images"  # Directory containing original images
output_dir = "./preview_images"  # Output directory for selected preview images

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load COCO annotations
with open(annotation_file, "r") as f:
    coco_data = json.load(f)

# Step 1: Count instances per image
image_instance_count = defaultdict(list)
for ann in coco_data["annotations"]:
    image_id = ann["image_id"]
    category_id = ann["category_id"]
    image_instance_count[image_id].append(category_id)

# Step 2: Identify single-instance images for each category
single_pill_images = defaultdict(list)
for image_id, categories in image_instance_count.items():
    if len(categories) == 1:  # Ensure it's a single-pill image
        category_id = categories[0]
        single_pill_images[category_id].append(image_id)

# Step 3: Select 10 samples per category
selected_images = {}
for category_id, image_list in single_pill_images.items():
    if len(image_list) >= 10:
        selected_images[category_id] = random.sample(image_list, 10)
    else:
        selected_images[category_id] = image_list  # Keep all if less than 10 available

# Step 4: Convert image IDs to file names
image_id_to_filename = {img["id"]: img["file_name"] for img in coco_data["images"]}

# Step 5: Copy selected images to output directory and rename
for category_id, image_list in selected_images.items():
    for idx, image_id in enumerate(image_list, start=1):
        original_filename = image_id_to_filename[image_id]
        original_path = os.path.join(image_dir, original_filename)
        
        # New filename format: "categoryID_index.jpg" (e.g., "3_01.jpg")
        new_filename = f"{category_id:02d}_{idx:02d}.jpg"
        new_path = os.path.join(output_dir, new_filename)
        
        # Copy and rename file
        if os.path.exists(original_path):
            shutil.copy(original_path, new_path)
            print(f"Copied {original_filename} → {new_filename}")
        else:
            print(f"Warning: File {original_filename} not found in {image_dir}")

print(f"\n✅ All selected images have been copied and renamed in {output_dir}.")
