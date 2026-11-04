from dataclasses import dataclass
from string import Template

from requests import Response

from SoapRequest import SoapRequest


@dataclass(frozen=True)
class CreateFeature:
    producer:str ###= 'flex1879-uat.flexnetoperations.com',
    token:str

    feature_body = Template(
        "<urn:feature>"
        "<urn:featureName>$name</urn:featureName>"
        "<urn:versionFormat>$versionFormat</urn:versionFormat>"
        "<urn:version>$version</urn:version>"
        "<urn:description>$description</urn:description>"
        "<urn:featureOverrideParams>"
        "<urn:vendorString>$vendorString</urn:vendorString>"
        "</urn:featureOverrideParams>"
        "</urn:feature>"
    )

    body = Template(
        "$features"
    )

    def get_request(self) -> SoapRequest:
        return SoapRequest(
            producer=self.producer,
            service='v3/ProductPackagingService',
            version='v3',
            endpoint='createFeatureRequest',
            token=self.token
        )

    def make_feature(self, name:str, version:str, version_format:str, description:str, vendor_string:str) -> str:
        return self.feature_body.substitute(
            name=name,
            version=version,
            versionFormat=version_format,
            description=description,
            vendorString=vendor_string
        )

    def execute(self, feature:str) -> Response:
        return self.get_request().post(self.body.substitute(
            features=feature
        ))

    def execute_many(self, features:list[str]) -> Response:
        return self.get_request().post(self.body.substitute(
            features="".join(features)
        ))
