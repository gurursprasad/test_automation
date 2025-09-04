from page_objects.frames_objects import FramesObjects
from page_objects.home_page_objects import HomePageObjects
from utils.base_class import BaseClass
from page_objects.challenging_dom_objects import ChallengingDOMObjects

class Test_Frames(BaseClass):
    def test_frames_is_loaded(self, setup_driver):
        home_page_objects = HomePageObjects(self.driver)
        home_page_objects.click_frames()
        assert "/frames" in self.driver.current_url


    def test_nested_frames_is_loaded(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_nested_frames()
        assert "/nested_frames" in self.driver.current_url


    def test_i_frames_is_loaded(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        self.driver.back()
        assert "/frames" in self.driver.current_url
        frames_objects.click_i_frames()
        assert "/iframe" in self.driver.current_url
        self.driver.back()


    def test_nested_frames(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_nested_frames()
        assert "/nested_frames" in self.driver.current_url
        frames_objects.switch_to_frame("frame-top")
        frames_objects.validate_frameset()
        # frames_objects.switch_to_default_content()
        self.driver.back()


    def test_i_frames(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_i_frames()
        assert "/iframe" in self.driver.current_url
        frames_objects.switch_to_frame("mce_0_ifr")
        editor = self.driver.find_element("id", "tinymce")
        editor.clear()
        editor.send_keys("This is a test message")
        assert editor.text == "This is a test message"
        frames_objects.switch_to_default_content()