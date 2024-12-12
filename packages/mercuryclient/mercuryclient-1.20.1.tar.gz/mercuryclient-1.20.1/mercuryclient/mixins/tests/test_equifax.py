from datetime import date
from unittest import TestCase, mock

from mercuryclient.api import MercuryApi
from mercuryclient.types.equifax.request import EquifaxRequest


class EquifaxMixinTest(TestCase):
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
        data = {
            "profile": "test",
            "product_code": ["CCR"],
            "inquiry_purpose": "OTHER",
            "first_name": "STEVE SMITH",
            "middle_name": "",
            "last_name": "SMITH",
            "dob": date(1996, 12, 9),
            "inquiry_address": [
                {
                    "address_type": ["HOME"],
                    "address_line_1": "B/404, Durja Pooj Society, Haridwar, Haridwar, UP",
                    "state": "TRIPURA",
                    "city": "Udaipur",
                    "postal": "955567",
                }
            ],
            "inquiry_phones": [{"number": "7777794563", "number_type": ["MOBILE"]}],
            "id_details": [
                {"id_type": "AADHAR", "id_value": "986249396345"},
                {"id_type": "VOTER_ID", "id_value": "KJG0226988", "source": "Inquiry"},
            ],
            "mif_details": {
                "family_details": [
                    {"additional_name_type": "FATHER", "additional_name": "John Smith"},
                    {"additional_name_type": "HUSBAND", "additional_name": "KIng"},
                ]
            },
        }

        self.request_data = EquifaxRequest(**data)

    def test_request_equifax_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.request_equifax_report(self.request_data, "test", "some_provider")
        self.post_api_mock.assert_called_with(
            "api/v1/equifax/",
            data={
                "product_code": ["CCR"],
                "inquiry_purpose": "OTHER",
                "first_name": "STEVE SMITH",
                "middle_name": "",
                "last_name": "SMITH",
                "dob": "1996-12-09",
                "inquiry_address": [
                    {
                        "address_type": ["HOME"],
                        "address_line_1": "B/404, Durja Pooj Society, Haridwar, Haridwar, UP",
                        "state": "TRIPURA",
                        "city": "Udaipur",
                        "postal": "955567",
                    }
                ],
                "inquiry_phones": [{"number": "7777794563", "number_type": ["MOBILE"]}],
                "id_details": [
                    {"id_type": "AADHAR", "id_value": "986249396345"},
                    {
                        "id_type": "VOTER_ID",
                        "id_value": "KJG0226988",
                        "source": "Inquiry",
                    },
                ],
                "mif_details": {
                    "family_details": [
                        {
                            "additional_name_type": "FATHER",
                            "additional_name": "John Smith",
                        },
                        {"additional_name_type": "HUSBAND", "additional_name": "KIng"},
                    ]
                },
                "profile": "test",
                "provider": "some_provider",
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.request_equifax_report(
                self.request_data, "test", "some_provider"
            )

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        request_id = self.client.request_equifax_report(
            self.request_data, "test", "some_provider"
        )
        self.assertEqual(request_id, "random_string")

    def test_response_verify_rc(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client.get_equifax_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/equifax/",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_equifax_response("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client.get_equifax_response("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")
