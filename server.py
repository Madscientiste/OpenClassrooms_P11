from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from dateutil.parser import parse


def create_app(config=None):
    app = Flask(__name__, template_folder="app/templates", instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="ayaya")

    if not config:
        app.config.from_pyfile("config.py", silent=True)
        from app.data import clubs, competitions
    else:
        app.config.update(config)
        clubs = config["clubs"]
        competitions = config["competitions"]

    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/summary", methods=["POST"])
    def summary():
        club = clubs.get_by("email", request.form["email"], first=True)

        if club:
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            return render_template("login.html", error="Email not found"), 401

    @app.route("/confirm_booking", methods=["POST"])
    def confirm_booking():
        competition = competitions.get_by("name", request.form["competition"], first=True)
        club = clubs.get_by("name", request.form["club"], first=True)

        competition_date = parse(competition["date"])
        requested_seats = int(request.form["seats"])
        seats_available = int(competition["seats_available"])

        if requested_seats > seats_available:
            flash("Sorry, we don't have enough seats available for that competition.")
        elif requested_seats > 12:
            flash("Sorry, we can only book up to 12 seats at a time.")
        elif competition_date < datetime.now():
            flash("Sorry, that competition has already passed.")
        else:
            competition["seats_available"] = seats_available - requested_seats
            flash("Great-booking complete!")

        return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/book/<competition>/<club>")
    def book_seats(competition, club):
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        if foundClub and foundCompetition:
            return render_template("booking.html", club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app
