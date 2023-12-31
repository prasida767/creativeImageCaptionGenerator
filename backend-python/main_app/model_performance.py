import os


def save_loss_chart(epochs_info, model_name, nameOfModel):
    # Extract epochs and losses from the epochs_info list
    epochs = [info['Epoch'] for info in epochs_info]
    losses = [info['Loss'] for info in epochs_info]

    # Save the plot in a file under the folder named after the model's name
    sub_directory = os.path.join("models_performance", nameOfModel)
    os.makedirs(sub_directory, exist_ok=True)
    data_file = os.path.join(sub_directory, f"{model_name}_performance_chart.txt")

    with open(data_file, mode='w') as file:
        file.write("Epoch Loss\n")
        for epoch, loss in zip(epochs, losses):
            file.write(f"{epoch} {loss}\n")
