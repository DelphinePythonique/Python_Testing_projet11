import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import EMAIL_OK, EMAIL_KO, refresh_datafiles


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerLoginClass:

    def setup_method(self):
        refresh_datafiles()

    @pytest.mark.nondestructive
    def test_login_with_known_email(self, live_server, selenium):
        selenium.get("http://localhost:5002")
        assert "GUDLFT Registration" in selenium.title

        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_OK)
        email_input.send_keys(Keys.RETURN)
        assert "GUDLFT Registration" in selenium.title
        assert (
            "congratulation you are connected"
            in selenium.find_element(By.TAG_NAME, "li").text
        )


    @pytest.mark.nondestructive
    def testlogin_with_unknown_email(
        self, live_server, selenium
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


































































