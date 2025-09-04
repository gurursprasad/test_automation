import json

from utils.common_utils import *


updated_profile_name = ""


def append_random_id_to_payload():
    json_payloads = ["rest-api-payloads/addEnvironment.json", "rest-api-payloads/addProfile.json", 
                     "rest-api-payloads/createVm.json", "rest-api-payloads/custImageVm.json", 
                     "rest-api-payloads/parseVm.json"]
    random_id = generate_random_id()

    for payload in json_payloads:
        path = build_configuration_file_path(payload)
        if path is None:
            print(f"Unable to find the payload {payload}")
            continue

        try:
            with open(path, "r") as file:
                data = json.load(file)

            if payload in ["rest-api-payloads/addProfile.json", "rest-api-payloads/createVm.json", "rest-api-payloads/custImageVm.json"]:
                data["ProfileName"] = "pytest" + random_id

            elif payload == "rest-api-payloads/parseVm.json":
                data["ImageName"] = "pytest-image-" + random_id

            elif payload == "rest-api-payloads/addEnvironment.json":
                data["Pools"][0]["ProfileName"] = "pytest" + random_id
    

            with open(path, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"An error occurred while processing {payload}: {e}")
