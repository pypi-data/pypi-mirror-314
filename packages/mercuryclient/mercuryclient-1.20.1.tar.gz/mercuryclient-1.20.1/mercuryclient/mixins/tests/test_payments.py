import json
from mercuryclient.api import MercuryApi
from unittest import TestCase, mock
from mercuryclient.types.payments.enums import Endpoints
from mercuryclient.types.payments.request import (
    QRCodeDetails,
    CreatePlan,
    SubscriptionCreation,
    SubscriptionFetch,
    PaymentGateway,
)


class PaymentsMixinTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        qr_code_data = {
            "type": "test_qr_code",
            "name": "test_name",
            "usage": "test_use",
            "fixed_amount": True,
            "payment_amount": 999,
            "description": "Pass Case",
            "notes": {"purpose": "testing"},
        }
        plan_creation_data = {
            "period": "monthly",
            "interval": 1,
            "item": {
                "name": "test_user",
                "amount": 9999,
                "currency": "INR",
                "description": "Pass Case",
            },
        }
        subscription_creation_data = {
            "plan_id": "RZP001",
            "total_count": 12,
            "quantity": 1,
            "customer_notify": 0,
        }
        subscription_fetch_data = {
            "provider": "razorpay",
            "profile": "sample_profile",
            "subscription_id": "RZPSC001",
        }
        payment_link_data = {
            "provider": "razorpay",
            "profile": "sample_profile",
            "amount": 123244,
            "currency": "INR",
            "accept_partial": False,
            "description": "Collection of loan id 21343",
            "notes": {
                "purpose": "Collection of loan id 21343",
            },
            "customer": {
                "name": "test customer",
                "email": "test@test.com",
                "contact": "9837632567",
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True,
        }
        self.qr_code_request_obj = QRCodeDetails(**qr_code_data)
        self.plan_creation_obj = CreatePlan(**plan_creation_data)
        self.subscription_creation_obj = SubscriptionCreation(
            **subscription_creation_data
        )
        self.subscription_fetch_obj = SubscriptionFetch(**subscription_fetch_data)
        self.payment_link_obj = PaymentGateway(**payment_link_data)

        self.qr_code_request_dict = {
            **json.loads(self.qr_code_request_obj.json(exclude_unset=True)),
            **{"profile": "sample_profile"},
            **{"provider": "razorpay"},
        }
        self.plan_creation_dict = {
            **json.loads(self.plan_creation_obj.json(exclude_unset=True)),
            **{"profile": "sample_profile"},
            **{"provider": "razorpay"},
        }
        self.subscription_creation_dict = {
            **json.loads(self.subscription_creation_obj.json(exclude_unset=True)),
            **{"profile": "sample_profile"},
            **{"provider": "razorpay"},
        }
        self.subscription_fetch_dict = {
            **json.loads(self.subscription_fetch_obj.json(exclude_unset=True)),
            **{"profile": "sample_profile"},
            **{"provider": "razorpay"},
        }
        self.payment_link_dict = {
            **json.loads(self.payment_link_obj.json(exclude_unset=True)),
            **{"profile": "sample_profile"},
            **{"provider": "razorpay"},
        }

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.get_api_mock.stop)

    def test_entire_qr_code_flow(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.generate_qr_code(
            self.qr_code_request_obj, "sample_profile", "razorpay"
        )

        self.post_api_mock.assert_called_with(
            "api/v1/payments/generate/qr/code",
            data=self.qr_code_request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

        self.assertEqual(response[1]["status"], "SUCCESS")

    def test_qr_code_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.generate_qr_code(
                self.qr_code_request_obj, "test", "some_provider"
            )

    def test_entire_payment_plan_flow(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.generate_payment_plan(
            self.plan_creation_obj, "sample_profile", "razorpay"
        )

        self.post_api_mock.assert_called_with(
            "api/v1/payments/plan/create",
            data=self.plan_creation_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

        self.assertEqual(response[1]["status"], "SUCCESS")

    def test_plan_creation_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.generate_payment_plan(
                self.plan_creation_obj, "test", "some_provider"
            )

    def test_entire_subscription_creation_flow(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.create_payment_subscription(
            self.subscription_creation_obj, "sample_profile", "razorpay"
        )

        self.post_api_mock.assert_called_with(
            "api/v1/payments/subscription/create",
            data=self.subscription_creation_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

        self.assertEqual(response[1]["status"], "SUCCESS")

    def test_subscription_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.create_payment_subscription(
                self.subscription_creation_obj, "test", "some_provider"
            )

    def test_entire_subscription_fetch_flow(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.fetch_subscription(
            self.subscription_fetch_obj, "sample_profile", "razorpay"
        )

        self.post_api_mock.assert_called_with(
            "api/v1/payments/subscription/fetch",
            data=self.subscription_fetch_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

        self.assertEqual(response[1]["status"], "SUCCESS")

    def test_fetch_subs_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.fetch_subscription(
                self.subscription_fetch_obj, "test", "some_provider"
            )

    def test_entire_payment_link_flow(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.generate_payment_link(
            self.payment_link_obj, "sample_profile", "razorpay"
        )

        self.post_api_mock.assert_called_with(
            "api/v1/payments/payment/link/create",
            data=self.payment_link_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

        self.assertEqual(response[1]["status"], "SUCCESS")

    def test_payment_link_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.fetch_subscription(
                self.payment_link_obj, "test", "some_provider"
            )

    def test_payments_result_response(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client.get_payment_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/payments/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_payment_result_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_payment_result("random_string")

    def test_payment_result_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client.get_payment_result("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")
