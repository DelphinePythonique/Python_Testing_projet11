import json
import os.path

from flask import Flask, render_template, request, redirect, flash, url_for

from utils import DataManager

MAX_PLACE_PER_BOOKING = 12

app = Flask(__name__)
if os.environ["FLASK_ENV"] == "development":
    app.config.from_pyfile("./settings/dev.cfg")
elif os.environ["FLASK_ENV"] == "testing":
    app.config.from_pyfile("./settings/test.cfg")
else:
    app.config.from_pyfile("./settings/prod.cfg")


def save_booking(club, competition, booked_places):
    data_manager = DataManager(app)

    competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    for c in competitions:
        if c["name"] == competition["name"]:
            c.update(
                {"numberOfPlaces": str(int(c["numberOfPlaces"]) - int(booked_places))}
            )
    data_manager.tables[data_manager.TableName.COMPETITIONS].save(competitions)

    clubs = data_manager.tables[data_manager.TableName.CLUBS].all()
    for c in clubs:
        if c["name"] == club["name"]:
            c.update({"points": str(int(c["points"]) - int(booked_places))})
    data_manager.tables[data_manager.TableName.COMPETITIONS].save(competitions)

    bookings = data_manager.tables[data_manager.TableName.BOOKINGS].all()
    bookings.append(
        {
            "club": club["name"],
            "competition": competition["name"],
            "booked_places": booked_places,
        }
    )

    data_manager.tables[data_manager.TableName.BOOKINGS].save(bookings)


def max_place_for_booking(competition, club):
    try:
        data_manager = DataManager(app)
        places_already_booked = data_manager.tables[
            data_manager.TableName.CLUBS
        ].filter({"club": club, "competition": competition})

        return min(
            MAX_PLACE_PER_BOOKING - places_already_booked,
            int(competition["numberOfPlaces"]),
            int(club["points"]),
        )
    except TypeError:
        return 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    data_manager = DataManager(app)
    competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    club_selected = data_manager.tables[
        data_manager.TableName.CLUBS
    ].filter_first_element({"email": request.form["email"]})

    if club_selected:
        return render_template(
            "welcome.html", club=club_selected, competitions=competitions
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

    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    data_manager = DataManager(app)
    competitions = data_manager.tables[data_manager.TableName.COMPETITIONS].all()
    found_club = data_manager.tables[data_manager.TableName.CLUBS].filter_first_element(
        {"name", request.form["club"]}
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

    if found_club and found_competition:
        places_required = int(request.form["places"])
        if places_required > max_place_for_booking(found_competition, found_club):
            flash("enter less places!")
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )

        else:
            save_booking(found_club, found_competition, places_required)
            flash("Great-booking complete!")
            competitions = data_manager.tables[
                data_manager.TableName.COMPETITIONS
            ].all()
            return render_template(
                "welcome.html", club=found_club, competitions=competitions
            )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
