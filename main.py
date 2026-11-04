import html
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
import json
from pprint import pprint

from CreateFeature import CreateFeature
from CreateProduct import CreateProduct
from DeleteFeature import DeleteFeature
from GetFeatures import GetFeatures

ROOT = Path(r"C:\Users\juliansmith\OneDrive - Flexera, Inc\Assignments\Velotic\thingworx")
PRODUCER="flex1879-uat.flexnetoperations.com"
# SOAP_URL = "https://flex1879-uat.flexnetoperations.com/flexnet/services/v3/ProductPackagingService"
BEARER_TOKEN = "rna_1d532555e9e08188072902dcbe3c860e5f4f67337158"


@dataclass
class Feature:
    name: str
    version: str
    description: str
    vendorString: str
    quantity: str

@dataclass
class Product:
    name: str
    version: str
    description: str
    productName: str
    isForced: str
    isForcedException: str
    delayedEnforcement: str
    licenseModel: str
    quantity: str
    features: list[Feature] = field(default_factory=list)

@dataclass
class Suite:
    name: str
    version: str
    description: str
    productName: str
    isForced: str
    isForcedException: str
    delayedEnforcement: str
    licenseModel: str
    products: list[Product] = field(default_factory=list)

@dataclass
class Orderables:
    accepted: list[Suite] = field(default_factory=list)
    accepted_products:list[Product] = field(default_factory=list)
    accepted_featureless_products:list[Product] = field(default_factory=list)
    accepted_features: list[Feature] = field(default_factory=list)
    rejected: list[Suite] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

@dataclass
class ThingWorxData:
    orderables:Orderables
    unnamed_servicables_with_no_features: list[Product] = field(default_factory=list)
    named_servicables_with_no_features: list[Product] = field(default_factory=list)
    accepted_orderables_with_no_product_name: list[Suite] = field(default_factory=list)

def delete_all_features():
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

        service = DeleteFeature(PRODUCER)

        for i in range(0, len(unique_ids), 25):

            values = unique_ids[i:i + 25]

            response = service.execute_many(values=values)

            print(i, values, response.status_code)

            if response.status_code != 200:
                print(i, response.status_code, response.content)



class Constants:
    LICENSE_TECHNOLOGY = 'FlexNet Licensing'
    LICENSE_GENERATOR = 'demo'
    LICENSE_MODEL = 'THINGWORX'
    FEATURE_VERSION = '8.0'
    SUITE_VERSION = 'Orderable'
    PRODUCT_VERSION = 'Serviceable'
    ATT_PRODUCT_NAME = "ProductName"
    ATT_DELAYED_ENFORCEMENT = "DelayedEnforcement"
    ATT_LICENSE_MODEL = "LicenseModel"
    ATT_IS_ENFORCED = "IsEnforced"
    ATT_IS_ENFORCED_EXCEPTION = "IsEnforcedException"

    @staticmethod
    def integer_string(value: str) -> str:
        # print("VERSION", value)
        whole, dot, fraction = value.partition(".")

        if dot and int(fraction) != 0:
            raise ValueError(f"Not an integer: {value}")

        return str(int(whole))


def create_features(features, feature_version):
    service = CreateFeature(PRODUCER, BEARER_TOKEN)

    for feature in features:

        payload = (service.make_feature(
            name=feature["name"],
            version=feature_version,
            version_format="FIXED",
            description=feature["description"],
            vendor_string=feature["vendorString"])
        )

        response = service.execute(payload)

        print(response)



def get_failed_reason(xml: str | bytes) -> str | None:
    root = ET.fromstring(xml)

    ns = {
        "fn": "urn:v3.webservices.operations.flexnet.com"
    }

    reason = root.find(
        ".//fn:failedData/fn:failedProduct/fn:reason",
        ns
    )

    return reason.text if reason is not None else None

def create_products(products, license_technology, license_generator, license_model, product_version, feature_version):
    service = CreateProduct(PRODUCER, BEARER_TOKEN)

    index = 0

    ## peoducts may be duplicated becuase of suite counts

    unique_products = {obj["name"]: obj for obj in products}

    for product in unique_products.values():
        # print(feature)
        index += 1
        print(f"{index} of {len(unique_products)} {product["name"]}")
        
        # pprint(product["features"])
        features = [ service.make_feature(
            name=feature["name"],
            version=feature_version,
            count=Constants.integer_string(feature["quantity"]))
            for feature in product["features"]
        ]

        attributes = [
            service.make_boolean_attribute(
                name=name,
                value=value
            ) if is_bool else
            service.make_string_attribute(
                name=name,
                value=value
            )
            for name, value, is_bool in [
                (Constants.ATT_LICENSE_MODEL, product["licenseModel"], False),
                (Constants.ATT_DELAYED_ENFORCEMENT, product["delayedEnforcement"], False),
                (Constants.ATT_PRODUCT_NAME, product["productName"], False),
                (Constants.ATT_IS_ENFORCED, product["isForced"], True),
                (Constants.ATT_IS_ENFORCED_EXCEPTION, product["isForcedException"], True),
            ]
        ]

        response = service.execute(
            name=product["name"],
            version=product_version,
            description=product["description"],
            technology=license_technology,
            generator=license_generator,
            models=license_model,
            features=features,
            attributes=attributes
        )

        reason = get_failed_reason(response.content)
        if reason is not None:
            print(product["name"], reason)
            exit(0)



def load_thingworx_data():
    print("Loading ThingWorx data...")

    orderables = None

    with open(ROOT / "ptc-revenera-orderables.json", "r", encoding="utf-8") as f:
        orderables = json.load(f)

    # create_features(orderables["orderables"]["accepted_features"])

    create_products(
        products=orderables["orderables"]["accepted_products"],
        ### constant values
        license_technology=Constants.LICENSE_TECHNOLOGY,
        license_generator=Constants.LICENSE_GENERATOR,
        license_model=Constants.LICENSE_MODEL,
        product_version=Constants.PRODUCT_VERSION,
        feature_version=Constants.FEATURE_VERSION
    )





if __name__ == "__main__":
    print("Here we go...")
    load_thingworx_data()