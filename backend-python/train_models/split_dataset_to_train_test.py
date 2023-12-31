import os
import random
from itertools import islice


def caption_train_test(uniqueValue, captions_file, output_dir, train_size=200, test_size=100):
    # Read the captions.txt file to get image names and captions
    print(captions_file)
    with open(captions_file, 'r') as file:
        # Skip the first line (header)
        lines = islice(file, 1, None)
        lines = list(lines)

    # Create a dictionary to group captions by image name
    image_captions = {}
    for line in lines:
        image_name, caption = line.strip().split(',', 1)
        image_captions.setdefault(image_name, []).append(caption)

    # Shuffle the image names to randomly select images for train and test sets
    image_names = list(image_captions.keys())
    random.shuffle(image_names)

    # Create output directories for train and test sets
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Save train captions to file
    train_samples = image_names[:train_size]
    with open(os.path.join(train_dir, f'train_captions_{uniqueValue}.txt'), 'w') as train_file:
        for image_name in train_samples:
            for caption in image_captions[image_name]:
                train_file.write(f"{image_name},{caption}\n")

    # Save test captions to file
    test_samples = image_names[train_size:train_size + test_size]
    with open(os.path.join(test_dir, f'test_captions_{uniqueValue}.txt'), 'w') as test_file:
        for image_name in test_samples:
            for caption in image_captions[image_name]:
                test_file.write(f"{image_name},{caption}\n")

    return f'train_captions_{uniqueValue}.txt', f'test_captions_{uniqueValue}.txt'

