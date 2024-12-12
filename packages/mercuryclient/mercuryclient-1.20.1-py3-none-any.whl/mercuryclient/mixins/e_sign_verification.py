from urllib.parse import urlparse
import PyPDF2
import requests
from io import BytesIO


class ESignVerification:
    """ """

    def _download_pdf_from_url(self, pdf_url):
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return None
        content_type = response.headers.get("Content-Type", "")
        if "application/pdf" in content_type or response.content.startswith(b"%PDF"):
            return BytesIO(response.content)

    def check_e_sign(self, profile, provider, pdf_path):
        # Open the PDF file
        file_content = self._download_pdf_from_url(pdf_path)
        parsed_url = urlparse(pdf_path)
        file_name = parsed_url.path.split("/")[-1]
        if not file_content:
            raise Exception("Document file must be a PDF")
        # Create a PDF reader object
        reader = PyPDF2.PdfFileReader(file_content)
        # Check if the document has signature fields
        signature_count = 0
        number_of_pages = len(reader.pages)
        sign_per_page = {}
        for page_no, page in enumerate(reader.pages, start=1):
            per_page_sign = 0
            fields = page.get("/Annots")
            if fields:
                for field in fields:
                    field_obj = field.getObject()
                    if field_obj.get("/FT") == "/Sig":
                        signature_count += 1
                        per_page_sign += 1
            sign_per_page[f"page_{page_no}"] = per_page_sign

        api = "api/v1/e_sign/verify/"
        request_data = dict(
            profile=profile,
            provider=provider,
            signature_count=signature_count,
            file_name=file_name,
            number_of_pages=number_of_pages,
            sign_per_page=sign_per_page,
        )
        request_id, r = self._post_json_http_request(
            api, data=request_data, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 200:
            return request_id, r.json()

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending e-signature request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
