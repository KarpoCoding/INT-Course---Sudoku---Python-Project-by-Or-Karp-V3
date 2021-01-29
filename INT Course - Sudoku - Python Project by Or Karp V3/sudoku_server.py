from flask import Flask, session, request, jsonify
import sys
sys.path.append(r'DB_Folder')
from Sudoku_DataBase import *
# from Create_board_function_sent_by_Ethan import create_board
# create_board_OK.py file written by me
from create_board_OK import *
from minutes_counter import *
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "012345678945612345orororoasdysaysadysaysdaysadysadysadjynklsadyhlsadjyhuoasdhyuiosdayhouiasd"


# GET METHOD
@app.route("/logout")
def logout():
    # checks if the user is logged in before it logs him out
    if "logged_in" in session:
        # deleting the Name and logged_in dict elements
        session.pop("Name", None)
        session.pop('logged_in', None)
        return "True"
    else:
        return "False"


# GET METHOD
@app.route("/show_score_board")
def show_score_board():
    list = sudokuDB.show_scores_table()
    return jsonify(list)


# POST METHOD
@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        # gets the username and password from the user
        username, password = request.get_json()
        # translates the password into hash
        hash_password = make_hash_str(password)
        # adding the user and its hash into the Users DB if it doesn't already exist
        if sudokuDB.add_username(username, hash_password):
            return "True"
        else:
            return "False"


# POST METHOD
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # gets the username and password from the user
        username, password = request.get_json()
        # translates the password into hash
        hash_password = make_hash_str(password)
        # takes the given Username's DB hash
        user_db_password = sudokuDB.take_hash(username)

        # checks if the given password is correct
        if user_db_password == hash_password:
            session['logged_in'] = True
            session["Name"] = username
            return "True"
        else:
            return "False"


# POST METHOD
@app.route("/create_game_board", methods=["POST", "GET"])
def create_game_board():
    # checks if the user is logged in before creating a new game board
    if request.method == "POST" and session["logged_in"]:
        difficulty = request.get_json()
        return jsonify(board.make_board(difficulty))
    return "REQUEST FAILURE"


# POST METHOD
@app.route("/save_player_info", methods=["POST", "GET"])
def save_player_info():
    # saves info about the player who created the game board so it could check it later on when the player submits the game board
    if request.method == "POST" and session["logged_in"]:
        Name, Difficulty = request.get_json()
        session["start_time"] = current_hour_in_seconds()
        session["board_player_name"] = Name
        session["Difficulty"] = Difficulty
        return "SUCCESS"
    return "REQUEST FAILURE"


# POST METHOD
@app.route("/finished_game__board", methods=["POST", "GET"])
def finished_game__board():
    if request.method == "POST" and session["logged_in"]:
        game_board = request.get_json()
        if "Name" in session and "board_player_name" in session:
            if session["Name"] == session["board_player_name"]:
                validity = check_board_validity(game_board)

                if validity == "The Board is NOT full!!":
                    return validity
                elif validity == "Something went wrong":
                    return validity
                elif validity:
                    return "True"
                elif not validity:
                    return "False"
            else:
                return "NOT SAME USER"
        else:
            return "BOARD WAS NOT CREATED"

    return "REQUEST FAILURE"


# POST METHOD
@app.route("/add_score_to_score_board", methods=["POST", "GET"])
def add_score_to_score_board():
    if request.method == "POST" and session["logged_in"]:
        username = request.get_json()
        finish_time = current_hour_in_seconds()
        if session["Name"] == username:
            if "start_time" in session and "Difficulty" in session:
                sudokuDB.add_score(session["Name"], subtract_the_times_return_minutes(session["start_time"], finish_time), session["Difficulty"])
                # deleting the info from the sessions dict about the player who created the board because it has been submitted
                session.pop("start_time", None)
                session.pop("Difficulty", None)
                return "SUCCESS"
            else:
                return "BOARD ALREADY SUBMITTED"
        else:
            return "Something went wrong"

    return "REQUEST FAILURE"


def make_hash_str(string):
    # turning a string into a hash encoding
    return str(hashlib.sha1(string.encode()).hexdigest())


if __name__ == '__main__':
    # creating the DB Object
    sudokuDB = SudokuDB(r"DB_Folder/sudokuDB.db")
    sudokuDB.create_connection()
    sudokuDB.create_db_tables()

    # creating board object
    board = Board()

    # running the server
    app.run(debug=True)
