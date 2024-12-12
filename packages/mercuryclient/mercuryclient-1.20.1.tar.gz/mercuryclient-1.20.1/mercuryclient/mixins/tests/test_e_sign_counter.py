from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi


class ESignMixinTest(TestCase):
    def setUp(self):

        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.pdf_path = (
            r"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        )

        self.expected_dict = {
            "profile": "some_profile",
            "provider": "some_provider",
            "signature_count": 0,
            "file_name": "dummy.pdf",
            "number_of_pages": 1,
            "sign_per_page": {"page_1": 0},
        }

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_check_e_sign(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.check_e_sign(
            "some_profile", "some_provider", pdf_path=self.pdf_path
        )
        self.post_api_mock.assert_called_with(
            "api/v1/e_sign/verify/",
            data=self.expected_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.check_e_sign(
                "some_profile", "some_provider", pdf_path=self.pdf_path
            )

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id, _ = self.client.check_e_sign(
            "some_profile", "some_provider", pdf_path=self.pdf_path
        )
        self.assertEqual(request_id, "random_string")
