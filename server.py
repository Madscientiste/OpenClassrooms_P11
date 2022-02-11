import pathlib
from flask import Flask, render_template, request, redirect, flash, url_for

from app.exceptions import ClientError
from app.data import clubs, competitions


def create_app(config=None):
    app = Flask(__name__, template_folder="app/templates", instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="ayaya")

    if not config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(config)

    # making sure the folder exist
    # pathlib.Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    @app.errorhandler(ClientError)
    def handle_exception(e):
        # By default the "description" attribute is used for the error argument in the template.
        # if an argument "error" is present in the template_kwargs, it overrides the default.
        kwargs = {"error": e.description, **e.template_kwargs}
        return render_template(e.template, **kwargs), e.code

    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/summary", methods=["POST"])
    def summary():
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/confirm_booking", methods=["POST"])
    def confirm_booking():
        competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        seatsRequired = int(request.form["seats"])
        competition["seats_available"] = int(competition["seats_available"]) - seatsRequired
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
