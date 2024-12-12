from datetime import date
from unittest import TestCase, mock

from mercuryclient.api import MercuryApi


class RekognitionMixinTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.get_api_mock.stop)
        self.request_data = dict(
            profile="test",
            provider="test",
            token="test_token",
            liveness_prefix="test_prefix",
        )

    def test_create_session_id(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        self.client.generate_liveness_session_id(**self.request_data)

        self.post_api_mock.assert_called_with(
            "api/v1/rekognition/create/session",
            data={
                "profile": "test",
                "provider": "test",
                "token": "test_token",
                "liveness_prefix": "test_prefix",
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)

        with self.assertRaises(Exception):
            self.client.generate_liveness_session_id(**self.request_data)

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        response = self.client.generate_liveness_session_id(**self.request_data)
        self.assertEqual(response[0], "random_string")
