from keras.models import load_model

from djangoProject import settings
from main_app import PreprocessDataset, utils
from test_models import TestDataSetLoader
from test_models import EvaluateModel


def test_model(data):
    trained_models_directory = settings.FILE_MAPPINGS['trained_models_directory']
    model = data["model"]
    # Parse the model string to extract folder name, pretrained model, and unique file name
    model_info = model.split('___')
    folder_name = model_info[0]
    pretrained_cnn_model = model_info[1]
    unique_file_name = model_info[-1].rsplit('.', 1)[0]

    # Create the full path to the model file
    model_file_path = trained_models_directory + "/" + folder_name + "/" + model

    trainFileName = fileName = settings.FILE_MAPPINGS['file_path_caption_generation'] + \
                               f"train_captions_{unique_file_name}.txt"

    # Initialize trainingParams to the number of lines in the file
    with open(fileName, 'r') as file:
        testingParams = len(file.readlines())
    # Your processing logic goes here
    descriptionsDictionary, fileWithImageName, fileWithCaptionAndImageName = PreprocessDataset.PreprocessDataset(
        fileName, unique_file_name, testingParams, "test")

    test_images, test_descriptions, test_features, vocab_size, max_length, tokenizer = TestDataSetLoader. \
        dataset_loader(fileWithImageName, fileWithCaptionAndImageName, unique_file_name, descriptionsDictionary,
                       pretrained_cnn_model)

    max_length_required = utils.max_length(
        PreprocessDataset.cleaning_text(PreprocessDataset.create_image_captions_dict(trainFileName)))

    model = load_model(model_file_path)

    evaluationMetric = EvaluateModel.evaluate_model(model, test_descriptions, test_features, tokenizer,
                                                    max_length_required)

    return evaluationMetric
