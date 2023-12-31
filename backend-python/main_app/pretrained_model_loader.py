from keras.applications.xception import Xception
# small library for seeing the progress of loops.
from tqdm import tqdm_notebook as tqdm
import PreprocessDataset

import string
import numpy as np
from PIL import Image
import os
from pickle import dump, load
import numpy as np


def extract_features(directory):
    model = Xception(include_top=False, pooling='avg')
    featureVectors = {}
    for img in tqdm(os.listdir(directory)):
        filename = directory + "/" + img
        image = Image.open(filename)
        image = image.resize((299, 299))
        image = np.expand_dims(image, axis=0)
        # image = preprocess_input(image)
        image = image / 127.5
        image = image - 1.0
        feature = model.predict(image)
        featureVectors[img] = feature
    return featureVectors


# 2048 feature vector
features = extract_features('/cicg/Images')
dump(features, open("features.p", "wb"))
