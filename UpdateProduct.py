from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class UpdateProduct:
    producer:str ###= 'flex1879-uat.flexnetoperations.com',

    attribute_body = Template(
        "<urn:attribute>"
        "<urn:attributeName>"
        "$name"
        "</urn:attributeName>"
        "<urn:stringValue>"
        "$value"
        "</urn:stringValue>"
        "</urn:attribute>"
    )

    body = Template(
        "<urn:product>"
        "<urn:productIdentifier>"
        "<urn:primaryKeys>"
        "<urn:name>$name</urn:name>"
        "<urn:version>$version</urn:version>"
        "</urn:primaryKeys>"
        "</urn:productIdentifier>"
        "<urn:productAttributes>"
        "$attributes"
        "</urn:productAttributes>"
        "</urn:product>"
    )

    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='updateProductRequest',
            token="rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"
        )

    def make_attribute(self, name:str, value:str) -> str:
        self.attribute_body.substitute(
            name=name,
            value=value,
        )

    def execute(self,
        name:str,
        version:str,
        attributes:list[str]) -> Response:

        return self.get_request().post(self.body.substitute(
            name=name,
            version=version,
            attributes="".join(attributes)
        ))
