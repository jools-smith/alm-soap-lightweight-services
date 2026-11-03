from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class GetAllSuites:
    producer:str ###= 'flex1879-uat.flexnetoperations.com',


    body=Template(
        "<urn:queryParams>"
        "</urn:queryParams>"
        "<urn:pageNumber>$pageNumber</urn:pageNumber>"
        "<urn:batchSize>$batchSize</urn:batchSize>"
        "<urn:returnContainedObjects>$returnContainedObjects</urn:returnContainedObjects>"
    )


    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='getUniformSuitesQueryRequest',
            token="rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"
        )

    def execute(self,page_number, batch_size, return_all) -> Response:
        return self.get_request().post(
            self.body.substitute(
                pageNumber=page_number,
                batchSize=batch_size,
                returnContainedObjects=return_all
            )
        )

