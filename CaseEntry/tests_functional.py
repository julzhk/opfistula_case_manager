from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# class NewCaseTest(unittest.TestCase):
class NewCaseTest(object):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_form_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('opfistula', self.browser.title.lower())
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Case', header_text)

        inputbox = self.browser.find_element_by_class_name('patient')
        self.assertEqual(
            inputbox.get_attribute('patient'),
            'Patient Name'
        )
        inputbox.send_keys('Selenium Patient')
        inputbox.send_keys(Keys.ENTER)