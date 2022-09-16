import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import EMAIL_OK, refresh_datafiles


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerDisplayClubClass:

    def setup_method(self):
        refresh_datafiles()

    @pytest.mark.nondestructive
    def test_display_club_with_competitions(self, live_server, selenium):
        selenium.get("http://localhost:5002")
        assert "GUDLFT Registration" in selenium.title

        email_input = selenium.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(EMAIL_OK)
        email_input.send_keys(Keys.RETURN)

        selenium.get("http://localhost:5002/display_clubs")
        assert "Clubs| GUDLFT" in selenium.title
