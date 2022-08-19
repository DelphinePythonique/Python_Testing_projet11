import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import EMAIL_OK, EMAIL_KO


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerClass:
    @pytest.mark.nondestructive
    def test_should_display_summary(self, live_server, selenium):
        selenium.get("http://localhost:5002")
        assert "GUDLFT Registration" in selenium.title

        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_OK)
        email_input.send_keys(Keys.RETURN)
        assert "Summary | GUDLFT Registration" in selenium.title

    @pytest.mark.nondestructive
    def test_should_not_display_summary(
        self, live_server, selenium, clubs_fixture, mocker
    ):
        selenium.get("http://localhost:5002")
        assert "GUDLFT Registration" in selenium.title

        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_KO)
        email_input.send_keys(Keys.RETURN)
        assert "GUDLFT Registration" in selenium.title
        message_list = selenium.find_element(By.TAG_NAME, "li")
        assert message_list.text == "email not existing"