import base64

from keras.src.callbacks import History
from keras.utils import plot_model

from main_app.model_performance import save_loss_chart
from train_models.BaseClassTrainModel import BaseClassTrainModel
from main_app import inception_cnn_lstm_model, data_generator
from train_models import TrainDatasetLoader
import os
import io
from contextlib import redirect_stdout


class InceptionTrainModel(BaseClassTrainModel):

    def __init__(self, dataset, cnn_model, denseLayersForCNN, lstm_model,
                 denseLayersForLSTM, dropOutRate, nameOfModel, epochs, fileWithImageNameOnly,
                 fileWithCaptionAndImageName, uniqueValueForFile, descriptionsDictionary, numLayersForLSTM, optimizer,
                 learningRate, l2RegularizerValue):
        super().__init__(dataset, cnn_model, denseLayersForCNN,
                         lstm_model, denseLayersForLSTM, dropOutRate, nameOfModel, epochs,
                         fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValueForFile, descriptionsDictionary,
                         numLayersForLSTM, optimizer, learningRate, l2RegularizerValue
                         )

    def train_model(self, dataset, cnn_model, denseLayersForCNN, lstm_model, denseLayersForLSTM, dropOutRate,
                    nameOfModel, epochs, fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValueForFile,
                    descriptionsDictionary, numLayersForLSTM, optimizer, learningRate, l2RegularizerValue):
        model_architecture_image_base64 = {}
        train_images, train_descriptions, train_features, vocab_size, max_length, tokenizer = \
            TrainDatasetLoader.dataset_loader(fileWithImageNameOnly, fileWithCaptionAndImageName, uniqueValueForFile,
                                              descriptionsDictionary, "Inception")

        model = inception_cnn_lstm_model.define_model(vocab_size, max_length, denseLayersForCNN, denseLayersForLSTM,
                                                      dropOutRate, lstm_model, numLayersForLSTM, optimizer,
                                                      learningRate,
                                                      l2RegularizerValue)
        steps = len(train_descriptions)

        main_directory = "MLModels"
        os.makedirs(main_directory, exist_ok=True)

        epochs_info = []
        for i in range(epochs):
            # Create an instance of the History callback
            history = History()
            generator = data_generator.data_generator(train_descriptions, train_features, tokenizer, max_length,
                                                      vocab_size)
            model.fit(generator, epochs=1, steps_per_epoch=steps, verbose=1, callbacks=[history])
            # Create the main directory 'MLModels' if it doesn't exist

            # Create the subdirectory with the name of 'nameOfModel'
            sub_directory = os.path.join(main_directory, nameOfModel)
            os.makedirs(sub_directory, exist_ok=True)

            # Save the model in the subdirectory
            model_filename = f"{nameOfModel}___Inception___{i}___{uniqueValueForFile}.keras"
            model_path = os.path.join(sub_directory, model_filename)
            model.save(model_path)

            model_architecture_image_path = os.path.join(sub_directory, f"{nameOfModel}___Inception___{i}.png")
            plot_model(model, to_file=model_architecture_image_path, show_shapes=True)

            # Read the model architecture image as bytes
            with open(model_architecture_image_path, "rb") as img_file:
                model_architecture_image_bytes = img_file.read()

            # Encode the image bytes as a base64 string
            model_architecture_image_base64 = base64.b64encode(model_architecture_image_bytes).decode("utf-8")

            # Access the training information for this epoch
            epochs_so_far = len(history.epoch)
            loss_for_this_epoch = history.history['loss'][0]
            epochs_info.append({'Epoch': i, 'Loss': loss_for_this_epoch})

        save_loss_chart(epochs_info, f"{nameOfModel}___Inception___'Epochs'___{uniqueValueForFile}", nameOfModel)

        # Create a file-like object to capture the output of model.summary()
        model_summary_file = io.StringIO()

        # Redirect the output of model.summary() to the file-like object
        with redirect_stdout(model_summary_file):
            model.summary()

        # Save the contents of the file-like object to a string
        model_summary_str = model_summary_file.getvalue()

        # Create a dictionary to store the response
        response_data = {
            'Model Name': 'Your Model will be saved under the name - ' f"{nameOfModel}___Inception___'Epochs'___{uniqueValueForFile}",
            'train_images_length': len(train_images),
            'train_descriptions_length': len(train_descriptions),
            'train_features_length': len(train_features),
            'vocab_size': vocab_size,
            'max_length': max_length,
            'model_architecture_image': model_architecture_image_base64,
            'model_summary': model_summary_str,
            'epochs_info': epochs_info,
        }
        return response_data
