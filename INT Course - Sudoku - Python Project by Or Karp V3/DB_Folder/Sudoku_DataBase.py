import sqlite3


class SudokuDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.c = None

    def create_connection(self):
        try:
            # setting the connection to the DB file, if the file DOES NOT exist - creates it.
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)

        except Exception as e:
            print(e)

        finally:
            # self.c = the DB Cursor
            self.c = self.connection.cursor()

    def create_db_tables(self):
        sql_create_usernames_table = """CREATE TABLE IF NOT EXISTS Users (
        ID Integer PRIMARY KEY,
        Username text NOT NULL,
        Hash text NOT NULL
        );"""

        sql_create_scores_table = """CREATE TABLE IF NOT EXISTS Scores (
        ID Integer PRIMARY KEY,
        Name text NOT NULL,
        TimeInMinutes int NOT NULL,
        Difficulty text NOT NULL,
        DifficultyIndex text NOT NULL
        );"""

        # creating the DB Tables
        if self.connection:
            self.create_table(sql_create_usernames_table)
            self.create_table(sql_create_scores_table)
        else:
            print("Error! Cannot connect to database.")

    def create_table(self, table_to_create):
        self.c.execute(table_to_create)

    def show_scores_table(self):
        list_of_strings = [["SCOREBOARD: \n"]]
        self.c.execute(f"""SELECT * FROM Scores ORDER BY DifficultyIndex, TimeInMinutes LIMIT 10;""")
        list_of_scores = self.c.fetchall()
        for tup in list_of_scores:
            list_of_strings.append([f"{list_of_scores.index(tup)+1}. {tup[1]}, TimeInMinutes: {tup[2]}, Difficulty: {tup[3]}"])
        return list_of_strings

    def take_hash(self, username):
        # returns the hash from the Users table according to a username
        try:
            self.c.execute(f"SELECT Hash FROM Users WHERE Username = ?", (username,))
            return self.c.fetchall()[0][0]
        except IndexError:
            return "User doesn't exist"

    # def take_usernames(self):
    #     # returns all usernames from the Users table
    #     self.c.execute(f"SELECT Username FROM Users")
    #     try:
    #         return self.c.fetchall()[0][0]
    #     except:
    #         return "EMPTY"

    def check_if_user_exists(self, username):
        self.c.execute(f"SELECT Username FROM Users WHERE Username = ?", (username,))
        return bool(self.c.fetchall())

    def add_username(self, username, hash):
        if not self.check_if_user_exists(username):
            self.c.execute("""INSERT INTO Users (Username,Hash)
            VALUES (?,?)""", (username, hash))
            self.connection.commit()
            return True
        return False

    def add_score(self, username, time_in_minutes, difficulty):
        # checking if this score exists
        if not self.check_if_score_exists(username, time_in_minutes, difficulty):
            difficulty_index = None

            if difficulty == "Hard":
                difficulty_index = 1
            elif difficulty == "Medium":
                difficulty_index = 2
            elif difficulty == "Easy":
                difficulty_index = 3

            self.c.execute("""INSERT INTO Scores (Name,TimeInMinutes,Difficulty,DifficultyIndex)
            VALUES (?,?,?,?)""", (username, time_in_minutes, difficulty,difficulty_index))
            self.connection.commit()

    def check_if_score_exists(self, Name, TimeInMinutes, Difficulty):
        self.c.execute("SELECT Name, TimeInMinutes, Difficulty FROM Scores WHERE Name = ? AND TimeInMinutes = ? AND Difficulty = ?", (Name,TimeInMinutes,Difficulty))
        if self.c.fetchall():
            return True
        return False


if __name__ == '__main__':
    sudokuDB = SudokuDB(r"sudokuDB.db")
    sudokuDB.create_connection()
    sudokuDB.create_db_tables()

    # print(sudokuDB.return_scores_table_length())
    # sudokuDB.update_scores_table()
    # sudokuDB.add_score(username="YA",time_in_minutes=2,difficulty="Medium")
    # sudokuDB.show_table("Scores")
    # print(sudokuDB.scores_table_length())
    # sudokuDB.add_username("Or", "1234")
    # sudokuDB.show_table("Users")
    # sudokuDB.delete_username("Or", "1234")
    # sudokuDB.update_username()
    # sudokuDB.update_password()
    # sudokuDB.delete_table("Scores")
    print(sudokuDB.take_usernames())
