from main_app import utils
import pickle
import os
from djangoProject import settings


def dataset_loader(fileNameWithImage, fileWithCaptionAndImageName, uniqueValueForFile, descriptionsDictionary,
                   cnn_model):
    train_images = utils.load_photos(fileNameWithImage)
    train_descriptions = utils.load_clean_descriptions(fileWithCaptionAndImageName, train_images)
    train_features = utils.load_features(train_images, cnn_model)

    # give each word an index, and store that into tokenizer.p pickle file
    tokenizer = utils.create_tokenizer(train_descriptions)

    # Save the tokenizer to a specific directory
    output_directory = settings.FILE_MAPPINGS['tokenizer_file_path']
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

    tokenizer_file = os.path.join(output_directory, f"{uniqueValueForFile}_tokenizer.p")
    with open(tokenizer_file, 'wb') as file:
        pickle.dump(tokenizer, file)
    vocab_size = len(tokenizer.word_index) + 1

    max_length = utils.max_length(descriptionsDictionary)

    print('No. of Training Dataset::::: ', len(train_images))
    print('Length of Training Descriptions::::: ', len(train_descriptions))
    print('No. of Features For Training Images::::: ', len(train_features))
    print('Vocabulary Size::::: ', vocab_size)
    print('Longest/Maximum Description Length:::::  ', max_length)
    return train_images, train_descriptions, train_features, vocab_size, max_length, tokenizer
