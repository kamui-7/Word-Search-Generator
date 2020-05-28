import string, random
import json, sys
from subprocess import call
import os, logging

num_puzzle = int(sys.argv[1])
alphabet = string.ascii_uppercase
board = [[random.choice(alphabet) for _ in range(10)] for _ in range(10)]
num_ver = [[[num, x] for x in range(10)] for num in range(10)]
logging.basicConfig(level=logging.INFO)


class Letter:
    def __init__(self, char):
        self.char = char


def possible_locs(puzzle_board):
    pos = []
    count = 1
    for row_num, num in enumerate(puzzle_board):
        while count < 10:
            pos.append(num[:count + 1])
            count += 1
        count = 1
    return pos


def get_verticals(puzzle_board):
    flipped = zip(*puzzle_board)
    return possible_locs(flipped)


def get_diagonals(grid, bltr=True):
    dim = len(grid)
    assert dim == len(grid[0])
    return_grid = [[] for total in range(2 * len(grid) - 1)]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if bltr:
                return_grid[row + col].append(grid[col][row])
            else:
                return_grid[col - row + (dim - 1)].append(grid[row][col])
    return return_grid




def load_words():
    with open("Themed_Vocab.json") as f:
        return json.load(f)


def print_file(filename):
    abs_path = f'"{os.path.abspath(filename)}"'
    call(f"notepad /p {abs_path}",shell=True)


def make_word_search(outFile, text):
    with open(outFile, "w", encoding="utf8") as f:
        f.write(text)


def string_board(words):
    board_string = f"{theme.title()}\n\n"
    for row in board:
        for cell in row:
            if isinstance(cell, Letter):
                board_string += f"{cell.char}    "
            else:
                board_string += f"{cell}    "
        board_string += "\n\n"

    board_string += f"\nWord Bank\n================================\n"
    board_string += f"{'   '.join(words[:4])}\n{'   '.join(words[5:10])}"
    return board_string


def rm_dup(dup_list):
    unique = []
    for item in dup_list:
        if item in unique:
            continue
        unique.append(item)
    return unique


def valid_loc(coors, letters):
    for coor, l in zip(coors, letters):
        if isinstance(board[coor[0]][coor[1]], Letter):
            if board[coor[0]][coor[1]].char == l:
                continue
            else:
                return False
    return True


diags = get_diagonals(num_ver, bltr=False) + get_diagonals(num_ver)
verticals = get_verticals(num_ver)
horizontals = possible_locs(num_ver)
vocab_bank = {k: v for k, v in load_words().items() if len(v) >= 10}
theme = ""
for i in range(num_puzzle):
    logging.info(f"Starting to work on puzzle number {i}.")
    theme = random.choice(list(vocab_bank.keys()))
    try:
        chosen_words = [x.strip() for x in vocab_bank[theme]
                        if all([l.upper() in alphabet for l in x.strip()]) and len(x.strip()) <= 10]
        if len(chosen_words) < 10:
            continue
        chosen_words = random.sample(chosen_words,10)

    except Exception as e:
        print(e)
    for word in chosen_words:
        letters = [Letter(x) for x in word.upper()] # + horizontals + verticals
        h = [x for x in diags if len(x) >= len(letters)]
        locs = rm_dup([coor[x:x + len(letters)] for coor in h for x in range((len(coor) - len(letters)) + 1)])
        chosen_loc = random.choice(locs)
        retries = 10
        invalid_pos = False
        while not valid_loc(chosen_loc, letters):
            if retries >= 90:
                invalid_pos = True
                break
            chosen_loc = random.choice(locs)
            retries += 1
        if invalid_pos:
            new_word = random.choice([x.strip() for x in vocab_bank[theme]
                                           if all([l.upper() in alphabet for l in x.strip()]) and len(x) <= 10 and x not in chosen_words])
            chosen_words.append(new_word)
            break
        for pos, letter in zip(chosen_loc, letters):
            board[pos[0]][pos[1]] = letter

    output = f"{theme}_Word_Search.txt"
    make_word_search(output ,string_board(chosen_words))
    # print_file(output)
    # os.remove(output)
