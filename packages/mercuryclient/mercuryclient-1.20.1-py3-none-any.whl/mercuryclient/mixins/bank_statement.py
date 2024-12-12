import time
from typing import Tuple


class BankStatementMixin:
    """
    Mixin for analyzing bank statements
    """

    def request_bank_statement(self, payload) -> str:
        api = "api/v1/bank_statement/"

        request_id, r = self._post_json_http_request(
            api, data=payload, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return request_id

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending bank statement verififcation request "
            "Status: {}, Response is {}".format(r.status_code, response_json)
        )

    def get_bank_statement_result(self, request_id: str) -> Tuple[str, dict]:
        api = "api/v1/bank_statement/"

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
            "Error getting bank statement Verification result. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def analysis_bank_statement(
        self,
        provider: str,
        profile: str,
        statement_file_url: str,
        statement_bank_name: str = None,
        statement_password: str = None,
        entity_type: str = None,
        bank_code: str = None,
        account_type: str = None,
        account_number: str = None,
        max_attempts: int = 5,
        retry_backoff: int = 5,
    ):

        request_data = {
            "provider": provider,
            "profile": profile,
            "statement_file_url": statement_file_url,
        }
        if statement_password is not None:
            request_data["statement_password"] = statement_password
        if statement_bank_name is not None:
            request_data["statement_bank_name"] = statement_bank_name

        if provider == "signzy":
            if not all([entity_type, bank_code, account_type, account_number]):
                raise ValueError(
                    "Mandatory fields missing: entity_type,bank_code,account_type,account_number required for signzy"
                )
            request_data.update(
                {
                    "entity_type": entity_type,
                    "bank_code": bank_code,
                    "account_type": account_type,
                    "account_number": account_number,
                }
            )

        print(request_data)
        mercury_request_id = self.request_bank_statement(request_data)

        for attempts in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self.get_bank_statement_result(
                mercury_request_id
            )
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception(
            "Error while getting bank statement verification. Status: IN_PROGRESS"
        )
