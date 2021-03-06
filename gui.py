#!/usr/bin/python

import Tkinter as tk
from Tkinter import Label
import random
import time

import FileReader as fileReader
from tile import Piece
from tile import Tile
from tile import combine_pieces
from tile import zero_pieces
from tile import find_locations


class MainWindow(tk.Frame):
    puzzle_name = 'No puzzle selected'

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(
            self, text="Trivial",
            command=lambda puzzle_name='input_files/input_small.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Checkerboard",
            command=lambda puzzle_name='input_files/input_checkerboard.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Pentominoes 3x20",
            command=lambda puzzle_name='input_files/pentominoes3x20.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Pentominoes 4x15",
            command=lambda puzzle_name='input_files/pentominoes4x15.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Pentominoes 5x12",
            command=lambda puzzle_name='input_files/pentominoes5x12.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Pentominoes 6x10",
            command=lambda puzzle_name='input_files/pentominoes6x10.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="IQ Creator",
            command=lambda puzzle_name='input_files/IQ_creator.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Lucky Thirteen",
            command=lambda puzzle_name='input_files/lucky13.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Partial Cross",
            command=lambda puzzle_name='input_files/partial_cross.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Test 1",
            command=lambda puzzle_name='input_files/test1.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Test 2",
            command=lambda puzzle_name='input_files/test2.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="13 Holes",
            command=lambda puzzle_name='input_files/thirteen_holes.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Your Puzzle",
            command=lambda puzzle_name='input_files/your_puzzle.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")

    def create_window(self, puzzle_name):
        t = tk.Toplevel(self)
        t.wm_title("Puzzle: %s" % puzzle_name)
        content = fileReader.read_file(puzzle_name)

        puzzle_pieces_and_board = self.get_puzzle_pieces(content)
        puzzle_pieces = puzzle_pieces_and_board[0]
        game_board = puzzle_pieces_and_board[1]

        board = tk.Canvas(t, bg="grey", height=350, width=600)

        color = ["red", "orange", "yellow", "green", "blue", "violet"]
        # random.choice(color)

        board.button = tk.Button(
            t, text="Solve Puzzle",
            command=lambda puzzle_pieces=puzzle_pieces, game_board=game_board: self.solve_puzzle(puzzle_pieces, game_board)
        )
        board.button.pack(side="top")

        org_x1 = 10
        org_x2 = 20
        org_x3 = 20
        org_x4 = 10
        x1 = org_x1
        y1 = 10
        x2 = org_x2
        y2 = 10
        x3 = org_x3
        y3 = 20
        x4 = org_x4
        y4 = 20
        value1 = ''
        value2 = ''

        for line in content:
            for letter in line:
                if letter == ' ':
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='grey'
                    )
                elif(letter == value1):
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='black'
                    )
                elif(letter == value2):
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='white'
                    )
                elif(letter != value1 and letter != value2 and value1 == ''):
                    value1 = letter
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='black'
                    )
                elif(letter != value1 and letter != value2 and value2 == ''):
                    value2 = letter
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='white'
                    )
                x1 = x1 + 10
                x2 = x2 + 10
                x3 = x3 + 10
                x4 = x4 + 10
            y1 = y1 + 10
            y2 = y2 + 10
            y3 = y3 + 10
            y4 = y4 + 10
            x1 = org_x1
            x2 = org_x2
            x3 = org_x3
            x4 = org_x4

        board.pack()
        board.pack(side="top", fill="both", expand=True, padx=50, pady=50)

    # create list of x values used for a tile object
    # remove x values from list once a grey square on the x value
    def get_puzzle_pieces(self, content):
        all_tiles = []
        all_indexes = []
        all_pieces = []

        # find position and color of each tile and store it
        tile_position_y = 0
        color1 = ''
        color2 = ''
        for line in content:
            tile_position_x = 0
            for letter in line:
                if letter != ' ':
                    new_position = [tile_position_x, tile_position_y]
                    new_tile = Tile(new_position)
                    all_indexes.append(new_position)
                    if letter == color2:
                        new_tile.set_color(1)
                    elif color1 == '':
                        color1 = letter
                    elif color2 == '' and letter != color1:
                        color2 = letter
                        new_tile.set_color(1)
                    all_tiles.append(new_tile)

                tile_position_x = tile_position_x + 1
            tile_position_y = tile_position_y + 1

        # searches through list of tiles to find pieces
        piece_to_tile = {}
        for tile in all_tiles:
            position = tile.get_position()
            str_position = str(position)
            check_position_up = [position[0], position[1] - 1]
            check_position_left = [position[0] - 1, position[1]]
            check_position_up_right = [position[0] + 1, position[1] - 1]

            if check_position_up in all_indexes or check_position_left in all_indexes or check_position_up_right in all_indexes:
                for piece in all_pieces:
                    blocks = piece.get_positions()
                    if check_position_up in blocks or check_position_left in blocks or check_position_up_right in blocks:
                        piece.add_block(tile)
                        if str_position in piece_to_tile:
                            # combine current piece and piece with same tile
                            # remove both from all_pieces and add new_piece
                            conflict_piece = piece_to_tile[str_position]
                            new_piece = combine_pieces(piece, conflict_piece)
                            all_pieces.remove(piece)
                            all_pieces.remove(conflict_piece)
                            all_pieces.append(new_piece)

                            piece_to_tile[str_position] = new_piece
                        else:
                            piece_to_tile[str_position] = piece
            else:
                piece = Piece([tile])
                all_pieces.append(piece)
                piece_to_tile[str_position] = piece

        # for key in all_pieces:
        #     print key.get_size()
        all_pieces = zero_pieces(all_pieces)

        # searches through list of pieces to find the board (largest piece)
        largest_piece_index = 0
        largest_size = 0
        piece_index = 0
        for piece in all_pieces:
            if piece.get_size() > largest_size:
                largest_piece_index = piece_index
                largest_size = piece.get_size()
            piece_index = piece_index + 1

        board = all_pieces[largest_piece_index]
        board.set_board(True)
        all_pieces.remove(board)

        # import pdb; pdb.set_trace()

        return [all_pieces, board]

    def solve_puzzle(self, puzzle_pieces, game_board):

        y_list = []
        x_list = []
        for value in game_board.get_positions():
            y_list.append(value[1])
            x_list.append(value[0])
        max_x = x_list[len(x_list) - 1]
        max_y = y_list[len(y_list) - 1]

        start = time.time()

        total_piece_size = 0
        for piece in puzzle_pieces:
            total_piece_size = total_piece_size + piece.get_size()

        num_locations = find_locations(puzzle_pieces, game_board, max_x, max_y)

        # import pdb; pdb.set_trace()
        # need to change to check after the locations are retrieved
        if total_piece_size < len(game_board.get_positions()) or game_board.get_positions() == []:
            end = time.time()
            t = tk.Toplevel(self)
            t.wm_title("Puzzle Solution")

            num_solutions_label = Label(t, text='There are not enough pieces to solve this puzzle.')
            num_solutions_label.pack(padx=10, pady=10)

            num_solutions_label = Label(t, text='Determined in %s' % str(end-start))
            num_solutions_label.pack(padx=10, pady=10)

            return

        number_of_possibilities = sorted(num_locations.keys())

        solutions = []
        temp_solution = []
        number_of_solutions = 0
        first_flag = True
        first_end = 0

        # import pdb; pdb.set_trace()

        # add board position to orig positions and remove from board

        # outer most row (for each frequency of occurance)
        temp_board_outer = game_board.get_positions()
        for x in number_of_possibilities:

            # middle row (for each piece in occurance)
            temp_board_middle = temp_board_outer
            for piece in num_locations[x]:

                # rotation for each piece
                temp_board_inner = temp_board_middle
                for rotation in piece.get_rotations():
                    # inner most row (for each location of piece)

                    for first_piece in rotation.get_locations():

                        x_value = first_piece[0][0]
                        y_value = first_piece[0][1]
                        all_locations = []
                        for location in first_piece[1]:
                            new_x = location[0] + x_value
                            new_y = location[1] + y_value
                            all_locations.append([new_x, new_y])

                        remove = 0
                        for location in all_locations:
                            if location in temp_board_inner:
                                remove = remove + 1
                        if remove == len(all_locations):
                            prev_solution = temp_solution
                            temp_solution.append(all_locations)
                            for location in all_locations:
                                temp_board_inner.remove(location)

                            if len(temp_board_inner) == 0:
                                if first_flag == True:
                                    first_end = time.time()
                                solutions.append(temp_solution)
                                number_of_solutions = number_of_solutions + 1
                                temp_board_inner = temp_board_middle
                                temp_solution = prev_solution
                                first_flag = False
                            break

                if len(temp_board_inner) != 0 and len(temp_solution) > 0:
                    temp_board_middle = temp_board_inner

        end = time.time()
        if first_end == 0:
            first_end = start

        t = tk.Toplevel(self)
        t.wm_title("Puzzle Solution")

        num_solutions_label = Label(t, text='Number of Solutions:')
        num_solutions_label.pack()
        num_solutions = Label(t, text=str(number_of_solutions))
        num_solutions.pack(pady=5)

        w = Label(t, text='CPU Time for 1 Solution:')
        w.pack()
        w = Label(t, text=str(first_end-start))
        w.pack(pady=5)

        w = Label(t, text='CPU Time for All Solutions:')
        w.pack()
        w = Label(t, text=str(end-start))
        w.pack(pady=5)

        board = tk.Canvas(t, bg="grey", height=150, width=300)

        color = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']

        org_x1 = 10
        org_x2 = 20
        org_x3 = 20
        org_x4 = 10
        x1 = org_x1
        y1 = 10
        x2 = org_x2
        y2 = 10
        x3 = org_x3
        y3 = 20
        x4 = org_x4
        y4 = 20

        for solution in solutions:
            for piece in solution:
                piece_color = random.choice(color)
                for tile in piece:
                    # import pdb; pdb.set_trace()
                    tile_1 = tile[0] + 1
                    tile_2 = tile[1] + 1
                    board.create_polygon(
                        x1 + (x1 * tile_1),
                        y1 + (x1 * tile_2),
                        x2 + (x1 * tile_1),
                        y2 + (x1 * tile_2),
                        x3 + (x1 * tile_1),
                        y3 + (x1 * tile_2),
                        x4 + (x1 * tile_1),
                        y4 + (x1 * tile_2),
                        fill=piece_color
                    )

        board.pack()
        board.pack(side="top", fill="both", expand=True, padx=50, pady=50)

        return []

    def no_solution(self, end_time, start_time):
        t = tk.Toplevel(self)
        t.wm_title("Puzzle Solution")

        num_solutions_label = Label(t, text='There is no solution to this puzzle.')
        num_solutions_label.pack(padx=10, pady=10)

        num_solutions_label = Label(t, text='Determined in %s' % str(end_time-start_time))
        num_solutions_label.pack(padx=10, pady=10)

        return


if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    root.mainloop()
