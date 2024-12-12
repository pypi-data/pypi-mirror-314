import time


class UdyogAadhaarVerifyMixin:
    """
    Mixin for Udyog Aadhaar verification
    """

    def initiate_udyog_verification(self, request_dict):
        """
        udyog verification using the mercury service

        :param udyog_aadhaar: string
        :param provider: any
        :param profile: An existing profile in Mercury. The profile has to correspond
        to the provider.
        :return: (request_id, data)
        """
        api = "api/v1/udyog_aadhaar/verify/"

        request_id, r = self._post_json_http_request(
            api, data=request_dict, send_request_id=True, add_bearer_token=True
        )
        try:
            response_json = r.json()
        except Exception:
            response_json = {}

        if r.status_code == 201:
            return request_id

        raise Exception(
            f"Error while sending Udyog aadhaar verify request. Status: {r.status_code}, Response is {response_json}"
        )

    def get_udyog_details(self, request_id: str):
        api = "api/v1/udyog_aadhaar/verify/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            result = r.json()
            if result["status"] == "FAILURE":
                raise Exception(
                    f"Error verifying Udyog aadhaar. Status: {result['status']} | Message {result['message']}"
                )
            return request_id, result

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            f"Error getting Udyog aadhaar Verification result. Status: {r.status_code}, Response is {response_json}"
        )

    def verify_udyog_aadhaar(
        self,
        udyog_aadhaar: str,
        consent: bool,
        provider: str,
        profile: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Based on udyog aadhaar numbers it fetches all the details associated with it
        returns: mercury_request_id, verified udyog response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "udyog_aadhaar": udyog_aadhaar,
            "consent": consent,
        }

        mercury_request_id = self.initiate_udyog_verification(request_data)

        for attempts in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self.get_udyog_details(mercury_request_id)
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception("Error while getting udyog response. Status: IN_PROGRESS")
