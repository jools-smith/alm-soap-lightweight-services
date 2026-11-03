from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class CreateSuite:
    producer:str ###= 'flex1879-uat.flexnetoperations.com',

    product_body = Template(
        "<urn:product>"
        "<urn:productIdentifier>"
        "<urn:primaryKeys>"
        "<urn:name>$name</urn:name>"
        "<urn:version>$version</urn:version>"
        "</urn:primaryKeys>"
        "</urn:productIdentifier>"
        "<urn:count>$count</urn:count>"
        "</urn:product>"
    )

    body = Template(
        "<urn:uniformSuite>"
        "<urn:suiteName>$name</urn:suiteName>"
        "<urn:version>$version</urn:version>"
        "<urn:description>$description</urn:description>"
        "<urn:licenseTechnology>"
        "<urn:primaryKeys>"
        "<urn:name>$license_technology</urn:name>"
        "</urn:primaryKeys>"
        "</urn:licenseTechnology>"
        "<urn:licenseGenerator>"
        "<urn:primaryKeys>"
        "<urn:name>$license_generator</urn:name>"
        "</urn:primaryKeys>"
        "</urn:licenseGenerator>"
        "<urn:products>$product_list</urn:products>"
        "<urn:licenseModels>"
        "<urn:licenseModel>"
        "<urn:primaryKeys>"
        "<urn:name>$license_models</urn:name>"
        "</urn:primaryKeys>"
        "</urn:licenseModel>"
        "</urn:licenseModels>"
        "<urn:usedOnDevice>true</urn:usedOnDevice>"
        "</urn:uniformSuite>"
    )

    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='createUniformSuiteRequest',
            token="rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"
        )

    def make_product(self, name:str, version:str, count:int) -> str:
        self.product_body.substitute(
            name=name,
            version=version,
            count=count
        )

    def execute(self,
        name:str,
        version:str,
        description:str, technology:str, generator:str, models:str, products:list[str]) -> Response:

        return self.get_request().post(self.body.substitute(
            name=name,
            version=version,
            description=description,
            license_technology=technology,
            license_generator=generator,
            license_models=models,
            products="".join(products)
        ))
