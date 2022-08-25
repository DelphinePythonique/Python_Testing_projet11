import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import (
    EMAIL_OK,
    EMAIL_KO,
    refresh_datafiles,
    COMPETITION_OK,
    CLUB_OK,
    QUANTITY_PLACES_OK,
    QUANTITY_PLACES_SUP_AVAILABLE,
    QUANTITY_POINTS_SUP_AVAILABLE,
)


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerDisplayClubClass:
    def setup_method(self):
        refresh_datafiles()

    @pytest.mark.nondestructive
    def test_should_display_book_form_and_book(self, live_server, selenium):
        selenium.get(f"http://localhost:5002/book/{COMPETITION_OK}/{CLUB_OK}")
        assert "Booking for competition test1 || GUDLFT" in selenium.title

        email_input = selenium.find_element(By.NAME, "places")
        email_input.clear()
        email_input.send_keys(QUANTITY_PLACES_OK)
        email_input.send_keys(Keys.RETURN)
        assert "Great-booking complete!" in selenium.find_element(By.TAG_NAME, "li").text

    @pytest.mark.nondestructive
    def test_should_display_book_form_and_not_book(self, live_server, selenium):
        selenium.get(f"http://localhost:5002/book/{COMPETITION_OK}/{CLUB_OK}")
        assert "Booking for competition test1 || GUDLFT" in selenium.title

        email_input = selenium.find_element(By.NAME, "places")
        email_input.clear()
        email_input.send_keys(QUANTITY_POINTS_SUP_AVAILABLE)
        email_input.send_keys(Keys.RETURN)
        assert "enter less places!" in selenium.find_element(By.TAG_NAME, "li").text




