import json
import os.path

from flask import Flask, render_template, request, redirect, flash, url_for

MAX_PLACE_PER_BOOKING = 12

app = Flask(__name__)
app.secret_key = "something_special"

def init_booking():
    bookings = {'bookings': []}
    with open('bookings.json', 'w') as f:
        json.dump(bookings, f)


def save_booking(club, competition, booked_places):
    if not os.path.isfile("bookings.json"):
        init_booking()
    competitions = loadCompetitions()
    for c in competitions:
        if c['name'] == competition['name']:
            c.update({'numberOfPlaces': str(int(c['numberOfPlaces']) - int(booked_places))})
    competitions_to_write = {"competitions": competitions}
    with open('competitions.json', 'w') as f:
        json.dump(competitions_to_write, f, indent=4)
    bookings = load_bookings()
    bookings.append({'club':club['name'], 'competition': competition['name'], 'booked_places': booked_places})
    bookings_to_write = {"bookings": bookings}
    with open('bookings.json', 'w') as f:
        json.dump(bookings_to_write, f, indent=4)

def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions

def load_bookings():

    with open("bookings.json") as booking:
        list_of_booking = json.load(booking)["bookings"]
        return list_of_booking

def max_place_for_booking(competition, club):
    try:
        return min(MAX_PLACE_PER_BOOKING, int(competition['numberOfPlaces']), int(club['points']))
    except TypeError:
        return 0

def clubs_with_email(clubs, email):

    return [club for club in clubs if club["email"] == email]


def extract_first_club_with_name(clubs, name):
    found_clubs = [c for c in clubs if c["name"] == name]
    if len(found_clubs) == 0:
        return False
    else:
        return found_clubs[0]


def extract_first_competition_with_name(competitions, name):
    found_competitions = [c for c in competitions if c["name"] == name]
    if len(found_competitions) == 0:
        return False
    else:
        return found_competitions[0]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    clubs = loadClubs()
    competitions = loadCompetitions()

    clubs_selected = clubs_with_email(clubs, request.form["email"])
    if len(clubs_selected) > 0:
        club = clubs_selected[0]
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("email not existing")
        return redirect(url_for("index"))


@app.errorhandler(404)
@app.route("/book/<competition>/<club>")
def book(competition, club):
    clubs = loadClubs()
    competitions = loadCompetitions()

    found_club = extract_first_club_with_name(clubs, club)
    if not found_club:
        flash("club not found")
        return render_template("404.html"), 404

    found_competition = extract_first_competition_with_name(competitions, competition)
    if not found_competition:
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
    clubs = loadClubs()
    competitions = loadCompetitions()

    found_club = extract_first_club_with_name(clubs, request.form["club"])
    if not found_club:
        flash("club not found")
        return render_template("404.html"), 404

    found_competition = extract_first_competition_with_name(
        competitions, request.form["competition"]
    )
    if not found_competition :
        flash("competition not found")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            404,
        )

    if found_club and found_competition:
        places_required = int(request.form["places"])
        if places_required > max_place_for_booking(found_competition,found_club):
            flash("enter less places!")
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )

        else:
            save_booking(found_club,found_competition, places_required)
            flash("Great-booking complete!")
            return render_template(
                "welcome.html", club=found_club, competitions=competitions
            )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


