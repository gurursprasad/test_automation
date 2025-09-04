import subprocess
import time
import os
import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.common_utils import *
from configuration_files.ui_configs import *
from page_objects.common_objects import *
from page_objects.landing_page import *
from page_objects.profiles_page import *
from page_objects.login_page import *


def pytest_configure(config):
    setup_env = config.getoption("--setup_env")
    setup_browser = config.getoption("--browser")
    if setup_env == "true":
        get_profile_data()
        driver = driver_instance_object(setup_browser)
        # setup_profiles(driver)
    elif setup_env == "false":
        print("Proceeding without setup")


def driver_instance_object(browser):
    if browser == "firefox":
        # logger.info("Starting firefox browser setup")
        options = webdriver.FirefoxOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "chrome":
        # logger.info("Starting chrome browser setup")
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "edge":
        # logger.info("Starting edge browser setup")
        options = webdriver.EdgeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    # logger.info("Starting test on " + browser + " browser")
    driver.get("https://" + get_public_ip())
    driver.maximize_window()
    driver.implicitly_wait(10)
    enter_email(driver)
    # logger.info("Entered user email")
    click_next(driver)
    # logger.info("Clicked on next button")
    enter_password(driver)
    # logger.info("Entered user password")
    time.sleep(1)
    click_sign_in(driver)
    # logger.info("Clicked on sign in button")
    if "execution=UPDATE_PASSWORD" in driver.current_url:
        enter_new_password(driver)
        # logger.info("Entered new password")
        enter_confirm_password(driver)
        # logger.info("Entered confirm password")
        click_submit(driver)
        # logger.info("Clicked on submit button")
        driver.implicitly_wait(10)
    assert "https://" + get_public_ip() + "/dashboard" in driver.current_url
    # logger.info("Logged in successfully!!!")
    return driver


def get_profile_data():
    private_ip = get_private_ip()
    api_url = f"http://{private_ip}:5000/v1/profile/az1"
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    print(response_data["Controller"]["IamInstanceProfile"])
    print(response_data["Controller"]["ImageId"])
    print(response_data["Controller"]["SubnetId"])
    print(response_data["Worker"]["IamInstanceProfile"])
    print(response_data["Worker"]["ImageId"])
    print(response_data["Worker"]["SubnetId"])
    print(response_data["XspotVersion"])


# def setup_profiles(driver_instance):
#     click_profiles(driver_instance)
#     print("Clicked on Profiles!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     assert "/dashboard/profiles" in driver_instance.current_url
#     # logger.info("Profiles page is loaded")
#     click_add_profile(driver_instance)
#     # logger.info("Clicked on Add Profile")
#     enter_profile_information(driver_instance, profiles_config["profile_name"], profiles_config["profile_description"])
#     # logger.info("Entering profile information: Profile Name, Profile Description")
#     select_region(driver_instance, profiles_config["region"])
#     # logger.info("Selecting Region")
#     select_az(driver_instance, profiles_config["az"])
#     # logger.info("Selecting Availability Zone")
#     enter_log_path(driver_instance, profiles_config["log_path"])
#     # logger.info("Entering Log Path")
#     enter_node_group_name(driver_instance, profiles_config["node_group_name"])
#     # logger.info("Entering Node Group Name")
#     enter_max_controllers(driver_instance, profiles_config["max_controllers"])
#     # logger.info("Entering Max Controllers")
#     click_next_button(driver_instance)
#     # logger.info("Clicked on Next Button")
#     enter_controller_information(driver_instance, 
#                                  profiles_config["controller"]["iam"], 
#                                  profiles_config["controller"]["image_id"], 
#                                  profiles_config["controller"]["subnet_id"], 
#                                  profiles_config["controller"]["sg"], 
#                                  profiles_config["controller"]["instance_type"], 
#                                  profiles_config["controller"]["volume_size"],
#                                  profiles_config["controller"]["instance_tags"])
#     # logger.info("Entering Controller Information: IAM Instance Profile, Image ID, Subnet ID, Security Group, Instance Type, Volume Size, Instance Tags")
#     click_next_button(driver_instance)
#     # logger.info("Clicked on Next Button")
#     enter_worker_information(driver_instance, 
#                              profiles_config["worker"]["iam"], 
#                              profiles_config["worker"]["image_id"], 
#                              profiles_config["worker"]["subnet_id"], 
#                              profiles_config["worker"]["sg"], 
#                              profiles_config["worker"]["instance_type"], 
#                              profiles_config["worker"]["spot_fleet_type"], 
#                              profiles_config["worker"]["instance_tags"])
#     # logger.info("Entering Worker Information: IAM Instance Profile, Image ID, Subnet ID, Security Group, Instance Type, Spot Fleet Type, Instance Tags")
#     click_next_button(driver_instance)
#     # logger.info("Clicked on Next Button")
#     # enter_xspot_version(driver_instance, profiles_config["xspot"]["version"])
#     # logger.info("Entering Xspot Version")
#     click_submit_button(driver_instance)
#     # logger.info("Clicked on Submit Button")
#     time.sleep(3)
#     # click_ballooning_checkbox(driver_instance)
#     # click_hyperthreading_checkbox(driver_instance)
#     assert wait_for_success_message(driver_instance) # logger.info("Profile is not created")
#     # logger.info("Success message is displayed. Profile is created")
#     click_profiles(driver_instance)
#     # logger.info("Clicked on Profiles")
#     time.sleep(2)
#     added_list = check_item_in_grid(driver_instance, profiles_config["profile_name"])
#     # logger.info("Checking if profiles list is updated after addition")
#     assert profiles_config["profile_name"] in added_list
#     # logger.info("Profile is created")





# def setup_xio_environment(driver_instance, logger):
#     click_application_environment(driver_instance)
#     logger.info("Clicked on Application Environment")
#     assert "/dashboard/environments" in driver_instance.current_url
    # logger.info("Environments page is loaded")
    # click_add_environment(driver_instance)
    # logger.info("Clicked on Add Environment")
    # select_environment_type(driver_instance, environment_config["environment_type"])
    # logger.info("Selected Environment Type")
    # click_next_button(driver_instance)
    # logger.info("Clicked on Next Button")
    # enter_environment_name(driver_instance, environment_config["environment_name"])
    # logger.info("Entered Environment Name")
    # # enter_cluster_name(driver_instance, environment_config["cluster_name"])
    # click_next_button(driver_instance)
    # logger.info("Clicked on Next Button")
    # enter_pool_name(driver_instance, environment_config["pool_name"], 0)
    # logger.info("Entered Pool Name")
    # enter_pool_size(driver_instance, environment_config["pool_size"], 0)
    # logger.info("Entered Pool Size")
    # enter_profile_name(driver_instance, environment_config["profile_name"], 0)
    # logger.info("Entered Profile Name")
    # enter_image_name(driver_instance, environment_config["image_name"], 0)
    # logger.info("Entered Image Name")
    # enter_cpus(driver_instance, environment_config["cpus"], 0)
    # logger.info("Entered Cpus")
    # enter_min_memory(driver_instance, environment_config["min_memory"], 0)
    # logger.info("Entered Min Memory")
    # enter_max_memory(driver_instance, environment_config["max_memory"], 0)
    # logger.info("Entered Max Memory")
    # enter_volume_size(driver_instance, environment_config["volume_size"], 0)
    # logger.info("Entered Volume Size")
    # enter_prefix_count(driver_instance, environment_config["prefix_count"], 0)
    # logger.info("Entered Prefix Count")
    # click_submit_button(driver_instance)
    # logger.info("Clicked on Submit Button")
    # assert "Submission Successful!" in get_submission_status(driver_instance)
    # logger.info("Environment is created")
    # click_close_button(driver_instance)
    # logger.info("Clicked on Close Button")
    # time.sleep(2)
    # click_application_environment(driver_instance)
    # logger.info("Clicked on Application Environment")
    # envs_list = check_environment_is_created(driver_instance)
    # logger.info("Checking Environment is created")
    # assert environment_config["environment_name"] in envs_list
    # logger.info("Environment is created")


def setup_karpenter():
    karpenter_install_command = f"helm upgrade --install karpenter oci://public.ecr.aws/x5d4i9x1/exostellar-karpenter/karpenter \
   --version v1.0.0 \
   --namespace karpenter \
   --create-namespace \
   --set 'settings.clusterName={os.environ.get('CLUSTER_NAME')}' \
   --set controller.resources.requests.cpu=1 \
   --set controller.resources.requests.memory=1Gi \
   --set controller.resources.limits.cpu=1 \
   --set controller.resources.limits.memory=1Gi \
   --set headnode=http://{get_private_ip()}:5000 \
   --set environmentName={environment_config['setup_env_name']} \
   --wait"
    
    print(karpenter_install_command)
    
    # subprocess.run(karpenter_install_command, shell=True, check=True)
