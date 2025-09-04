import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="class")
def setup_driver(request):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://the-internet.herokuapp.com/")
    driver.maximize_window()
    
    request.cls.driver = driver
    yield driver
    driver.quit()