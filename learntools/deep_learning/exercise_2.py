# This file is used by old notebooks (before DL micro-course was converted to LearnTools)

from IPython.display import Image, display

def visualize_results(images_paths, most_likely_labels):
	for i, img_path in enumerate(image_paths):
		display(Image(img_path))
		print(most_likely_labels[i])
