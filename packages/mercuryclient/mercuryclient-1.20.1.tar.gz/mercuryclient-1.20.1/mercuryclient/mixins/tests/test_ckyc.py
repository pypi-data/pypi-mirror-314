import json
from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi
from mercuryclient.types.ckyc.request import IndividualEntityRequest, LegalEntityRequest


class CkycMixinTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        self.indv_data = {
            "fi_reference_no": "string",
            "account_type": "NORMAL",
            "personal_details": {
                "applicant_name": {
                    "name_prefix": "Mrs",
                    "first_name": "string",
                    "middle_name": "string",
                    "last_name": "string",
                },
                "applicant_maiden_name": {
                    "name_prefix": "Mrs",
                    "first_name": "string",
                    "middle_name": "string",
                    "last_name": "string",
                },
                "relationship_type": "FATHER",
                "relationship_person_name": {
                    "name_prefix": "Mrs",
                    "first_name": "string",
                    "middle_name": "string",
                    "last_name": "string",
                },
                "applicant_mother_name": {
                    "name_prefix": "Mrs",
                    "first_name": "string",
                    "middle_name": "string",
                    "last_name": "string",
                },
                "gender": "MALE",
                "date_of_birth": "2024-01-30",
                "pan_or_form_60": "string",
                "applicant_image": {
                    "image_url": "https://picsum.photos/id/2/5000/3333.jpg",
                    "image_type": "PHOTOGRAPH",
                },
            },
            "address_details": [
                {
                    "address_type": "CURRENT",
                    "address_line_1": "string",
                    "address_line_2": "string",
                    "address_line_3": "string",
                    "city": "string",
                    "district": "string",
                    "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                    "country": "AFGHANISTAN",
                    "pincode": "string",
                    "address_proof": "PROOF_OF_POSSESSION_OF_AADHAAR",
                    "address_proof_other_details": "string",
                    "id_proof_and_address_proof_same": True,
                    "address_proof_images": {
                        "image_url": "https://picsum.photos/id/3/5000/3333.jpg",
                        "image_type": "PAN",
                    },
                },
                {
                    "address_type": "PERMANENT",
                    "address_line_1": "string",
                    "address_line_2": "string",
                    "address_line_3": "string",
                    "city": "string",
                    "district": "string",
                    "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                    "country": "AFGHANISTAN",
                    "pincode": "string",
                    "address_proof": "PROOF_OF_POSSESSION_OF_AADHAAR",
                    "address_proof_other_details": "string",
                    "id_proof_and_address_proof_same": True,
                    "address_proof_images": {
                        "image_url": "https://picsum.photos/id/7/5000/3333.jpg",
                        "image_type": "PAN",
                    },
                },
            ],
            "contact_details": {
                "office_telephone_code": "+91",
                "office_telephone_no": "string",
                "mobile_code": "+91",
                "mobile_no": "0987654321",
                "email_id": "user@example.com",
                "residence_telephone_code": "+91",
                "residence_telephone_no": "string",
            },
            "remarks": "string",
            "kyc_verification_details": {
                "date_of_declaration": "2024-01-30",
                "place_of_declaration": "string",
                "kyc_verification_date": "2024-01-30",
                "type_of_document_submitted": "CERTIFIED_COPIES",
                "kyc_verification_name": "string",
                "kyc_verification_designation": "string",
                "kyc_verification_branch": "string",
                "kyc_verification_emp_code": "+91",
                "organisation_name": "string",
                "organisation_code": "+91",
            },
            "identity_details": [
                {
                    "identity_number": "string",
                    "other_identity_description": "string",
                    "identity_type": "PASSPORT",
                    "identity_image": {
                        "image_url": "https://picsum.photos/id/4/5000/3333.jpg",
                        "image_type": "PAN",
                    },
                }
            ],
            "relation_person_details": [
                {
                    "related_person_type_others_description": "string",
                    "ckyc_number": "string",
                    "name": {
                        "name_prefix": "Mrs",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "maiden_name": {
                        "name_prefix": "Mrs",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "relationship_type": "FATHER",
                    "relationship_person_name": {
                        "name_prefix": "Mrs",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "mother_name": {
                        "name_prefix": "Mrs",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "date_of_birth": "2024-01-30",
                    "gender": "MALE",
                    "nationality": "AFGHANISTAN",
                    "pan_or_form_60": "string",
                    "related_person_image": {
                        "image_url": "https://picsum.photos/id/5/5000/3333.jpg",
                        "image_type": "PHOTOGRAPH",
                    },
                    "contact_details": {
                        "office_telephone_code": "+91",
                        "office_telephone_no": "string",
                        "mobile_code": "+91",
                        "mobile_no": "9087654321",
                        "email_id": "user@example.com",
                    },
                    "kyc_verification_details": {
                        "date_of_declaration": "2024-01-30",
                        "place_of_declaration": "string",
                        "kyc_verification_date": "2024-01-30",
                        "type_of_document_submitted": "CERTIFIED_COPIES",
                        "kyc_verification_name": "string",
                        "kyc_verification_designation": "string",
                        "kyc_verification_branch": "string",
                        "kyc_verification_emp_code": "+91",
                        "organisation_name": "string",
                        "organisation_code": "+91",
                    },
                    "organisation_name": "string",
                    "organisation_code": "+91",
                    "remarks": "string",
                    "identity_details": {
                        "identity_number": "string",
                        "other_identity_description": "string",
                        "identity_type": "AADHAAR_NUMBER",
                        "identity_image": {
                            "image_url": "https://picsum.photos/id/0/5000/3333.jpg",
                            "image_type": "OFFICIALLY_VALID_DOCUMENT_IN_RESPECT_OF_PERSON_AUTHORIZED_TO_TRANSACT",
                        },
                    },
                    "address_details": [
                        {
                            "address_type": "PERMANENT",
                            "address_line_1": "string",
                            "address_line_2": "string",
                            "address_line_3": "string",
                            "city": "string",
                            "district": "string",
                            "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                            "country": "AFGHANISTAN",
                            "pincode": "string",
                            "address_proof": "PROOF_OF_POSSESSION_OF_AADHAAR",
                            "address_proof_other_details": "string",
                            "id_proof_and_address_proof_same": True,
                            "address_proof_images": {
                                "image_url": "https://picsum.photos/id/1/5000/3333.jpg",
                                "image_type": "PAN",
                            },
                        },
                        {
                            "address_type": "CURRENT",
                            "address_line_1": "string",
                            "address_line_2": "string",
                            "address_line_3": "string",
                            "city": "string",
                            "district": "string",
                            "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                            "country": "AFGHANISTAN",
                            "pincode": "string",
                            "address_proof": "PROOF_OF_POSSESSION_OF_AADHAAR",
                            "address_proof_other_details": "string",
                            "id_proof_and_address_proof_same": True,
                            "address_proof_images": {
                                "image_url": "https://picsum.photos/id/10/5000/3333.jpg",
                                "image_type": "PAN",
                            },
                        },
                    ],
                    "type_of_relationship": "GUARDIAN_OF_MINOR",
                }
            ],
        }
        self.legal_data = {
            "fi_reference_no": "string",
            "constitution_type": "SOLE_PROPRIETORSHIP",
            "constitution_type_others": "string",
            "legal_entity_details": {
                "name_of_the_entity": "string",
                "date_of_incorporation": "2024-07-24",
                "place_of_incorporation": "string",
                "date_of_commencement_of_business": "2024-07-24",
                "country_of_incorporation": "AFGHANISTAN",
                "tin_or_gst_registration_number": "string",
                "tin_issuing_country": "AFGHANISTAN",
                "pan_or_form_60": "string",
            },
            "address_details": [
                {
                    "address_type": "PERMANENT",
                    "address_line_1": "string",
                    "address_line_2": "string",
                    "address_line_3": "string",
                    "city": "string",
                    "district": "string",
                    "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                    "country": "AFGHANISTAN",
                    "pincode": "string",
                    "id_proof_and_address_proof_same": True,
                    "address_proof": "CERTIFICATE_OF_INCORPORATION_OR_FORMATION",
                    "address_proof_other_details": "string",
                    "address_proof_images": {
                        "image_url": "https://picsum.photos/id/0/5000/3333.jpg",
                        "image_type": "OFFICIALLY_VALID_DOCUMENT_IN_RESPECT_OF_PERSON_AUTHORIZED_TO_TRANSACT",
                    },
                }
            ],
            "contact_details": {
                "office_telephone_code": "str",
                "office_telephone_no": "string",
                "mobile_code": "str",
                "mobile_no": "9087654321",
                "email_id": "user@example.com",
                "fax_code": "str",
                "fax_no": "string",
                "alternate_email_id": "user@example.com",
                "alternate_mobile_number_code": "str",
                "alternate_mobile_number": "9087654321",
            },
            "remarks": "string",
            "kyc_verification_details": {
                "date_of_declaration": "2024-07-24",
                "place_of_declaration": "string",
                "kyc_verification_date": "2024-07-24",
                "type_of_document_submitted": "CERTIFIED_COPIES",
                "kyc_verification_name": "string",
                "kyc_verification_designation": "string",
                "kyc_verification_branch": "string",
                "kyc_verification_emp_code": "str",
                "organisation_name": "string",
                "organisation_code": "str",
            },
            "identity_details": [
                {
                    "identity_number": "string",
                    "other_identity_description": "string",
                    "identity_type": "PAN",
                    "identity_image": {
                        "image_url": "https://picsum.photos/id/1/5000/3333.jpg",
                        "image_type": "OFFICIALLY_VALID_DOCUMENT_IN_RESPECT_OF_PERSON_AUTHORIZED_TO_TRANSACT",
                    },
                }
            ],
            "relation_person_details": [
                {
                    "related_person_type_others_description": "string",
                    "ckyc_number": "string",
                    "name": {
                        "name_prefix": "str",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "maiden_name": {
                        "name_prefix": "str",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "relationship_type": "FATHER",
                    "relationship_person_name": {
                        "name_prefix": "str",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "mother_name": {
                        "name_prefix": "str",
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                    },
                    "date_of_birth": "2024-07-24",
                    "gender": "MALE",
                    "nationality": "AFGHANISTAN",
                    "pan_or_form_60": "string",
                    "related_person_image": {
                        "image_url": "https://picsum.photos/id/2/5000/3333.jpg",
                        "image_type": "PHOTOGRAPH",
                    },
                    "contact_details": {
                        "office_telephone_code": "str",
                        "office_telephone_no": "string",
                        "mobile_code": "str",
                        "mobile_no": "9087654321",
                        "email_id": "user@example.com",
                    },
                    "kyc_verification_details": {
                        "date_of_declaration": "2024-07-24",
                        "place_of_declaration": "string",
                        "kyc_verification_date": "2024-07-24",
                        "type_of_document_submitted": "CERTIFIED_COPIES",
                        "kyc_verification_name": "string",
                        "kyc_verification_designation": "string",
                        "kyc_verification_branch": "string",
                        "kyc_verification_emp_code": "str",
                        "organisation_name": "string",
                        "organisation_code": "str",
                    },
                    "organisation_name": "string",
                    "organisation_code": "str",
                    "remarks": "string",
                    "identity_details": {
                        "identity_number": "string",
                        "other_identity_description": "string",
                        "identity_type": "AADHAAR_NUMBER",
                        "identity_image": {
                            "image_url": "https://picsum.photos/id/3/5000/3333.jpg",
                            "image_type": "OFFICIALLY_VALID_DOCUMENT_IN_RESPECT_OF_PERSON_AUTHORIZED_TO_TRANSACT",
                        },
                    },
                    "address_details": [
                        {
                            "address_type": "PERMANENT",
                            "address_line_1": "string",
                            "address_line_2": "string",
                            "address_line_3": "string",
                            "city": "string",
                            "district": "string",
                            "state": "ANDAMAN_AND_NICOBAR_ISLANDS",
                            "country": "AFGHANISTAN",
                            "pincode": "string",
                            "id_proof_and_address_proof_same": True,
                            "address_proof": "CERTIFICATE_OF_INCORPORATION_OR_FORMATION",
                            "address_proof_other_details": "string",
                            "address_proof_images": {
                                "image_url": "https://picsum.photos/id/4/5000/3333.jpg",
                                "image_type": "OFFICIALLY_VALID_DOCUMENT_IN_RESPECT_OF_PERSON_AUTHORIZED_TO_TRANSACT",
                            },
                        }
                    ],
                    "type_of_relationship": "GUARDIAN_OF_MINOR",
                    "director_identification_number": "string",
                }
            ],
        }
        self.indv_request_obj = IndividualEntityRequest(**self.indv_data)
        self.legal_request_obj = LegalEntityRequest(**self.legal_data)
        self.indv_request_dict = {
            **json.loads(self.indv_request_obj.json(exclude_unset=True)),
            **{"profile": "some_profile"},
        }
        self.legal_request_dict = {
            **json.loads(self.legal_request_obj.json(exclude_unset=True)),
            **{"profile": "some_profile"},
        }
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.get_api_mock.stop)
        self.sleep_mock = mock.patch("mercuryclient.mixins.ckyc.time.sleep").start()
        self.sleep_mock.return_value = None
        self.addCleanup(self.get_api_mock.stop)

    def test_request_ckyc_report(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_data = json.loads(self.indv_request_obj.json(exclude_unset=True))
        request_data["profile"] = "some_profile"
        self.client._initiate_ckyc_request(
            api="ckyc/indv/entity/upload/", request_dict=request_data
        )
        self.post_api_mock.assert_called_with(
            "api/v1/ckyc/indv/entity/upload/",
            data=self.indv_request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_data = json.loads(self.indv_request_obj.json(exclude_unset=True))
        request_data["profile"] = "some_profile"
        with self.assertRaises(Exception):
            self.client._initiate_ckyc_request(request_data)

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_data = json.loads(self.indv_request_obj.json(exclude_unset=True))
        request_data["profile"] = "some_profile"
        request_id = self.client._initiate_ckyc_request("some_profile", request_data)
        self.assertEqual(request_id, "random_string")

    def test_response_ckyc_report(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client._get_ckyc_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/ckyc/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.fetch_ckyc_result("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client._get_ckyc_response("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")

    def test_entire_request_response_flow_indv(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.create_indv_entity("some_profile", self.indv_request_obj)

        self.post_api_mock.assert_called_with(
            "api/v1/ckyc/indv/entity/upload/",
            data=self.indv_request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )
        self.get_api_mock.assert_called_with(
            "api/v1/ckyc/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )
        self.sleep_mock.assert_called_with(15)
        self.assertEqual(response["status"], "SUCCESS")

    def test_entire_request_response_flow_failure_indv(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "IN_PROGRESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        with self.assertRaises(Exception):
            self.client.create_indv_entity("some_profile", self.indv_request_obj)

    def test_entire_request_response_flow_legal(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        response = self.client.create_legal_entity(
            "some_profile", self.legal_request_obj
        )

        self.post_api_mock.assert_called_with(
            "api/v1/ckyc/legal/entity/upload/",
            data=self.legal_request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )
        self.get_api_mock.assert_called_with(
            "api/v1/ckyc/result",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )
        self.sleep_mock.assert_called_with(15)
        self.assertEqual(response["status"], "SUCCESS")

    def test_entire_request_response_flow_failure_legal(self):
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "IN_PROGRESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        with self.assertRaises(Exception):
            self.client.create_legal_entity("some_profile", self.legal_request_dict)
