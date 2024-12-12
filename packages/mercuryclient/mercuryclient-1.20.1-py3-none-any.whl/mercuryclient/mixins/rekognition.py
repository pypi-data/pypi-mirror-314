import time
from typing import Tuple


class RekognitionMixins:
    """
    Mixin for face rekognition
    """

    def generate_liveness_session_id(
        self, profile, provider, token, liveness_prefix="image_auth"
    ) -> Tuple[str, dict]:
        api = "api/v1/rekognition/create/session"
        payload = dict(
            profile=profile,
            provider=provider,
            token=token,
            liveness_prefix=liveness_prefix,
        )

        request_id, response = self._post_json_http_request(
            api, data=payload, send_request_id=True, add_bearer_token=True
        )

        if response.status_code == 201:
            result = response.json()
            return request_id, result

        try:
            response_json = response.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while generating Session id for rekognition. Status: {}, Response is {}".format(
                response.status_code, response_json
            )
        )

    def get_liveness_session_result(
        self, profile: str, provider: str, session_id: str
    ) -> Tuple[str, dict]:
        api = "api/v1/rekognition/verify/session"
        payload = dict(profile=profile, provider=provider, session_id=session_id)
        request_id, response = self._post_json_http_request(
            api, data=payload, send_request_id=True, add_bearer_token=True
        )

        if response.status_code == 200:
            result = response.json()
            return request_id, result

        try:
            response_json = response.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error getting rekognition session result. Status: {}, Response is {}".format(
                response.status_code, response_json
            )
        )
