import time
import json
from typing import Tuple

from mercuryclient.types.ckyc.request import IndividualEntityRequest, LegalEntityRequest


class CkycMixin:
    """
    Mixin for registering Ckyc requests
    """

    def _initiate_ckyc_request(
        self,
        api: str,
        request_dict: dict,
    ) -> str:
        """
        POST a request to Mercury to Request Ckyc report. This posts the request to
        Mercury and returns immediately. Use the returned request ID and poll
        _get_ckyc_response to check for report.
        You can also use fetch_Ckyc_report which is a helper function that combines
        this api and the result api to get the result.

        :param request_obj: Object of CkycRequest model
        :type request_obj: CkycRequest
        :param profile: Ckyc profile name
        :type profile: str
        :return: Dict containing request ID and status
        :rtype: dict
        """
        api = "api/v1/" + api
        request_id, r = self._post_json_http_request(
            api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return request_id

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Ckyc request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def _get_ckyc_response(self, request_id: str) -> Tuple[str, dict]:
        """
        Get result for ckyc job request at the provided request ID. You can poll
        this method to check for response. If the job is still progressing, the status
        within the response will be IN_PROGRESS and the method can continue to be polled
        until you get either a SUCCESS or FAILURE

        :param request_id: Request ID of the CKYC job request
        :type request_id: str
        :return: Tuple containing request ID and job response. This response will
            contain the "status" of the job (IN_PROGRESS, SUCCESS or FAILURE), a
            "message" and a "data" key containing a dict with the bureau report
        :rtype: Tuple[str, dict]
        """
        api = "api/v1/ckyc/result"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            return request_id, r.json()

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while getting Ckyc response. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def create_indv_entity(
        self,
        profile: str,
        request_obj: IndividualEntityRequest,
        max_attempts: int = 8,
        retry_backoff: int = 15,
    ):
        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id = self._initiate_ckyc_request(
            "ckyc/indv/entity/upload/", request_dict
        )

        return self.fetch_ckyc_result(request_id, max_attempts, retry_backoff)

    def create_legal_entity(
        self,
        profile: str,
        request_obj: LegalEntityRequest,
        max_attempts: int = 8,
        retry_backoff: int = 15,
    ):
        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id = self._initiate_ckyc_request(
            "ckyc/legal/entity/upload/", request_dict
        )

        return self.fetch_ckyc_result(request_id, max_attempts, retry_backoff)

    def fetch_ckyc_result(
        self, request_id: str, max_attempts: int = 8, retry_backoff: int = 15
    ):
        attempts = 0
        while attempts < max_attempts:
            time.sleep(retry_backoff)
            request_id, result = self._get_ckyc_response(request_id)
            if result.get("status") != "IN_PROGRESS":
                return result

            retry_backoff *= 2
            attempts += 1

        raise Exception("Error while getting Ckyc response. Status: IN_PROGRESS")
