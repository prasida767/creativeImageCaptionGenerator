from pickle import load, dump

from keras.preprocessing.text import Tokenizer
from djangoProject import settings


# Loading a text file into memory
def load_doc(filename):
    # Opening the file as read only
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text


# load the data
def load_photos(filename):
    file = load_doc(filename)
    photos = file.split("\n")
    return photos


def load_clean_descriptions(filename, photos):
    # loading clean_descriptions
    file = load_doc(filename)
    descriptions = {}
    for line in file.split("\n"):
        words = line.split()
        if len(words) < 1:
            continue
        image, image_caption = words[0], words[1:]
        if image in photos:
            if image not in descriptions:
                descriptions[image] = []
            desc = '<start> ' + " ".join(image_caption) + ' <end>'
            descriptions[image].append(desc)
    return descriptions


def load_features(photos, cnn_model):
    # loading all features
    if cnn_model == "VGG16":
        all_features = load(open(settings.FILE_MAPPINGS['vgg_features'], "rb"))
    elif cnn_model == "Inception":
        all_features = load(open(settings.FILE_MAPPINGS['xception_features'], "rb"))
    elif cnn_model == "Xception":
        all_features = load(open(settings.FILE_MAPPINGS['xception_features'], "rb"))

    # selecting only needed features
    features = {k: all_features[k] for k in photos}
    return features


# converting dictionary to clean list of descriptions
def dict_to_list(descriptions):
    all_desc = []
    for key in descriptions.keys():
        [all_desc.append(d) for d in descriptions[key]]
    return all_desc


# creating tokenizer class
# this will vectorise text corpus
# each integer will represent token in dictionary


def create_tokenizer(descriptions):
    desc_list = dict_to_list(descriptions)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(desc_list)
    return tokenizer


# calculate maximum length of descriptions
def max_length(descriptions):
    desc_list = dict_to_list(descriptions)
    return max(len(d.split()) for d in desc_list)
