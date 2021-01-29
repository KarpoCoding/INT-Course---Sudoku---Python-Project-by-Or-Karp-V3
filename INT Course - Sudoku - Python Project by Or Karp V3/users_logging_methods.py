def sign_up():
    # taking the Username field from the user
    username = no_spaces_lowercase(input("Please enter your desired Username: \n"))
    # taking the Password field from the user
    password = no_spaces_lowercase(input("Please enter your desired Password: \n"))

    return username, password


def login():
    # asking for the username and password fields in order to login
    username = input("Please enter your Username: \n").lower()
    password = input("Please enter your Password: \n").lower()
    return username, password


def logout():
    # asks for the username in order to logout
    username = input("Please enter your username in order to logout: \n").lower()
    return username


def no_spaces_lowercase(string):
    # a function that makes sure you don't type any spaces in your input and returns the string with all lowercase letters when it doesn't contain any spaces
    while " " in string:
        print("That's not valid!! spaces are not allowed. Try Again:")
        string = input()
    return string.lower()


if __name__ == '__main__':
    # sudokuDB = SudokuDB(r"DB_Folder/sudokuDB.db")
    # sudokuDB.create_connection()
    # sudokuDB.main()
    # user = User()

    # user.sign_up()
    # user.login()

    # sudokuDB.add_username("Or", "1234")
    # sudokuDB.show_table("Users")
    pass

