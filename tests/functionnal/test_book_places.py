import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.conftest import (
    refresh_datafiles,
    CLUB_OK,
    QUANTITY_PLACES_OK,
    QUANTITY_POINTS_SUP_AVAILABLE,
    COMPETITION2_OK,
)


@pytest.mark.usefixtures("live_server")
class TestFunctionnalServerDisplayClubClass:
    def setup_method(self):
        refresh_datafiles()

    @pytest.mark.nondestructive
    def test_book(self, live_server, selenium):
        selenium.get(f"http://localhost:5002/book/{COMPETITION2_OK}/{CLUB_OK}")
        assert "Booking for competition test2 || GUDLFT" in selenium.title

        email_input = selenium.find_element(By.NAME, "places")
        email_input.clear()
        email_input.send_keys(QUANTITY_PLACES_OK)
        email_input.send_keys(Keys.RETURN)
        assert (
            "Great-booking complete!" in selenium.find_element(By.TAG_NAME, "li").text
        )

    @pytest.mark.nondestructive
    def test_book_to_many_places(self, live_server, selenium):
        selenium.get(f"http://localhost:5002/book/{COMPETITION2_OK}/{CLUB_OK}")
        assert "Booking for competition test2 || GUDLFT" in selenium.title

        email_input = selenium.find_element(By.NAME, "places")
        email_input.clear()
        email_input.send_keys(QUANTITY_POINTS_SUP_AVAILABLE)
        email_input.send_keys(Keys.RETURN)
        assert "enter less places!" in selenium.find_element(By.TAG_NAME, "li").text

    @pytest.mark.nondestructive
    def test_book_zero_place(self, live_server, selenium):
        selenium.get(f"http://localhost:5002/book/{COMPETITION2_OK}/{CLUB_OK}")
        assert "Booking for competition test2 || GUDLFT" in selenium.title

        email_input = selenium.find_element(By.NAME, "places")
        email_input.clear()
        email_input.send_keys(0)
        email_input.send_keys(Keys.RETURN)
        assert (
            "booking must be superior to 0"
            in selenium.find_element(By.TAG_NAME, "li").text
        )
