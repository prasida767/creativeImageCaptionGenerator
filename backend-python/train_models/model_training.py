import json
import random
import string

from train_models import TrainModelFactory, split_dataset_to_train_test
from django.http import JsonResponse
from main_app import PreprocessDataset
from djangoProject import settings


def train_model(request_data):
    try:
        dataset = request_data.get('dataset')
        cnn_model = request_data.get('pretrainedCNNModel')
        lstm_model = request_data.get('lstmArchitecture')
        denseLayersForCNN = int(request_data.get('denseLayersCNN'))
        denseLayersForLSTM = int(request_data.get('denseLayersLSTM'))
        dropOutRate = float(request_data.get('dropoutRate'))
        nameOfModel = request_data.get('nameOfModel')
        epochs = int(request_data.get('epochs'))
        trainingParams = int(request_data.get('trainingParams'))
        testingParams = int(request_data.get('testingParams'))
        numLayersForLSTM = int(request_data.get('numLayersForLSTM'))
        optimizer = request_data.get('optimizer')
        learningRate = float(request_data.get('learningRate'))
        l2RegularizerValue = float(request_data.get('l2Regularizer'))

        if not (cnn_model and lstm_model and epochs and dataset):
            return JsonResponse({"error": "Missing required parameters."}, status=400)

        unique_value = generate_random_string()

        captions = settings.FILE_MAPPINGS['caption_path']
        split_dataset_to_train_test.caption_train_test(unique_value,
                                                       captions, 'train_test', trainingParams, testingParams)

        fileName = "Flickr8k"
        if dataset == "Flickr8k":
            fileName = settings.FILE_MAPPINGS['file_path_caption_generation'] + f"train_captions_{unique_value}.txt"
        elif dataset == "Flickr30k":
            fileName = settings.FILE_MAPPINGS['file_path_caption_generation'] + f"train_captions_{unique_value}.txt"

        descriptionsDictionary, fileWithImageName, fileWithCaptionAndImageName = PreprocessDataset.PreprocessDataset(
            fileName, unique_value, trainingParams, "train")

        responseData = TrainModelFactory.TrainModelFactory.create_model(
            dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM, dropOutRate, nameOfModel, epochs,
            fileWithImageName, fileWithCaptionAndImageName, unique_value, descriptionsDictionary, numLayersForLSTM,
            optimizer, learningRate, l2RegularizerValue)

        # Return a success response
        response_data = {"message": "Training completed successfully", "parameters": responseData}
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)


def generate_random_string(length=6):
    # Generate a random string of letters and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
