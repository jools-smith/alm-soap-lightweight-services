from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class DeleteProduct:
    producer:str ###= 'flex1879-uat.flexnetoperations.com',

    body = Template(
        "<urn:product>"
        "<urn:productIdentifier>"
        "<urn:uniqueId>$hid</urn:uniqueId>"
        "</urn:productIdentifier>"
        "</urn:product>"
    )

    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='deleteProductRequest',
            token="rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"
        )

    def execute(self,hid) -> Response:
        return self.get_request().post(
            self.body.substitute(
                hid=hid
            )
        )

    def execute_many(self, values: list[str]) -> Response:
        bodies = [
            self.body.substitute(hid=hid)
            for hid in values
        ]

        return self.get_request().post("".join(bodies))

