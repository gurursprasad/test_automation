import json
import os
import random
import string
import time
import datetime
import uuid

import boto3
import botocore
import requests


def get_public_ip():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(
            InstanceIds=[os.environ.get("HEAD_NODE_EC2_INSTANCE_ID")]
        )

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                public_dns_name = instance.get("PublicIpAddress", "Not available")
                return public_dns_name
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while retrieving public DNS: {e}")
        return "Not available"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Not available"
    

def get_private_ip():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(
            InstanceIds=[os.environ.get("HEAD_NODE_EC2_INSTANCE_ID")]
        )

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                private_dns_name = instance.get("PrivateIpAddress", "Not available")
                return private_dns_name
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while retrieving private DNS: {e}")
        return "Not available"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Not available"


def generate_random_id():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(4))


def get_configuration_files_path():
    try:
        root_folder = os.path.abspath(__file__ + "/../..")
        configuration_files = os.path.abspath(root_folder + "/" + "configuration_files")
        return configuration_files
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def build_configuration_file_path(file_name):
    try:
        configuration_files_path = get_configuration_files_path() + "/" + file_name
        return configuration_files_path
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_report_files_path():
    try:
        root_folder = os.path.abspath(__file__ + "/../..")
        configuration_files = os.path.abspath(root_folder + "/" + "test")
        return configuration_files
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def build_report_file_path(file_name):
    try:
        configuration_files_path = get_report_files_path() + "/" + file_name
        return configuration_files_path
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None        


def get_current_timestamp():
    ct = datetime.datetime.now()

    return ct
    
    
def scan_logs_for_pattern(log_file_path):
    ERROR_PATTERNS = [
    "Unexpected number of domU domains",
    "fail to migrate sandbox"
    ]
    WARNING_PATTERNS = [
        "Unable to send metrics packet"
    ]
    try:
        with open(log_file_path, "r") as log_file:
            log_line = log_file.readline()
            for error_pattern in ERROR_PATTERNS:
                if error_pattern in log_line:
                    return log_line

            # for warning_pattern in WARNING_PATTERNS:
            #     if warning_pattern in logs:
            #         print(f"Warning found: {warning_pattern}")
            #         return log_file.line()
        return False
    except FileNotFoundError:
        print(f"Log file {log_file_path} not found.")
        return False    
    

def update_ui_configs():
    try:
        head_node_ip = get_private_ip()
        api_url = f"http://{head_node_ip}:5000/v1/profile/az1"
        headers = {"Accept": "application/json"}
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        assert response_data["ProfileName"] == "az1"

        with open(build_configuration_file_path("rest-api-payloads/test_file.json"), "w") as f:
            json.dump(response_data, f)

    except (AssertionError, TypeError, AttributeError, FileNotFoundError) as e:
        assert False, f"An error occurred: {str(e)}"


def read_data_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
