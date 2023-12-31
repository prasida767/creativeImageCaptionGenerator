import json
from django.test import TestCase, Client


class TrainModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Set up any necessary data or configurations for testing

    def test_train_model_with_valid_data(self):
        # Prepare a valid request data dictionary
        valid_request_data = {
            'dataset': 'Flickr8k',
            'pretrainedCNNModel': 'SomeCNNModel',
            'lstmArchitecture': 'SomeLSTMModel',
            'denseLayersCNN': '2',
            'denseLayersLSTM': '2',
            'dropoutRate': '0.5',
            'nameOfModel': 'TestModel',
            'epochs': '5',
            'trainingParams': '10',
            'testingParams': '5',
            'numLayersForLSTM': '2',
            'optimizer': 'Adam',
            'learningRate': '0.001',
            'l2Regularizer': '0.01',
        }

        # Send a POST request to your view using the test client
        response = self.client.post('/train/', json.dumps(valid_request_data), content_type='application/json')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response content for expected data
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
        self.assertIn('parameters', response_data)

        # Add more assertions to check specific data in the response

    def test_train_model_with_invalid_data(self):
        # Prepare an invalid request data dictionary (missing required parameters)
        invalid_request_data = {
            'pretrainedCNNModel': 'SomeCNNModel',
            'lstmArchitecture': 'SomeLSTMModel',
            # Missing other required parameters
        }

        # Send a POST request to your view using the test client
        response = self.client.post('/train_model/', json.dumps(invalid_request_data), content_type='application/json')

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check the response content for an error message
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)

        # Add more assertions to check specific error conditions

    def tearDown(self):
        # Clean up any test-specific data or configurations if necessary
        pass