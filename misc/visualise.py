import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pycocotools.coco import COCO
import random

# Set paths to your image directory and annotation file
image_dir = "path/to/your/image_directory" # e.g., "F:/Downloads/test/images"
annotation_file = "path/to/annotation.json" # update with your annotation.json file
output_dir = "path/to/output/visualisations" # Directory where visualisations will be saved

os.makedirs(output_dir, exist_ok=True)

coco = COCO(annotation_file)

categories = coco.loadCats(coco.getCatIds())
cat_id_to_name = {cat["id"]: cat["name"] for cat in categories}

custom_colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 165, 255),
    (128, 0, 128),
    (203, 192, 255),
    (0, 255, 191),
    (128, 128, 0),
    (0, 128, 128),
    (42, 42, 165),
    (80, 127, 255),
    (128, 0, 0),
    (0, 215, 255),
    (130, 0, 75),
    (238, 130, 238),
    (208, 224, 64),
    (140, 230, 240),
    (214, 112, 218),
    (114, 128, 250),
    (205, 90, 106),
    (127, 255, 0),
    (30, 105, 210),
    (60, 20, 220),
    (0, 140, 255),
    (147, 20, 255),
    (34, 139, 34),
    (225, 105, 65),
    (219, 112, 147),
    (170, 178, 32)
]

# Create a color mapping for each category by cycling through the custom_colors list.
cat_ids = sorted(cat_id_to_name.keys())
cat_color_mapping = {}
for i, cat_id in enumerate(cat_ids):
    cat_color_mapping[cat_id] = custom_colors[i % len(custom_colors)]

# List available image files in the directory.
available_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Filter COCO image entries to those present in the directory.
available_images = []
for img_info in coco.loadImgs(coco.getImgIds()):
    if img_info['file_name'] in available_files:
        available_images.append(img_info)

for img_info in available_images:
    image_path = os.path.join(image_dir, img_info['file_name'])
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print(f"Error loading image: {image_path}")
        continue

    overlay = image_bgr.copy()

    # Get annotations for this image.
    ann_ids = coco.getAnnIds(imgIds=img_info['id'])
    anns = coco.loadAnns(ann_ids)

    # Process each annotation.
    for ann in anns:
        cat_id = ann["category_id"]
        color = cat_color_mapping.get(cat_id, (0, 255, 0))  # default to green if missing

        # Create binary mask from annotation.
        mask = coco.annToMask(ann)
        colored_mask = np.zeros_like(overlay, dtype=np.uint8)
        colored_mask[mask == 1] = color

        # Blend the colored mask with the image.
        alpha = 0.3
        overlay = cv2.addWeighted(overlay, 1.0, colored_mask, alpha, 0)

        # Draw the bounding box in black with a thinner line.
        bbox = ann.get("bbox", None)
        if bbox:
            x, y, w, h = map(int, bbox)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), color=(0, 0, 0), thickness=1)
            # Put the category name in the top-left corner of the bounding box.
            cat_name = cat_id_to_name.get(cat_id, str(cat_id))
            cv2.putText(overlay, cat_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), thickness=1)

    # Convert the final image from BGR to RGB for displaying with matplotlib.
    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 8))
    plt.imshow(overlay_rgb)
    plt.axis('off')
    
    output_path = os.path.join(output_dir, f"vis_{img_info['file_name']}")
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    print(f"Visualisation saved to {output_path}")