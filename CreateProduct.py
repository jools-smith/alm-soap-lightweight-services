from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class CreateProduct:
    producer:str
    token:str

    feature_body = Template(
        "<urn:feature>"
        "<urn:featureIdentifier>"
        "<urn:primaryKeys>"
        "<urn:name>$name</urn:name>"
        "<urn:version>$version</urn:version>"
        "</urn:primaryKeys>"
        "</urn:featureIdentifier>"
        "<urn:count>$count</urn:count>"
        "</urn:feature>"
    )

    string_attribute_body = Template(
        "<urn:attribute>"
        "<urn:attributeName>$name</urn:attributeName>"
        "<urn:stringValue>$value</urn:stringValue>"
        "</urn:attribute>"
    )

    boolean_attribute_body = Template(
        "<urn:attribute>"
        "<urn:attributeName>$name</urn:attributeName>"
        "<urn:booleanValue>$value</urn:booleanValue>"
        "</urn:attribute>"
    )

    body = Template(
        "<urn:product>"
        "<urn:productName>$name</urn:productName>"
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
        "<urn:features>$features</urn:features>"
        "<urn:licenseModels>"
        "<urn:licenseModel>"
        "<urn:primaryKeys>"
        "<urn:name>$license_models</urn:name>"
        "</urn:primaryKeys>"
        "</urn:licenseModel>"
        "</urn:licenseModels>"
        "<urn:usedOnDevice>true</urn:usedOnDevice>"
        
        "<urn:productAttributes>$attributes</urn:productAttributes>"
        
        "</urn:product>"
    )

    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='createProductRequest',
            token=self.token
        )

    def make_feature(self, name:str, version:str, count:str) -> str:
        return self.feature_body.substitute(
            name=name,
            version=version,
            count=count
        )

    def make_string_attribute(self, name:str, value:str) -> str:
        return self.string_attribute_body.substitute(
            name=name,
            value=value
        )

    def make_boolean_attribute(self, name:str, value:str) -> str:
        return self.boolean_attribute_body.substitute(
            name=name,
            value=value
        )

    def execute(self,
        name:str,
        version:str,
        description:str, technology:str, generator:str, models:str, features:list[str], attributes:list[str]) -> Response:

        return self.get_request().post(self.body.substitute(
            name=name,
            version=version,
            description=description,
            license_technology=technology,
            license_generator=generator,
            license_models=models,
            features="".join(features),
            attributes="".join(attributes),
        ))
