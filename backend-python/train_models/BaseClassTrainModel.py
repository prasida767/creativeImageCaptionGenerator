from abc import abstractmethod


class BaseClassTrainModel:
    def __init__(self, dataset, cnn_model,
                 denseLayersForCNN, lstm_model, denseLayersForLSTM, dropOutRate, nameOfModel, epochs,
                 fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValueForFile, descriptionsDictionary,
                 numLayersForLSTM, optimizer, learningRate, l2RegularizerValue):
        self.dataset = dataset
        self.cnn_model = cnn_model
        self.lstm_model = lstm_model
        self.denseLayersForCNN = denseLayersForCNN
        self.denseLayersForLSTM = denseLayersForLSTM
        self.dropOutRate = dropOutRate
        self.nameOfModel = nameOfModel
        self.epochs = epochs
        self.fileWithImageNameOnly = fileWithImageNameOnly
        self.fileWithDescriptionAndImageName = fileWithCaptionAndImageName
        self.uniqueValueForFile = uniqueValueForFile
        self.descriptionsDictionary = descriptionsDictionary
        self.numLayersForLSTM = numLayersForLSTM
        self.optimizer = optimizer
        self.learningRate = learningRate
        self.l2RegularizerValue = l2RegularizerValue

    @abstractmethod
    def train_model(self, dataset, cnn_model,
                    denseLayersForCNN, lstm_model, denseLayersForLSTM, dropOutRate, nameOfModel, epochs,
                    fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValue, descriptionsDictionary,
                    numLayersForLSTM, optimizer, learningRate, l2RegularizerValue):
        pass
