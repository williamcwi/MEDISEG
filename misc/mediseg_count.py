import json

# Update the file path to your annotation.json file
annotation_file = "path_to_annotation_file"

# Load the COCO annotations
with open(annotation_file, "r") as f:
    data = json.load(f)

# The COCO file should have keys: "annotations" and "categories"
annotations = data.get("annotations", [])
categories = data.get("categories", [])

# Build a mapping from category_id to category name
cat_id_to_name = {cat["id"]: cat["name"] for cat in categories}

# Count the instances per category
instance_counts = {}
for ann in annotations:
    cat_id = ann["category_id"]
    instance_counts[cat_id] = instance_counts.get(cat_id, 0) + 1

if instance_counts:
    # Find the category with the lowest and highest number of instances
    lowest_cat_id = min(instance_counts, key=lambda cid: instance_counts[cid])
    highest_cat_id = max(instance_counts, key=lambda cid: instance_counts[cid])
    
    lowest_name = cat_id_to_name.get(lowest_cat_id, str(lowest_cat_id))
    highest_name = cat_id_to_name.get(highest_cat_id, str(highest_cat_id))
    
    print(f"Category with the lowest instances: {lowest_name} (ID: {lowest_cat_id}) with {instance_counts[lowest_cat_id]} instances")
    print(f"Category with the highest instances: {highest_name} (ID: {highest_cat_id}) with {instance_counts[highest_cat_id]} instances")
else:
    print("No annotations found in the file.")
