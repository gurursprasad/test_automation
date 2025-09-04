import time

import pytest
import requests

from utils.base_class import BaseClass
from utils.rest_api_util import *

parse_job_id = ""
updatecompute_job_id = ""
node_names = []
license_expired = False

class Test_computeRestApis(BaseClass):

    # profiles:
    # addProfile
    # updateProfile
    # getProfiles
    # getProfileByName
    # removeProfile - This needs to be run finally at the end of all tests.
    def test_getProfileByName_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/profile/az1"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            response_data = response.json()
            logger.info("Response Status Code: " + str(response.status_code))
            assert response_data["ProfileName"] == "az1"

            with open(build_configuration_file_path("rest-api-payloads/addProfile.json"), "w") as f:
                json.dump(response_data, f)

        except (AssertionError, TypeError, AttributeError, FileNotFoundError) as e:
            assert False, f"An error occurred: {str(e)}"


    def test_addProfile_api(self, setup_server_ip):
        try:
            append_random_id_to_payload() # appends random id to all the payloads
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/profile"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addProfile.json")) as f:
                data = json.load(f)
            response = requests.post(api_url, headers=headers, json=data)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert response_data is not None
            data["Id"] = response_data["Id"]
            with open(build_configuration_file_path("rest-api-payloads/addProfile.json"), "w") as f:
                json.dump(data, f, indent=2)
        except (AssertionError, TypeError, AttributeError, FileNotFoundError) as e:
            assert False, f"An error occurred: {e}"


    def test_updateProfile_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/profile"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addProfile.json")) as f:
                data = json.load(f)
            response = requests.put(api_url, headers=headers, json=data)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert response_data is not None
            data["Id"] = response_data["Id"]
            with open(build_configuration_file_path("rest-api-payloads/addProfile.json"), "w") as f:
                json.dump(data, f, indent=2)
        except (AssertionError, TypeError, AttributeError, FileNotFoundError) as e:
            assert False, f"An error occurred: {str(e)}"


    def test_getProfiles_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/profiles"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert response_data is not None
            assert isinstance(response_data["Profiles"], list)
        except (AssertionError, TypeError, AttributeError, FileNotFoundError) as e:
            assert False, f"An error occurred: {str(e)}"



    # envs:
    # addEnvironment
    # updateEnvironment
    # getEnvironments
    # getEnvironmentByName
    # removeEnvironment
    def test_addEnvironment_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/env"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json")) as f:
                data = json.load(f)
            response = requests.post(api_url, headers=headers, json=data)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response_data["Id"] is not None
            assert "error" not in response_data
            data["Id"] = response_data["Id"]
            with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json"), "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    def test_updateEnvironment_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/env"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json")) as f:
                data = json.load(f)
            response = requests.put(api_url, headers=headers, json=data)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert "Id" in response_data
            data["Id"] = response_data["Id"]
            with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json"), "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    def test_getEnvironments_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/envs"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert "Environments" in response_data
            assert isinstance(response_data["Environments"], list)
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    def test_getEnvironmentByName_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json")) as f:
                data = json.load(f)
            env_name = data["EnvName"]
            api_url = f"http://{setup_server_ip}:5000/v1/env/{env_name}"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            response_data = response.json()
            assert response.status_code == 200
            assert response_data["EnvName"] == env_name
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    # images:
    # addImage
    # updateImage
    # getImages
    # getImageByName
    # removeImage
    def test_addImage_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/image"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addImage.json"), "r") as f:
                request_data = json.load(f)
            response = requests.post(api_url, headers=headers, json=request_data)
            if response is None:
                raise Exception("Null pointer exception: 'response' is null")
            response_data = response.json()
            if response_data is None:
                raise Exception("Null pointer exception: 'response_data' is null")
            if response.status_code != 200:
                raise Exception(f"Received HTTP status code {response.status_code}")
            request_data["Id"] = response_data["Id"]
            logger.info("Response Status Code: " + str(response.status_code))
            with open(build_configuration_file_path("rest-api-payloads/addImage.json"), "w") as f:
                json.dump(request_data, f, indent=2)
        except Exception as e:
            assert False, str(e)


    def test_updateImage_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/image"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addImage.json"), "r") as f:
                request_data = json.load(f)
            if request_data is None:
                raise Exception("Null pointer exception: 'request_data' is null")
            response = requests.put(api_url, headers=headers, json=request_data)
            logger.info("Response Status Code: " + str(response.status_code))
            if response is None:
                raise Exception("Null pointer exception: 'response' is null")
            if response.status_code != 200:
                raise Exception(f"Received HTTP status code {response.status_code}")
        except Exception as e:
            assert False, str(e)


    def test_getImages_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/images"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            if response is None:
                raise Exception("Null pointer exception: 'response' is null")
            response_data = response.json()
            if response_data is None:
                raise Exception("Null pointer exception: 'response_data' is null")
            if response.status_code != 200:
                raise Exception(f"Received HTTP status code {response.status_code}")
            if "Images" not in response_data:
                raise Exception("Unexpected response data: 'Images' key is missing")
            if not isinstance(response_data["Images"], list):
                raise Exception("Unexpected response data: 'Images' value is not a list")
        except Exception as e:
            assert False, str(e)


    def test_getImageByName_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            with open(build_configuration_file_path("rest-api-payloads/addImage.json"), "r") as f:
                request_data = json.load(f)
            if request_data is None:
                raise Exception("Null pointer exception: 'request_data' is null")
            image_name = request_data["ImageName"]
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/image/{image_name}"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            if response is None:
                raise Exception("Null pointer exception: 'response' is null")
            response_data = response.json()
            if response_data is None:
                raise Exception("Null pointer exception: 'response_data' is null")
            if response.status_code != 200:
                raise Exception(f"Received HTTP status code {response.status_code}")
            if "ImageName" not in response_data:
                raise Exception("Unexpected response data: 'ImageName' key is missing")
            if response_data["ImageName"] != image_name:
                raise Exception(
                    f"Unexpected response data: 'ImageName' value is not '{image_name}'"
                )
        except Exception as e:
            assert False, str(e)


    # License:
    # addLicense
    # getLicense
    def test_addLicense_api(self, setup_server_ip):
        global license_expired
        try:
            logger = self.getlogger()
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/license"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/addLicense.json"), "r") as f:
                request_data = json.load(f)
            response = requests.post(api_url, headers=headers, json=request_data)
            logger.info("Response Status Code: " + str(response.status_code))
            if response.status_code == 400:
                if "expired" in response.text:
                    license_expired = True
                    pytest.skip("License has expired, skipping test.")
            assert response.status_code == 200
        except Exception as e:
            assert False, str(e)


    def test_getLicense_api(self, setup_server_ip):
        global license_expired
        try:
            logger = self.getlogger()
            if license_expired:
                pytest.skip("License has expired, skipping test.")
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/license/compute"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.get(api_url, headers=headers)
            logger.info("Response Status Code: " + str(response.status_code))
            assert response.status_code == 200
        except Exception as e:
            assert False, str(e)


    # compute:
    #     createVm
    #     getVms
    #     getVmByName
    #     removeVm

    #     getUpdateList
    #     updatecompute
    #     getUpdateStatusByJobId

    #     parseVm - Need info on the parameters that are passed with the request
    #     getParseStatusByJobId - Need info on the parameters that are passed with the request

    #     downloadFile - Need info on how to use the api
    def test_createVm_api(self, setup_server_ip):
        try:
            logger = self.getlogger()
            head_node_url = setup_server_ip
            api_url = f"http://{head_node_url}:5000/v1/compute/vm"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/custImageVm.json"), "r") as f:
                assert f is not None, "Null pointer exception: 'f' is null"
                request_data = f.read()
                assert (request_data is not None), "Null pointer exception: 'request_data' is null"
            response = requests.post(api_url, headers=headers, data=request_data)
            logger.info("Response Status Code: " + str(response.status_code))
            assert response is not None, "Null pointer exception: 'response' is null"
            response_data = response.json()
            assert (response_data is not None), "Null pointer exception: 'response_data' is null"
            assert (
                response.status_code == 200
            ), "Request failed with status code: {}".format(response.status_code)
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    def test_parseVm_api(self, setup_server_ip):
        global parse_job_id
        try:
            logger = self.getlogger()
            api_url = f"http://{setup_server_ip}:5000/v1/compute/parse"
            logger.info("API URL: " + api_url)
            headers = {"Content-Type": "application/json"}
            with open(build_configuration_file_path("rest-api-payloads/parseVm.json"), "r") as f:
                assert f is not None, "Null pointer exception: 'f' is null"
                request_data = f.read()
                assert (request_data is not None), "Null pointer exception: 'request_data' is null"
            response = requests.post(api_url, headers=headers, data=request_data)
            response_data = response.json()
            logger.info("Response Status Code: " + str(response.status_code))
            assert (response_data is not None), "Null pointer exception: 'response_data' is null"
            assert "JobId" in response_data, "Expected JobId in response"
            assert (response.status_code == 200), "Request failed with status code: {}".format(response.status_code)
            parse_job_id = response_data["JobId"]
            print(parse_job_id)
            assert (parse_job_id is not None), "parse_job_id is not set. Hence skipping the test!!"
        except (Exception, AssertionError) as e:
            assert False, f"An unexpected error occurred: {str(e)}"


    def test_getParseStatusByJobId_api(self, setup_server_ip):
        global parse_job_id
        logger = self.getlogger()
        assert (
            parse_job_id is not None
        ), "parse_job_id is not set. Hence skipping the test!!"
        head_node_url = setup_server_ip
        api_url = f"http://{head_node_url}:5000/v1/compute/parse/{parse_job_id}"
        logger.info("API URL: " + api_url)
        headers = {"Accept": "application/json"}
        max_wait_time = 1200
        start_time = time.time()
        while True:
            try:
                response = requests.get(api_url, headers=headers)
                assert response is not None, "Null pointer exception: 'response' is null"
                status_code = response.status_code
                assert status_code in [
                    200,
                    102,
                    404,
                ], f"Unexpected status code: {status_code}"
                if status_code == 200:
                    logger.info("Response Status Code: " + str(response.status_code))
                    break
                elif time.time() - start_time >= max_wait_time:
                    assert False, "Parse not completed within  minutes."
                elif status_code == 102:
                    time.sleep(2)
                elif status_code == 404:
                    assert False, "Job ID not found."
                else:
                    assert False, "Unexpected status code: {}".format(status_code)
            except (Exception, AssertionError) as e:
                assert False, f"An error occurred: {str(e)}"


    def test_getUpdateList_api(self, setup_server_ip):
        logger = self.getlogger()
        head_node_url = setup_server_ip
        api_url = f"http://{head_node_url}:5000/v1/compute/updates"
        logger.info("API URL: " + api_url)
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(api_url, headers=headers)
            assert response is not None, "Null pointer exception: 'response' is null"
            response_data = response.json()
            logger.info("Response Status Code: " + str(response.status_code))
            assert (
                response_data is not None
            ), "Null pointer exception: 'response_data' is null"
            with open(build_configuration_file_path("rest-api-payloads/updateList.json"), "w") as json_file:
                json.dump(response_data, json_file)
            assert response.status_code == 200
            assert response_data is not None
            assert "UpdateList" in response_data
            assert response_data["UpdateList"] is not None
            assert isinstance(response_data["UpdateList"], list)
            time.sleep(3)
        except Exception as e:
            assert False, f"An error occurred: {str(e)}"


    # def test_updatecompute_api(self, setup_server_ip):
    #     logger = self.getlogger()
    #     head_node_url = setup_server_ip
    #     api_url = f"http://{head_node_url}:5000/v1/compute/update"
    #     logger.info("API URL: " + api_url)
    #     with open(build_configuration_file_path("rest-api-payloads/updateList.json")) as update_file:
    #         update_list = json.load(update_file).get("UpdateList", [])
    #         assert update_file is not None, "Null pointer exception: 'update_file' is null"
    #     if not update_list:
    #         pytest.skip("No updates available, skipping test.")
    #     update_data = {"computeVersion": update_list[0]}
    #     headers = {"Content-Type": "application/json", "Accept": "application/json"}
    #     update_json = json.dumps(update_data)
    #     assert update_json is not None, "Null pointer exception: 'update_json' is null"
    #     try:
    #         response = requests.post(api_url, headers=headers, data=update_json)
    #         assert response is not None, "Null pointer exception: 'response' is null"
    #         response_data = response.json()
    #         assert (response_data is not None), "Null pointer exception: 'response_data' is null"
    #         assert "JobId" in response_data, "Expected JobId in response"
    #         global updatecompute_job_id
    #         updatecompute_job_id = response_data["JobId"]
    #         logger.info("Response Status Code: " + str(response.status_code))
    #         assert (updatecompute_job_id is not None), "update_job_id is not set. Hence skipping!!"
    #     except (json.decoder.JSONDecodeError, requests.exceptions.RequestException) as e:
    #         assert False, f"An error occurred: {str(e)}"


    # def test_getUpdateStatusByJobId_api(self, setup_server_ip):
    #     global updatecompute_job_id
    #     logger = self.getlogger()
    #     with open(build_configuration_file_path("rest-api-payloads/updateList.json")) as update_file:
    #         update_list = json.load(update_file).get("UpdateList", [])
    #         assert update_file is not None, "Null pointer exception: 'update_file' is null"
    #     if not update_list:
    #         pytest.skip("No updates available, skipping test.")
    #     head_node_url = setup_server_ip
    #     api_url = f"http://{head_node_url}:5000/v1/compute/update/{updatecompute_job_id}"
    #     logger.info("API URL: " + api_url)
    #     headers = {"Accept": "application/json"}
    #     max_wait_time = 240  # 3 minutes
    #     start_time = time.time()
    #     try:
    #         while True:
    #             response = requests.get(api_url, headers=headers)
    #             assert response is not None, "Null pointer exception: 'response' is null"
    #             status_code = response.status_code
    #             assert (status_code is not None), "Null pointer exception: 'status_code' is null"
    #             if status_code == 200:
    #                 break
    #             elif time.time() - start_time >= max_wait_time:
    #                 assert False, "Update not completed within 3 minutes."
    #             elif status_code == 102:
    #                 time.sleep(2)
    #             elif status_code == 404:
    #                 assert False, "Job ID not found."
    #             elif status_code == 400:
    #                 assert False, "Bad Request. Invalid request supplied!! Status Code: {}"
    #             else:
    #                 assert False, f"Unexpected status code: {status_code}"
    #     except (AssertionError, Exception) as e:
    #         assert False, f"An error occurred: {str(e)}"


    # Remove api's
    def test_removeVm_api(self, setup_server_ip):
        logger = self.getlogger()
        global node_names
        head_node_url = setup_server_ip
        api_url = f"http://{head_node_url}:5000/v1/compute/vms"
        logger.info("API URL: " + api_url)
        headers = {"Accept": "application/json"}
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        for vm in response_data["Vms"]:
            node_names.append(vm["NodeName"])
        try:
            for node_name in node_names:
                if node_name == "pytest":
                    api_url = f"http://{head_node_url}:5000/v1/compute/vm/{node_name}"
                    headers = {"Accept": "application/json"}
                    response = requests.delete(api_url, headers=headers)
                    if response is None:
                        raise ValueError("Null pointer exception: 'response' is null")
                    try:
                        response.raise_for_status()
                    except (
                        requests.exceptions.HTTPError,
                        requests.exceptions.RequestException,
                    ) as e:
                        raise ValueError(str(e))
        except (ValueError, TypeError) as e:
            assert False, str(e)


    def test_removeEnvironment_api(self, setup_server_ip):
        logger = self.getlogger()
        head_node_url = setup_server_ip
        with open(build_configuration_file_path("rest-api-payloads/addEnvironment.json"), "r") as f:
            data = json.load(f)
        env_name = data["EnvName"]
        try:
            api_url = f"http://{head_node_url}:5000/v1/env/{env_name}"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.delete(api_url, headers=headers)
            assert response is not None, "Null pointer exception: 'response' is null"
            try:
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise AssertionError(f"An error occurred: {str(e)}") from e
        except (AssertionError, AttributeError) as e:
            raise AssertionError(f"An error occurred: {str(e)}") from e
        except Exception as e:
            raise AssertionError(f"An unhandled exception occurred: {str(e)}") from e


    def test_removeImage_api(self, setup_server_ip):
        logger = self.getlogger()
        head_node_url = setup_server_ip
        with open(build_configuration_file_path("rest-api-payloads/addImage.json"), "r") as f:
            data = json.load(f)
        image_name = data["ImageName"]
        try:
            api_url = f"http://{head_node_url}:5000/v1/image/{image_name}"
            logger.info("API URL: " + api_url)
            headers = {"Accept": "application/json"}
            response = requests.delete(api_url, headers=headers)
            if response is None:
                assert False, "Null pointer exception: 'response' is null"
            response.raise_for_status()
            assert response.status_code == 200, "Received HTTP status code " + str(
                response.status_code
            )
        except (AssertionError, requests.exceptions.RequestException) as e:
            assert False, f"An error occurred: {str(e)}"


    def test_removeProfile_api(self, setup_server_ip):
        logger = self.getlogger()
        head_node_url = setup_server_ip
        with open(build_configuration_file_path("rest-api-payloads/addProfile.json"), "r") as f:
            data = json.load(f)
        profile_name = data["ProfileName"]
        try:
            api_url = f"http://{head_node_url}:5000/v1/profile/{profile_name}"
            headers = {"Accept": "application/json"}
            logger.info("API URL: " + api_url)
            response = requests.delete(api_url, headers=headers)
            assert response is not None, "Null pointer exception: 'response' is null"
            try:
                response.raise_for_status()
            except (
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
            ) as e:
                assert False, f"An error occurred: {str(e)}"
            assert response.status_code == 200, "Received HTTP status code " + str(
                response.status_code
            )
        except (AssertionError, TypeError, AttributeError) as e:
            assert False, f"An error occurred: {str(e)}"            


    # # def test_removeVm_api():
    # #     try:
    # #         head_node_url = setup_server_ip

    # #         for node_name in node_names:
    # #             api_url = f"http://{head_node_url}:5000/v1/compute/vm/{node_name}"
    # #             headers = {"Accept": "application/json"}

    # #             response = requests.delete(api_url, headers=headers)

    # #             assert response is not None, "Null pointer exception: 'response' is null"

    # #             assert (
    # #                 response.status_code == 200
    # #             ), "Request failed with status code: {}".format(response.status_code)

    # #         time.sleep(3)
    # #         for node_name in node_names:
    # #             api_url = f"http://{head_node_url}:5000/v1/compute/vm/{node_name}"
    # #             headers = {"Accept": "application/json"}

    # #             response = requests.get(api_url, headers=headers)

    # #             assert response is not None, "Null pointer exception: 'response' is null"

    # #             assert (
    # #                 response.status_code == 404
    # #             ), "Request failed with status code: {}".format(response.status_code)
    # #     except Exception as e:
    # #         assert False, f"An error occurred: {str(e)}"
