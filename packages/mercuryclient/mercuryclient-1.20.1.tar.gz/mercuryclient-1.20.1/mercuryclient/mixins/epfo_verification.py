import time
from typing import Tuple

from mercuryclient.types.epfo_verification.enums import RequestTypes


class EpfoVerificationMixin:
    """
    Mixin for verifying Epfo
    """

    def _initiate_epfo_request(
        self,
        request_data,
    ) -> str:
        api = "api/v1/epfo/verify/"
        try:
            RequestTypes(request_data.get("request_type"))
        except ValueError:
            raise Exception(
                f"{request_data.get('request_type')} is not a valid request_type"
            )

        request_id, r = self._post_json_http_request(
            api, data=request_data, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return request_id

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Epfo verification request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def _get_epfo_response(self, request_id: str) -> Tuple[str, dict]:
        api = "api/v1/epfo/verify/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            result = r.json()
            return request_id, result

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error getting Epfo Verification result. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def _get_epfo_result(
        self, mercury_request_id: str, max_attempts: int, retry_backoff: int
    ):
        """Retry mechanism for epfo response

        raises:
            Exception: After max attempts, response till remains in progress

        returns mercury_request_id,response from the vendor

        """

        for _ in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self._get_epfo_response(mercury_request_id)
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception("Error while getting Epfo response. Status: IN_PROGRESS")

    def generate_epfo_otp(
        self,
        profile: str,
        provider: str,
        mobile_number: str,
        callback_url: str = None,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Initiates the request for epfo otp generation.

        returns: mercury_request_id,otp generation response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "mobile_number": mobile_number,
            "request_type": RequestTypes.OTP_REQUEST.value,
        }
        if callback_url:
            request_data["callback_url"] = callback_url
        mercury_request_id = self._initiate_epfo_request(request_data)
        return self._get_epfo_result(mercury_request_id, max_attempts, retry_backoff)

    def verify_epfo_otp(
        self,
        profile: str,
        provider: str,
        otp: str,
        epfo_request_id: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Get OTP from customer and verify with request_id.

        returns: mercury_request_id, verify epfo response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "otp": otp,
            "request_id": epfo_request_id,
            "request_type": RequestTypes.OTP_VERIFY.value,
        }
        mercury_request_id = self._initiate_epfo_request(request_data)
        return self._get_epfo_result(mercury_request_id, max_attempts, retry_backoff)

    def get_epfo_details(
        self,
        profile: str,
        provider: str,
        epfo_request_id: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Get OTP from customer and verify with request_id.

        returns: mercury_request_id, verify epfo response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "request_id": epfo_request_id,
            "request_type": RequestTypes.EPFO_DETAILS.value,
        }
        mercury_request_id = self._initiate_epfo_request(request_data)
        return self._get_epfo_result(mercury_request_id, max_attempts, retry_backoff)
