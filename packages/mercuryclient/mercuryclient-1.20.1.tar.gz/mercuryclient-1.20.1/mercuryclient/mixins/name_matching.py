class NameMatchMixin:
    """
    Mixin for name matching
    """

    def name_match(
        self,
        provider: str,
        profile: str,
        primary_name: str,
        secondary_name: str,
        remove_salutations: bool = True,
        purpose: str = "",
    ):
        """
        Name Matching using the mercury service

        Args:
            provider (str): service provider
            profile (str): mercury profile
            primary_name (str): name for comparison
            secondary_name (str): name to be compared with
            remove_salutations (bool, optional): Flag to remove salutation. Defaults to True.

        Raises:
            Exception: if Failed to ret response form mercury

        Returns:
            dict[str, dict]: mercury request id,name match result
        """
        api = "api/v1/name/match"

        request_dict = dict(
            profile=profile,
            provider=provider,
            primary_name=primary_name,
            secondary_name=secondary_name,
            remove_salutations=remove_salutations,
            purpose=purpose,
        )

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        try:
            response_json = r.json()
        except Exception:
            response_json = {}

        if r.status_code == 200:
            return request_id, response_json

        raise Exception(
            "Error while sending name match request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
