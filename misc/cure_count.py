import os

# Replace with the path to your local 'pill-images' directory
base_dir = "path_to_images"
counts = {}

# Iterate over each category folder (named 0, 1, ..., 195)
for category in os.listdir(base_dir):
    category_path = os.path.join(base_dir, category)
    if os.path.isdir(category_path):
        total = 0
        details = {}
        for side in ['top', 'bottom']:
            side_path = os.path.join(category_path, side)
            if os.path.isdir(side_path):
                for subfolder in ['Reference', 'Customer']:
                    folder_path = os.path.join(side_path, subfolder)
                    if os.path.isdir(folder_path):
                        # Count files that are images (assuming common extensions)
                        num_images = len([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                        details[f"{side}_{subfolder}"] = num_images
                        total += num_images
        counts[category] = {"total": total, "details": details}

# Print the results
for cat, info in sorted(counts.items(), key=lambda x: int(x[0])):
    print(f"Category {cat}: Total images = {info['total']}, Breakdown = {info['details']}")

# Find the category with the lowest and highest total images
if counts:
    lowest_cat = min(counts, key=lambda cat: counts[cat]["total"])
    highest_cat = max(counts, key=lambda cat: counts[cat]["total"])
    print("\nSummary:")
    print(f"Lowest total images: Category {lowest_cat} with {counts[lowest_cat]['total']} images")
    print(f"Highest total images: Category {highest_cat} with {counts[highest_cat]['total']} images")
else:
    print("No categories found.")