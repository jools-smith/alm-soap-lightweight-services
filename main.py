from pathlib import Path
import html
import xml.etree.ElementTree as ET

from DeleteSuite import DeleteSuite
from DeleteProduct import DeleteFeature, DeleteProduct
from GetAllSuites import GetAllSuites
from GetFeatures import GetFeatures
from GetProducts import GetProducts

root = Path(r"C:\Users\juliansmith\OneDrive - Flexera, Inc\Assignments\Velotic\thingworx")

# FlexNet Operations SOAP endpoint
# SOAP_URL = "https://flex13061.flexnetoperations.eu/flexnet/services/v7/UserAcctHierarchyService"
SOAP_URL = "https://flex1879-uat.flexnetoperations.com/flexnet/services/v3/ProductPackagingService"
# BEARER_TOKEN = "rna_89d0e7e2addad3d988a701f282cc3a0750ba7be21371"
BEARER_TOKEN = "rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"

PRODUCER="flex1879-uat.flexnetoperations.com"
# chunk_size = 25
# chunks: Any


# service = GetAllSuites(PRODUCER)
# service = GetProducts(PRODUCER)

# response = service.execute(page_number=1, batch_size=512, return_all=False)

service = GetFeatures(PRODUCER)
response = service.execute(page_number=1, batch_size=512)
print(response.content)

if response.status_code == 200:
    doc = ET.fromstring(html.unescape(response.content.decode("utf-8")))

    ns = {
        "fs": "urn:v3.webservices.operations.flexnet.com"
    }

    unique_ids = [
        item.findtext("fs:uniqueId", namespaces=ns)
        for item in doc.findall(".//fs:feature", ns)
    ]

    print("\n".join(unique_ids))

    # service = DeleteSuite(PRODUCER)
    service = DeleteFeature(PRODUCER)

    for i in range(0, len(unique_ids), 25):

        values = unique_ids[i:i + 25]

        response = service.execute_many(values=values)

        print(i, values, response.status_code)

        if response.status_code != 200:
            print(i, response.status_code, response.content)


    # for hid in unique_ids:
    #     response = service.execute_many(hid=hid)
    #
    #     print(i, hid, response.status_code)
    #
    #     if response.status_code != 200:
    #         print(i, response.status_code, response.content)
    #
    #     i += 1


