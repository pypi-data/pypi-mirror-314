from datetime import date
from unittest import TestCase, mock

from mercuryclient.api import MercuryApi


class ItrMixinTest(TestCase):
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
        self.request_data = {
            "provider": "zoop",
            "profile": "some_profile",
            "file_url": "some_url",
            "date_of_birth": date(2024, 1, 1),
        }

    def test_request_itr_pull(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.initiate_itr_extraction_request(self.request_data)

        self.post_api_mock.assert_called_with(
            "api/v1/itr/extract",
            data={
                "provider": "zoop",
                "profile": "some_profile",
                "file_url": "some_url",
                "date_of_birth": date(2024, 1, 1),
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)

        with self.assertRaises(Exception):
            self.client.initiate_itr_extraction_request(self.request_data)

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        request_id = self.client.initiate_itr_extraction_request(self.request_data)
        self.assertEqual(request_id, "random_string")

    def test_response_itr_result(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client.get_itr_extraction_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/itr/extract",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_itr_extraction_response("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client.get_itr_extraction_response("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")
