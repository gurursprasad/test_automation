import os
import tempfile
import time

import boto3
import paramiko

from datetime import datetime
from kubernetes import client, config


def connect_to_ec2_machine():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ec2 = boto3.client(
            "ec2",
            region_name=os.environ.get("AWS_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        ssm_client = boto3.client("ssm")

        response = ec2.describe_instances(
            InstanceIds=[os.environ.get("HEAD_NODE_EC2_INSTANCE_ID")]
        )
        instance_dns = response["Reservations"][0]["Instances"][0]["PublicDnsName"]

        # Retrieve PEM key from Parameter Store
        pem_key_parameter_name = os.environ.get("AWS_PARAMETER_STORE_PEM_KEY_FILE")
        response = ssm_client.get_parameter(
            Name=pem_key_parameter_name, WithDecryption=True
        )
        pem_key_str = response["Parameter"]["Value"]

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_pem_file:
            temp_pem_file.write(pem_key_str.encode("utf-8"))
            temp_pem_file.close()

        private_key = paramiko.RSAKey.from_private_key_file(temp_pem_file.name)

        ssh.connect(
            instance_dns,
            username=os.environ.get("HEAD_NODE_EC2_USERNAME"),
            pkey=private_key,
        )
        return ssh
    except Exception as e:
        print(f"An error occurred during SSH connection: {e}")
        return None


def execute_ec2_commands(command):
    ssh = connect_to_ec2_machine()
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        ssh.close()
        
        if error:
            print(f"Error: {error}")
            return None
        
        return output
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")
        return None


def run_controller_commands(controller_ip, command):
    try:
        ssh = connect_to_ec2_machine()
        if ssh:
            try:
                response = execute_command(ssh, controller_ip, command)
                return response
            finally:
                ssh.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def execute_command(ssh, controller_ip, command):
    try:
        shell = ssh.invoke_shell()
        shell.send("sudo su -\n")
        time.sleep(1)
        shell.send(f"ssh {controller_ip}\n")
        time.sleep(1)
        shell.send(f"{command}\n")
        time.sleep(1)
        output = shell.recv(65535).decode("utf-8")
        shell.close()

        return output
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
