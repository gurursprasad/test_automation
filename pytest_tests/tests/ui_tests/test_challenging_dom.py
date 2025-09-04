from page_objects.home_page_objects import HomePageObjects
from utils.base_class import BaseClass
from page_objects.challenging_dom_objects import ChallengingDOMObjects

class Test_ChallengingDOM(BaseClass):
    def test_challenging_dom_is_loaded(self, setup_driver):
        home_page_objects = HomePageObjects(self.driver)
        home_page_objects.click_challenging_dom()
        url = self.driver.current_url
        assert "/challenging_dom" in url

    
    def test_click_edit_for_any_element(self):
        challenging_dom_objects = ChallengingDOMObjects(self.driver)
        challenging_dom_objects.find_dynamic_table_element("Adipisci3")
        url = self.driver.current_url
        assert "#edit" in url
