import json
from io import BytesIO
from main_app import caption_generator
from django.http import JsonResponse
import base64
from djangoProject import settings
import os
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def generate_caption(request):
    trained_models_directory = settings.FILE_MAPPINGS['trained_models_directory']

    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)

            # Get the base64-encoded image data from the request
            image_base64 = request_data.get('image')
            if image_base64:
                image_base64 = image_base64.split(',')[1]
                # Decode the base64 image data into binary data
                image_data = base64.b64decode(image_base64)
                # Store the decoded image data in a BytesIO object
                image = BytesIO(image_data)
                # print(image)
            else:
                return JsonResponse({"error": "Image data not provided."}, status=400)

            # Parse the model string to extract folder name, pretrained model, and unique file name
            model_string = request_data.get('model')
            model_info = model_string.split('___')
            folder_name = model_info[0]
            pretrained_model = model_info[1]
            unique_file_name = model_info[-1].rsplit('.', 1)[0]

            # Create the full path to the model file
            model_file_path = trained_models_directory + "/" + folder_name + "/" + model_string

            # Call the function responsible for generating captions, passing the image as input
            descriptions = caption_generator.caption_generation(image, model_file_path, pretrained_model,
                                                                unique_file_name)

            # Assuming the 'descriptions' is a list of strings
            return JsonResponse({'descriptions': descriptions}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)

    else:
        response_data = {"error": "Invalid request method. POST request is required."}
        return JsonResponse(response_data, status=405)


def list_models(request):
    models_directory = settings.FILE_MAPPINGS['models_directory']
    models_performance_directory = settings.FILE_MAPPINGS['models_performance_directory']

    subdirectories = [subdir for subdir in os.listdir(models_directory)
                      if os.path.isdir(os.path.join(models_directory, subdir))]

    models_data = {}
    for subdir in subdirectories:
        subdir_path = os.path.join(models_directory, subdir)
        model_files = [filename for filename in os.listdir(subdir_path) if filename.endswith('.keras')]
        models_data[subdir] = model_files

    subdirectories = [subdir for subdir in os.listdir(models_performance_directory)
                      if os.path.isdir(os.path.join(models_performance_directory, subdir))]

    models_performance = {}
    for subdir in subdirectories:
        subdir_path = os.path.join(models_performance_directory, subdir)
        model_files = [filename for filename in os.listdir(subdir_path) if filename.endswith('.txt')]

        # Read the contents of each text file and include it in the models_performance dictionary
        for model_file in model_files:
            file_path = os.path.join(subdir_path, model_file)
            trimmed_key = model_file.rsplit("_performance_chart.txt", 1)[0]
            models_performance[trimmed_key] = parse_loss_file(file_path)

    combined_data = {
        'models_data': models_data,
        'models_performance': models_performance
    }

    return JsonResponse(combined_data)


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def parse_loss_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    headers = lines[0].strip().split()  # Get the headers and skip the first line
    for line in lines[1:]:
        epoch, loss = line.strip().split()
        data.append({headers[0]: int(epoch), headers[1]: float(loss)})

    return data
