from random import randint
from users_logging_methods import *
from create_board_OK import check_how_many_is_filled
from minutes_counter import *
import sys
import requests
import json
import csv


class Game:
    def __init__(self):
        # creating a username variable
        self.username = None

        # creating the Client object
        self.client = Client()

        # TimeInMinutes score variables
        self.start_time = None
        self.finish_time = None
        self.TimeInMinutes = None

        # game_board_file path
        self.BOARD_PATH = "game_board.csv"

    def introduction(self):
        print("Hello and welcome to Or Karp's Sudoku Python Project!\n")
        return self.__main_menu_text()

    def __main_menu_text(self):
        print("Main Menu: \n")
        print("1) Play")
        print("2) Show ScoreBoard")
        print("3) Quit")
        return self.__main_menu_exec()

    def __main_menu_exec(self):
        user_answer = input_from_user()

        # 1) Play
        if user_answer in ["1", "play"]:
            return self.__sign_up_login_menu()

        # 2) Show ScoreBoard
        elif user_answer in ["2", "sb"]:
            return self.__show_score_board()

        # 3) Quit
        elif user_answer in ["3", "quit", "exit"]:
            exit_game()

        else:
            return self.__main_menu_exec()

    def __sign_up_login_menu(self):
        print("Before you begin playing some good ol' sudoku you first need to log into your account")
        print("1) login")
        print("2) sign up")
        print("3) main menu")

        user_answer = input_from_user()

        # 1) login
        if user_answer in ["1", "login"]:
            username, password = login()
            response_from_server = self.client.login(username, password)
            if response_from_server.content.decode() == "True":
                # the user is now logged in
                self.username = username
                print(f"You Logged in Successfully {self.username.capitalize()}!\n")
                return self.__logged_in_menu_text()

            elif response_from_server.content.decode() == "False":
                # invalid information was inserted
                print("Wrong Username or Password!!!\n")

            else:
                print("Something went wrong..")

            return self.__sign_up_login_menu()

        # 2) sign up
        elif user_answer in ["2", "signup"]:
            username, password = sign_up()
            response_from_server = self.client.sign_up(username, password)
            if response_from_server.content.decode() == "True":
                print(f"Your account was created successfully {username.capitalize()}!")
                print("Awesome! Transferring you back to the previous menu.\n")
            elif response_from_server.content.decode() == "False":
                print("This account already exists!!!\n")
            else:
                print("Something went wrong..")
            return self.__sign_up_login_menu()

        # 3) main menu
        elif user_answer == "3":
            return self.__main_menu_text()

        else:
            self.__sign_up_login_menu()

    def __logged_in_menu_text(self):
        if self.username:
            print(f"Status: {self.username.capitalize()} is online \n")
            print("1) Create a new sudoku board (the board will appear in the same folder)")
            print("2) Show ScoreBoard")
            print("3) Send your finished sudoku board")
            print("4) Logout")
            return self.__logged_in_menu_exec()

        print("USER NOT LOGGED IN!!")
        return self.__main_menu_text()

    def __logged_in_menu_exec(self):
        user_answer = input_from_user()

        # 1) Create a new sudoku board (the board will appear in the same folder) - choose difficulty
        if user_answer == "1":
            return self.__choose_difficulty()

        # 2) Show ScoreBoard
        elif user_answer in ["2", "sb"]:
            return self.__show_score_board()

        # 3) Send your finished sudoku board - sending the completed board to the server
        elif user_answer == "3":
            return self.__send_completed_board()

        # 4) Logout - logging the user out
        elif user_answer in ["4", "logout"]:
            return self.__logout()

        else:
            return self.__logged_in_menu_exec()

    def __choose_difficulty(self):
        # a function for choosing the Sudoku's difficulty
        print("Please choose a difficulty: \n1) Easy \n2) Medium \n3) Hard \n")
        user_answer = input_from_user()
        difficulty = None

        if user_answer in ["1", "easy"]:
            difficulty = "Easy"
        elif user_answer in ["2", "medium"]:
            difficulty = "Medium"
        elif user_answer in ["3", "hard"]:
            difficulty = "Hard"
        else:
            return self.__choose_difficulty()

        return self.__get_game_board(difficulty)

    def __get_game_board(self, difficulty):
        # getting the board from server according to difficulty
        response_from_server = self.client.create_game_board(difficulty)
        # creating the game_board.csv file using the board just received from the server
        save_in_csv(self.BOARD_PATH, response_from_server.json())
        self.client.save_player_info(self.username, difficulty)

        print("Your board was created! go ahead and solve it and then send it!")
        print("Remember! The timer has started, you're on the clock. Let's see what you got!")
        print("Loading previous menu... \n")
        return self.__logged_in_menu_text()

    def __send_completed_board(self):
        response_from_server = self.client.finished_game__board()
        validity = response_from_server.content.decode()

        if validity == "BOARD WAS NOT CREATED":
            print("Board was NOT created yet. Please create a board first.")

        elif validity == "The Board is NOT full!!":
            print("The Board is NOT full!!, Fill it up please.")

        elif validity in ["Something went wrong", "REQUEST FAILURE"]:
            print("Something went wrong.. file is NOT valid.")

        elif validity == "True":
            # adding the score to the ScoreBoard via server
            response_from_server = self.client.add_score_to_score_board(self.username)
            if response_from_server.content.decode() == "BOARD ALREADY SUBMITTED":
                print("This board was already submitted!! you're not fooling anyone! create a new board.")
            else:
                print("Nice!! The board you've sent is valid!")
                print("Adding you now to the ScoreBoard!")

        elif validity == "False":
            # board sent wasn't valid
            print("Unfortunately the board you've sent is NOT valid. \nPlease try again.")

        elif validity == "NOT SAME USER":
            print(f"It seems like it's not your sudoku board {self.username.capitalize()}..")
            print("Please try creating a new board.")

        print("Loading logged in menu... \n")
        return self.__logged_in_menu_text()

    def __logout(self):
        self.client.logout()
        print(f"{self.username.capitalize()} Logged out. \nLoading main menu... \n")
        self.username = None
        return self.__main_menu_text()

    def __show_score_board(self):
        response_from_server = self.client.show_score_board()
        list = response_from_server.json()
        for score in list:
            print(*score)

        print("\n1) Get back to previous menu")
        user_answer = input_from_user()
        while user_answer != "1":
            print("1) Get back to previous menu")
            user_answer = input_from_user()
        print("Loading previous menu... \n")
        if self.username:
            return self.__logged_in_menu_text()
        return self.__main_menu_text()


class Client:
    def __init__(self):
        # creating the Client object
        self.requests = requests.Session()

    # GET FUNCTIONS:
    def logout(self):
        return self.requests.get(f'http://127.0.0.1:5000/logout')

    def show_score_board(self):
        return self.requests.get(f'http://127.0.0.1:5000/show_score_board')

    # POST FUNCTIONS:
    def sign_up(self, username, password):
        return self.requests.post(f'http://127.0.0.1:5000/sign_up', json=(username, password))

    def login(self, username, password):
        return self.requests.post(f'http://127.0.0.1:5000/login', json=(username, password))

    def create_game_board(self, difficulty):
        return self.requests.post(f'http://127.0.0.1:5000/create_game_board', json=difficulty)

    def finished_game__board(self):
        return self.requests.post(f'http://127.0.0.1:5000/finished_game__board', json=take_from_csv(game.BOARD_PATH))

    def save_player_info(self, Name, Difficulty):
        return self.requests.post(f'http://127.0.0.1:5000/save_player_info', json=(Name, Difficulty))

    def add_score_to_score_board(self, Name):
        return self.requests.post(f'http://127.0.0.1:5000/add_score_to_score_board', json=Name)


def input_from_user():
    # taking input from the user and lowercase all letters and deleting spaces
    string = input().replace(" ", "").lower()
    # checks if the user wants to quit
    if string in ["exit", "quit"]:
        exit_game()
    return string


def exit_game():
    # stops running the program
    print("Exiting Game..")
    sys.exit()


def save_in_csv(path, thing_to_save):
    # saves a csv file
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(thing_to_save)


def take_from_csv(path):
    # takes content from a csv file
    try:
        with open(path, newline='') as f:
            reader = csv.reader(f)
            content_csv = []
            for row in reader:
                row_to_print = []
                for square in row:
                    row_to_print.append(square)
                content_csv.append(row_to_print)
            return content_csv
    except FileNotFoundError:
        save_in_csv(path, "")


if __name__ == '__main__':
    # initializing
    game = Game()
    # starting the game
    game.introduction()
