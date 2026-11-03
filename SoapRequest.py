from dataclasses import dataclass
from string import Template

import requests
from requests import Response


@dataclass(frozen=True)
class SoapRequest:
    producer:str
    service:str
    version:str
    endpoint:str
    version:str
    endpoint:str
    token:str

    body = Template("""
    <soapenv:Envelope
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:urn="urn:$version.webservices.operations.flexnet.com">
        <soapenv:Header/>
        <soapenv:Body>
            <urn:$endpoint>
                $payload
            </urn:$endpoint>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    )

    def get_request(self, content:str) -> str:
       return self.body.substitute(
            version=self.version,
            endpoint=self.endpoint,
            payload=content
       )


    def post(self, body:str) -> Response:

        # print(self.get_request(body))

        return  requests.post(
            f'https://{self.producer}/flexnet/services/{self.service}',
            data=self.get_request(body),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": ''"#POST"'',
                "Authorization": f"Bearer {self.token}"
            },
            timeout=60
        )
