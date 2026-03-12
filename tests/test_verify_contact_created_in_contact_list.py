from time import sleep

import allure
import pytest

from config.environment import Environment
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.add_contact_page import AddContactPage
from pages.contact_details_page import ContactDetailsPage
from pages.contact_list_page import ContactListPage


@allure.feature("Contact")
@allure.story("Contact Creation")
class TestVerifyContact(BaseTest):


    @allure.title("Verifying successful creation of contact")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_successful_verify_contact(self):

        login_page = LoginPage(self.driver)
        add_contact_page_ = AddContactPage(self.driver)
        contact_details_page_ = ContactDetailsPage(self.driver)
        contact_list_page_ = ContactListPage(self.driver)
        env = Environment()
        base_url = env.get_base_url()
        email = env.get_email()
        password = env.get_password()


        with allure.step("Navigating to the login page"):
            login_page.navigate_to(base_url)
            assert login_page.login_page_visible(), "Login page did not load"

        with allure.step("Logging in to the application"):
            login_page.login(email, password)
            assert contact_list_page_.is_visible_contact_list(), "Contact list page did not load"

        with allure.step("Navigating to the add contact page"):
            contact_list_page_.click_add_new_contact()
            assert add_contact_page_.is_visible_add_contact(), "Add new contact page did not load"

        with allure.step("Fill the contact details"):
            add_contact_page_.fill_contact_form("Manjiri", "Deshpande", "1998-06-04", "manji@gmail.com", "1234567898", "Royal Castle", "Hinjawdi", "Pune", "Maharashtra", "411041", "India")
            assert contact_list_page_.is_visible_contact_list(), "Contact list page did not load"

        with allure.step("Verifying the contact created by clicking"):
            contact_list_page_.click_contact_link("Manji")
            assert contact_details_page_.is_visible_contact_details(), "Contact details page did not load"

        with allure.step("Verifying the contact created by checking the first name"):
            contact_details_page_.is_visible_firstname()


        with allure.step("Logging out of the application"):
            contact_details_page_.click_logout()
            assert login_page.login_page_visible(), "Login page did not load"
