import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for, session

from utils import DataManager, ClubCompetition

MAX_PLACE_PER_BOOKING = 12

app = Flask(__name__)
if os.environ["FLASK_ENV"] == "development":
    app.config.from_pyfile("./settings/dev.cfg")
elif os.environ["FLASK_ENV"] == "testing":
    app.config.from_pyfile("./settings/test.cfg")
else:
    app.config.from_pyfile("./settings/prod.cfg")


@app.template_filter("is_in_the_past")
def is_in_the_past(date_to_check):
    if isinstance(date_to_check, str):
        try:
            date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return True
    if date_to_check < datetime.now():
        return True
    return False


def save_competition_table(competition, booked_places):
    data_manager = DataManager(app)
    competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    for c in competitions:
        if c["name"] == competition["name"]:
            c.update({"numberOfPlaces": str(int(c["numberOfPlaces"]) - booked_places)})
    data_manager.tables[data_manager.TableName.COMPETITIONS].save(competitions)


def save_club_table(club, booked_places):
    data_manager = DataManager(app)
    clubs = data_manager.tables[data_manager.TableName.CLUBS].all()
    for c in clubs:
        if c["name"] == club["name"]:
            c.update({"points": str(int(c["points"]) - int(booked_places))})
    data_manager.tables[data_manager.TableName.CLUBS].save(clubs)


def save_booking_table(club_name, competition_name, booked_places):
    data_manager = DataManager(app)
    bookings = data_manager.tables[data_manager.TableName.BOOKINGS].all()
    bookings.append(
        {
            "club": club_name,
            "competition": competition_name,
            "booked_places": booked_places,
        }
    )
    data_manager.tables[data_manager.TableName.BOOKINGS].save(bookings)


def save_booking(club, competition, booked_places):
    data_manager = DataManager(app)
    club_competitions = ClubCompetition(
        data_manager
    )
    booking_is_allowed_, message = booking_is_allowed(
        booked_places,
        int(competition["numberOfPlaces"]),
        int(club["points"]),
        club_competitions.total_booked_places_per_competition_and_club(club['name'], competition['name']),
        competition['date']
    )

    if not booking_is_allowed_:
        return False, message

    save_competition_table(competition, booked_places)
    save_club_table(club, booked_places)
    save_booking_table(club["name"], competition["name"], booked_places)

    return True, "Great-booking complete!"


def booking_is_allowed(
        places_required: int,
        number_of_places: int,
        club_points: int,
        total_booked_places: int,
        competition_date: str
):
    if places_required <= 0:
        return False, "booking must be superior to 0"
    if places_required > max_place_for_booking(
            number_of_places, club_points, total_booked_places
    ):
        return False, "enter less places!"
    if is_in_the_past(competition_date):
        return False, "too late the competition is over"
    else:
        return True, "booking must be save"


def max_place_for_booking(
        number_of_places_competition, points_club, total_booked_places
):
    try:

        return min(
            MAX_PLACE_PER_BOOKING - total_booked_places,
            number_of_places_competition,
            points_club,
        )
    except TypeError:
        return 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"]
    data_manager = DataManager(app)
    competitions_ = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    club_selected = data_manager.tables[
        data_manager.TableName.CLUBS
    ].filter_first_element({"email": email})

    if club_selected:
        session['username'] = email
        return render_template(
            "welcome.html", club=club_selected, competitions=competitions_
        )
    else:
        flash("email not existing")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    data_manager = DataManager(app)
    found_club = data_manager.tables[data_manager.TableName.CLUBS].filter_first_element(
        {"name": club}
    )
    if not found_club:
        flash("club not found")
        return render_template("404.html"), 404

    found_competition = data_manager.tables[
        data_manager.TableName.COMPETITIONS
    ].filter_first_element({"name": competition})
    if not found_competition:
        competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()

        flash("competition not found")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            404,
        )
    if is_in_the_past(found_competition['date']):
        competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()

        flash("too late the competition is over")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            404,
        )
    return render_template(
        "booking.html", club=found_club, competition=found_competition
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    data_manager = DataManager(app)
    competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    found_club = data_manager.tables[data_manager.TableName.CLUBS].filter_first_element(
        {"name": request.form["club"]}
    )
    if not found_club:
        flash("club not found")
        return render_template("404.html"), 404

    found_competition = data_manager.tables[
        data_manager.TableName.COMPETITIONS
    ].filter_first_element({"name": request.form["competition"]})

    if not found_competition:
        flash("competition not found")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            404,
        )

    places_required = int(request.form["places"])
    is_saved, message = save_booking(found_club, found_competition, places_required)
    flash(message)
    if is_saved:
        found_club = data_manager.tables[data_manager.TableName.CLUBS].filter_first_element(
            {"name": request.form["club"]}
        )

        competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
        return render_template(
            "welcome.html", club=found_club, competitions=competitions
        )

    else:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )


@app.route("/display_clubs")
def display_club():
    data_manager = DataManager(app)
    if "username" not in session:
        return redirect(url_for("index"))
    clubs = data_manager.tables[data_manager.TableName.CLUBS].all()
    bookings = ClubCompetition(data_manager)
    for club in clubs:
        club['competitions'] = bookings.total_booked_places_per_club_all_competitions(club['name'])
    return render_template(
        "display_club.html", clubs=clubs
    )


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
