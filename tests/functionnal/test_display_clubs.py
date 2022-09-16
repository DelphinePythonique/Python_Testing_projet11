import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import EMAIL_OK, EMAIL_KO, refresh_datafiles


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerDisplayClubClass:

    def setup_method(self):
        refresh_datafiles()

    @pytest.mark.nondestructive
    def test_show_summary_with_known_email(self, live_server, selenium):
        selenium.get("http://localhost:5002")
        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_OK)
        email_input.send_keys(Keys.RETURN)
        link_to_showSummary = selenium.find_element(By.XPATH, "//a[@href='/showSummary']")
        link_to_showSummary.click()
        assert "Summary | GUDLFT Registration" in selenium.title
        assert (
                "Competitions:"
                in selenium.find_element(By.TAG_NAME, "H3").text
        )



    def test_book_and_click_on_link(self, live_server, selenium):
        selenium.get("http://localhost:5002")
        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_OK)
        email_input.send_keys(Keys.RETURN)
        link_to_showSummary = selenium.find_element(By.XPATH, "//a[@href='/showSummary']")
        link_to_showSummary.click()


        link_to_book = selenium.find_element(By.ID, "competition test2")
        link_to_book.click()
        assert "Booking for competition test2 || GUDLFT" in selenium.title
