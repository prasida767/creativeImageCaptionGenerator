from main_app import utils
import pickle
from djangoProject import settings


def dataset_loader(fileNameWithImage, fileWithCaptionAndImageName, unique_file_name, descriptionsDictionary,
                   cnn_model):
    test_images = utils.load_photos(fileNameWithImage)
    test_descriptions = utils.load_clean_descriptions(fileWithCaptionAndImageName, test_images)
    test_features = utils.load_features(test_images, cnn_model)

    tokenizerFile = settings.FILE_MAPPINGS['tokenizer_file_path'] + f"{unique_file_name}_tokenizer.p"
    tokenizer = pickle.load(open(tokenizerFile, "rb"))

    vocab_size = len(tokenizer.word_index) + 1

    max_length = utils.max_length(descriptionsDictionary)

    print('No. of Testing Dataset::::: ', len(test_images))
    print('Length of Testing Descriptions::::: ', len(test_descriptions))
    print('No. of Features For Testing Images::::: ', len(test_features))
    print('Vocabulary Size::::: ', vocab_size)
    print('Longest/Maximum Description Length:::::  ', max_length)
    return test_images, test_descriptions, test_features, vocab_size, max_length, tokenizer
