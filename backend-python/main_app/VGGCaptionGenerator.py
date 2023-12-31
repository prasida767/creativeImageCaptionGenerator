from pickle import load

from keras import Input
from keras.src.layers import Flatten, Dense
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
import numpy as np
from PIL import Image


# extract features from each photo in the directory
def extract_features(filename, base_model):
    # Add a Flatten layer to get a (4096,) feature vector
    flat = Flatten()(base_model.layers[-1].output)

    # Add a Dense layer to get a (None, 4096) feature vector
    dense = Dense(4096, activation='relu')(flat)

    # Create a new model with the Flatten and Dense layers
    model = Model(inputs=base_model.input, outputs=dense)

    try:
        image = Image.open(filename)
    except (FileNotFoundError, OSError) as e:
        print(f"ERROR: Couldn't open image! {e}")
        return None

    image = image.resize((224, 224))
    image = np.array(image)
    if image.shape[2] == 4:
        image = image[..., :3]
    image = np.expand_dims(image, axis=0)
    # image = preprocess_input(image)
    feature = model.predict(image)
    return feature


def photoFeatureExtractor(image):
    vgg16_model = VGG16(include_top=False, input_tensor=Input(shape=(224, 224, 3)))
    photo = extract_features(image, vgg16_model)
    return photo
