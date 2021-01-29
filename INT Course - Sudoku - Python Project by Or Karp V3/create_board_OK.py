from random import randint


class Board:
    def __init__(self):
        self.board = empty_board()
        self.random_nums_list = random_nums_list()
        self.squares_to_fill = None

    def create_full_board(self):
        # going through all rows
        for row in range(9):
            # going through all columns
            for column in range(9):
                # checking if the square is empty
                if self.board[row][column] == 0:
                    for value in self.random_nums_list:
                        # inserting a random value into the empty square
                        self.board[row][column] = value
                        # checking if it's a valid insert
                        if self.check_square_validity(square_row=row, square_column=column):
                            # if it is valid it starts a recursion until the board is complete OR it encounters an 'ERROR'
                            if self.create_full_board():
                                return self.board
                        # if the 'ERROR' occurs it resets the square and tries different value insertions
                        self.board[row][column] = 0
                    # this is the 'ERROR' which happens when none of the values in the random_nums_list is valid to insert into the square
                    return False
        # if the board is completely full it will get here and start returning True over and over again until it reaches the very first run of the function
        # and then it will execute 'return self.board'
        return True

    def check_square_validity(self, square_row, square_column):
        # checking row
        duplicates_list = []
        for num in self.board[square_row]:
            if num not in duplicates_list:
                if num != 0:
                    duplicates_list.append(num)
            else:
                return False

        # checking column
        duplicates_list = []
        for row in range(9):
            if self.board[row][square_column] not in duplicates_list:
                if self.board[row][square_column] != 0:
                    duplicates_list.append(self.board[row][square_column])
            else:
                return False

        # checking block
        duplicates_list = []
        block_list = return_block_list_of_square(self.board, square_row, square_column)
        for num in block_list:
            if num not in duplicates_list:
                if num != 0:
                    duplicates_list.append(num)
            else:
                return False

        return True

    def make_board(self, difficulty):
        # creating a full sudoku board
        self.board = self.create_full_board()

        # checking what is the difficulty
        if difficulty == "Easy":
            self.squares_to_fill = 50
        elif difficulty == "Medium":
            self.squares_to_fill = 40
        elif difficulty == "Hard":
            self.squares_to_fill = 30

        # deleting squares from the completed board until it fits the difficulties conditions
        while check_how_many_is_filled(self.board) != self.squares_to_fill:
            self.delete_random_square()

        return self.board

    def delete_random_square(self):
        # a function that deletes a random square from the board
        rand_num1 = random_number()
        rand_num2 = random_number()
        if self.board[rand_num1][rand_num2] != 0:
            self.board[rand_num1][rand_num2] = 0
        else:
            return self.delete_random_square()


def check_board_validity(board):
    try:
        # checks if the board is full
        if check_how_many_is_filled(board) != 81:
            return "The Board is NOT full!!"

        # checks if the user cheated or not
        if not check_if_board_nums_r_valid(board):
            return False

        # checking row
        for row in board:
            if len(set(row)) != 9:
                return False

        # checking column
        for column in range(9):
            column_list = []
            for num_index in range(9):
                if board[column][num_index] not in column_list:
                    column_list.append(board[column][num_index])
                else:
                    return False

        if not check_blocks_validity(board):
            return False

        return True

    except Exception as e:
        print(e)
        return "Something went wrong"


def empty_board():
    # a function that creates an empty board
    board = []
    row = []

    for i in range(9):
        row.append(0)
    for i in range(9):
        board.append(row.copy())
    return board


def random_nums_list():
    list_o_random_nums = []
    random_num = randint(1,9)
    while len(list_o_random_nums) != 9:
        if random_num not in list_o_random_nums:
            list_o_random_nums.append(random_num)
        random_num = randint(1,9)
    return list_o_random_nums


def print_board(board):
    for row in board:
        print(row)
    # print(f"This many squares are filled: {check_how_many_is_filled(board)}")


def return_block_list_of_square(board, square_row, square_column):
    block_list = []
    block_x = None
    block_y = None

    # checking the x of the block section
    block_x = (square_column//3) * 3
    # checking the y of the block section
    block_y = (square_row//3) * 3

    # appending to a list the elements of the chosen block
    for column_index in range(3):
        # appending the column nums
        for row_index in range(3):
            block_list.append(board[block_y + row_index][block_x + column_index])

    return block_list


def check_blocks_validity(board):
    block_list = []
    for block_y in range(3):
        for block_x in range(3):
            for num_x in range(3):
                # appending the column nums
                for num_y in range(3):
                    block_list.append(board[block_y * 3 + num_y][block_x * 3 + num_x])

            if len(set(block_list)) != 9:
                return False
            block_list = []

    return True


def check_how_many_is_filled(board):
    # taking a Board and checking how many squares are filled in the board
    how_many_filled = 0
    for row in board:
        for elem in row:
            if int(elem) != 0:
                how_many_filled += 1
    return how_many_filled


def check_if_board_nums_r_valid(board):
    # makes sure the user used only numbers between 1-9 and didn't try to cheat
    for row in board:
        for elem in row:
            if int(elem) > 9 or int(elem) < 1:
                return False
    return True


def random_number():
    return randint(0, 8)


if __name__ == '__main__':
    board = Board()
    # print(board.make_board("Easy"))
    # print_board(board.board)
    # print(board.board)
    # print_board(board.board)
    # print(random_nums_list())
    # print(board.create_full_board())
    game_board = board.create_full_board()
    print_board(game_board)
    print(check_board_validity(game_board))
