from flask import Flask, jsonify, request
from ..teambuilder.teambuilder_classes import Team, Pokemon
from ..teambuilder.teambuilder import load_teamdata

app = Flask(__name__)


@app.route("/")
def hello_world():
    data, dex = load_teamdata()
    new_team = Team(roster=data)
    return jsonify(new_team.roster[0].toJSON())


@app.route("/last_played")
def last_played():
    match_data = None
    return match_data


@app.route("/about")
def about_page():
    return 'Hello, About!'


@app.route("/contact")
def contact_page():
    return 'Hello, Contact!'


@app.route('/teambuilder')
def teambuilder():
    return 'Hello, Teambuilder!'


@app.route('/teambuilder')
def laboratory():
    return 'Hello, Laboratory!'


@app.route('/match_history')
def match_history():
    return 'Hello, Match History!'


@app.route('/calculator')
def calculator():
    return 'Hello, Calculator!'
