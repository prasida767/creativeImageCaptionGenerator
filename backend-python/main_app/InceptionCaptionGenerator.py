import numpy as np
from PIL import Image
from keras.applications.inception_v3 import InceptionV3


def extract_features(filename, model):
    try:
        image = Image.open(filename)
    except (FileNotFoundError, OSError) as e:
        print(f"ERROR: Couldn't open image! {e}")
        return None
    image = image.resize((299, 299))
    image = np.array(image)
    # for images that has 4 channels, we convert them into 3 channels
    if image.shape[2] == 4:
        image = image[..., :3]
    image = np.expand_dims(image, axis=0)
    image = image / 127.5
    image = image - 1.0
    feature = model.predict(image)
    return feature


def photoFeatureExtractor(image):
    inception_model = InceptionV3(include_top=False, pooling="avg")
    photo = extract_features(image, inception_model)
    return photo
