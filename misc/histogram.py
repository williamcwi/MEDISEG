import json
import matplotlib.pyplot as plt
from collections import Counter

# Path to your COCO annotation file
annotation_file = "annotations.json"  # Update with your actual file path

# Load COCO annotations
with open(annotation_file, "r") as f:
    coco_data = json.load(f)

# Extract image IDs and count the number of annotations per image
image_instance_count = Counter()
for ann in coco_data["annotations"]:
    image_id = ann["image_id"]
    image_instance_count[image_id] += 1

# Count how many images have 1, 2, ..., 11 instances
instance_distribution = Counter(image_instance_count.values())

# Create a list for plotting (1 to 11 instances only)
max_instances = 11
instance_counts = [instance_distribution.get(i, 0) for i in range(1, max_instances + 1)]

# Create labels for x-axis
x_labels = [f"{i}" for i in range(1, max_instances + 1)]

# Plot histogram
plt.figure(figsize=(8, 5))
plt.bar(x_labels, instance_counts, color="skyblue", edgecolor="black")

# Set y-axis to log scale
plt.yscale("log")  # Change to "sqrt" if square root scale is preferred

# Label bars with their values
for i, count in enumerate(instance_counts):
    plt.text(i, count + 1, str(count), ha="center", fontsize=10)

# Formatting
plt.xlabel("Number of Instances per Image")
plt.ylabel("Number of Images")
plt.title("Instance Distribution")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
plt.show()
