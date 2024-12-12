from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi


class NameMatchingMixinTest(TestCase):
    def setUp(self):

        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.name_1 = "MRs. test name"
        self.name_2 = "Mr test name"

        self.expected_dict = {
            "profile": "some_profile",
            "provider": "some_provider",
            "primary_name": self.name_1,
            "secondary_name": self.name_2,
            "remove_salutations": True,
            "purpose": "BANK_NAME",
        }

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_name_match(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.name_match(
            "some_provider",
            "some_profile",
            primary_name=self.name_1,
            secondary_name=self.name_2,
            purpose="BANK_NAME",
        )
        self.post_api_mock.assert_called_with(
            path="api/v1/name/match",
            data=self.expected_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.name_match(
                "some_provider",
                "some_profile",
                primary_name=self.name_1,
                secondary_name=self.name_2,
            )

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id, response = self.client.name_match(
            "some_provider",
            "some_profile",
            primary_name=self.name_1,
            secondary_name=self.name_2,
        )
        self.assertEqual(request_id, "random_string")
