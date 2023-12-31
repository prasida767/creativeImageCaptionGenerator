import json

import unittest
from django.http import JsonResponse

from main_app.views import generate_caption, list_models, read_text_file, parse_loss_file


def create_mock_request():
    # Create a mock request object with necessary attributes
    mock_request = unittest.mock.Mock()
    mock_request.method = 'POST'
    mock_request.body = json.dumps({'image': 'base64_encoded_image_data', 'model': 'model_string'})
    return mock_request


class MainAppTestCase(unittest.TestCase):

    def test_generate_caption(self):
        # Prepare a mock request object
        request = create_mock_request()

        # Call the function and get the response
        response = generate_caption(request)

        # Check if the response is a JsonResponse and has the expected status code
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)  # Replace with the expected status code

    def test_list_models(self):
        # Prepare a mock request object
        request = create_mock_request()

        # Call the function and get the response
        response = list_models(request)

        # Check if the response is a JsonResponse and has the expected status code
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)  # Replace with the expected status code

    def test_read_text_file(self):
        # Replace with the actual file path
        file_path = ''

        # Call the function to read the text file
        file_content = read_text_file(file_path)

        # Check if the file content is a non-empty string
        self.assertIsInstance(file_content, str)
        self.assertTrue(len(file_content) > 0)

    def test_parse_loss_file(self):
        # Replace with the actual file path
        file_path = ''

        # Call the function to parse the loss file
        loss_data = parse_loss_file(file_path)

        # Check if the parsed data is a list of dictionaries
        self.assertIsInstance(loss_data, list)
        self.assertTrue(all(isinstance(item, dict) for item in loss_data))
        self.assertTrue(len(loss_data) > 0)


if __name__ == '__main__':
    unittest.main()