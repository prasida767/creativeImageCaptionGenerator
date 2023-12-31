from train_models import XceptionTrainModel, InceptionTrainModel
from train_models import VGGTrainModel


class TrainModelFactory:
    @staticmethod
    def create_model(dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM, dropOutRate, nameOfModel,
                     epochs, fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValueForFile,
                     descriptionsDictionary, numLayersForLSTM, optimizer, learningRate, l2RegularizerValue):
        if cnn_model == "Xception":
            return XceptionTrainModel.XceptionTrainModel(
                dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM,
                dropOutRate, nameOfModel, epochs, fileWithImageNameOnly, fileWithCaptionAndImageName,
                uniqueValueForFile, descriptionsDictionary, numLayersForLSTM,
                optimizer, learningRate, l2RegularizerValue).train_model(dataset, cnn_model, denseLayersForCNN,
                                                                         lstm_model,
                                                                         denseLayersForLSTM, dropOutRate, nameOfModel,
                                                                         epochs,
                                                                         fileWithImageNameOnly,
                                                                         fileWithCaptionAndImageName,
                                                                         uniqueValueForFile, descriptionsDictionary,
                                                                         numLayersForLSTM, optimizer, learningRate,
                                                                         l2RegularizerValue
                                                                         )

        elif cnn_model == "VGG16":
            return VGGTrainModel.VGGTrainModel(
                dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM,
                dropOutRate, nameOfModel, epochs, fileWithImageNameOnly, fileWithCaptionAndImageName,
                uniqueValueForFile, descriptionsDictionary, numLayersForLSTM,
                optimizer, learningRate, l2RegularizerValue).train_model(dataset, cnn_model, denseLayersForCNN,
                                                                         lstm_model,
                                                                         denseLayersForLSTM, dropOutRate, nameOfModel,
                                                                         epochs,
                                                                         fileWithImageNameOnly,
                                                                         fileWithCaptionAndImageName,
                                                                         uniqueValueForFile, descriptionsDictionary,
                                                                         numLayersForLSTM, optimizer, learningRate,
                                                                         l2RegularizerValue)
        elif cnn_model == "InceptionV3":
            return InceptionTrainModel.InceptionTrainModel(
                dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM,
                dropOutRate, nameOfModel, epochs, fileWithImageNameOnly, fileWithCaptionAndImageName,
                uniqueValueForFile, descriptionsDictionary, numLayersForLSTM,
                optimizer, learningRate, l2RegularizerValue).train_model(dataset, cnn_model, denseLayersForCNN,
                                                                         lstm_model,
                                                                         denseLayersForLSTM, dropOutRate, nameOfModel,
                                                                         epochs,
                                                                         fileWithImageNameOnly,
                                                                         fileWithCaptionAndImageName,
                                                                         uniqueValueForFile, descriptionsDictionary,
                                                                         numLayersForLSTM, optimizer, learningRate,
                                                                         l2RegularizerValue
                                                                         )
