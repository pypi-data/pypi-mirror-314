import time
from typing import Tuple


class RcVerificationMixin:
    """
    Mixin for verifying vehicle rc
    """

    def initiate_rc_verification_request(
        self,
        request_data,
    ) -> str:
        api = "api/v1/rc/verify/"
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
            "Error while sending vehicle rc verification request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_rc_response(self, request_id: str) -> Tuple[str, dict]:
        api = "api/v1/rc/verify/"

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
            "Error getting vehicle rc Verification result. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def fetch_rc_details(
        self,
        profile: str,
        provider: str,
        rc_number: str,
        consent: bool,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Based on vehicle rc numbers it fetches all the details associated with it
        returns: mercury_request_id, verify vehicle rc response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "vehicle_rc_number": rc_number,
            "consent": consent,
        }

        mercury_request_id = self.initiate_rc_verification_request(request_data)

        for attempts in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self.get_rc_response(mercury_request_id)
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception("Error while getting rc response. Status: IN_PROGRESS")
