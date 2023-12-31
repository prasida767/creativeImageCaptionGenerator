import numpy as np
from djangoProject import settings
from keras.models import load_model
from pickle import load
from keras.utils import pad_sequences
from main_app import utils, PreprocessDataset, XceptionCaptionGenerator, VGGCaptionGenerator, InceptionCaptionGenerator


def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text


def caption_generation(image, model_file_path, pretrained_model, unique_file_name):
    fileName = settings.FILE_MAPPINGS['file_path_caption_generation'] + f"train_captions_{unique_file_name}.txt"
    tokenizerFile = settings.FILE_MAPPINGS['tokenizer_file_path'] + f"{unique_file_name}_tokenizer.p"

    max_length = utils.max_length(
        PreprocessDataset.cleaning_text(PreprocessDataset.create_image_captions_dict(fileName)))

    tokenizer = load(open(tokenizerFile, "rb"))
    model = load_model(model_file_path)
    photoFeature = []
    if pretrained_model == "Xception":
        photoFeature = XceptionCaptionGenerator.photoFeatureExtractor(image)
    elif pretrained_model == "VGG":
        photoFeature = VGGCaptionGenerator.photoFeatureExtractor(image)
    elif pretrained_model == "InceptionV3":
        photoFeature = InceptionCaptionGenerator.photoFeatureExtractor(image)

    description = generate_desc(model, tokenizer, photoFeature, max_length)
    print("\n\n")
    print(description)
    return description
