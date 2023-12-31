# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .model_training import train_model


@csrf_exempt
def train(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)

            # Check if any required keys have empty values
            for key, value in request_data.items():
                if value == '':
                    return JsonResponse({"error": f"Value for '{key}' cannot be empty."}, status=400)

            # train_model function from model_training.py
            response = train_model(request_data)
            return response

        except json.JSONDecodeError:
            response_data = {"error": "Invalid JSON format in the request body."}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {"error": "Invalid request method. POST request is required."}
        return JsonResponse(response_data, status=405)
