import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from test_models import modelTesting


@csrf_exempt
def test(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        required_keys = ["model", "testMetric"]

        for key in required_keys:
            if key not in data:
                raise Exception(f"Key '{key}' is missing in the JSON data")

        response_data = modelTesting.test_model(data)
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
