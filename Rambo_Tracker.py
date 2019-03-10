import requests
import json
from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

app = Flask(__name__)


# defining routes which include the home page, search page, and n6status page

@app.route('/')
def home():
    form = SearchForm(request.form)
    return render_template('pages/home.html', form=form)


@app.route('/search', methods=['POST'])
def search():
    name = request.form['steamname']
    players_location = players_server(name)
    return render_template('forms/search.html',players_location=players_location)


@app.route('/n6status', methods=['GET'])
def n6status():
    return render_template('pages/n6status.html')


def get_server_by_id(serverid):
    response = requests.get("https://atlas.hgn.hu/api/server/" + str(serverid) + "/players")
    response_text = response.text
    processed_data = json.loads(response_text)
    return processed_data


def players_server(steamname):
    server_1_response = get_server_by_id(410)
    server_2_response = get_server_by_id(411)
    server_3_response = get_server_by_id(412)
    server_4_response = get_server_by_id(425)
    server_5_response = get_server_by_id(426)
    server_6_response = get_server_by_id(427)
    server_7_response = get_server_by_id(440)
    server_8_response = get_server_by_id(441)
    server_9_response = get_server_by_id(442)
    am_i_online_1 = am_i_online(steamname, server_1_response)
    if am_i_online_1:
        return "M5"
    am_i_online_2 = am_i_online(steamname, server_2_response)
    if am_i_online_2:
        return "M6"
    am_i_online_3 = am_i_online(steamname, server_3_response)
    if am_i_online_3:
        return "M7"
    am_i_online_4 = am_i_online(steamname, server_4_response)
    if am_i_online_4:
        return "N5"
    am_i_online_5 = am_i_online(steamname, server_5_response)
    if am_i_online_5:
        return "N6"
    am_i_online_6 = am_i_online(steamname, server_6_response)
    if am_i_online_6:
        return "N7"
    am_i_online_7 = am_i_online(steamname, server_7_response)
    if am_i_online_7:
        return "O5"
    am_i_online_8 = am_i_online(steamname, server_8_response)
    if am_i_online_8:
        return "O6"
    am_i_online_9 = am_i_online(steamname, server_9_response)
    if am_i_online_9:
        return "O7"
    return "Player is either not in region or offline."


def am_i_online(steamname, server_response):
    return_value = False
    for player in server_response:
        if isinstance(player, dict):
            player_name = player.get("name")
            if steamname == player_name:
                return_value = True
    return return_value


def print_response_data(response):
    response_text = response.text
    processed_data = json.loads(response_text)
    print("Processed data: ")
    print(processed_data)

    if isinstance(processed_data, list):
        for player_entry in processed_data:
            print(player_entry)

    if isinstance(processed_data, dict):
        for key, value in processed_data.items():
            print(key, " - ", value)


class SearchForm(Form):
    steamname = TextField('Search a Steam ID', [DataRequired()])


class ServerInfo:
    """ This function takes any number of arguments and retrieves server info for the server IDs specified """

    def print_server_info(*argv):
        for arg in argv:
            response = requests.get("https://atlas.hgn.hu/api/server/" + str(arg))
            print_response_data(response)


class PlayerInfo:
    """ This function takes data from the Atlas API and sorts it in a list by playtime (descending) for all players in
    all 9 regions"""

    def print_player_info(*argv):
        for arg in argv:
            response = requests.get("https://atlas.hgn.hu/api/server/" + str(arg) + "/players")
            print_response_data(response)


app.secret_key = 'asssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'

# ServerInfo.print_server_info(410, 411, 412, 425, 426, 427, 440, 441, 442)
# PlayerInfo.print_player_info(410, 411, 412, 425, 426, 427, 440, 441, 442)

app.run()
