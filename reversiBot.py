import random

class Board:
    def __init__(self, board: "list[list[int]] | None" = None, size: int = 8) -> None:
        if board is None:
            self.lst = [[0 for x in range(8)] for y in range(3)] + [[0, 0, 0, 2, 1, 0, 0, 0]] + [[0, 0, 0, 1, 2, 0, 0, 0]] + [[0 for x in range(8)] for y in range(3)]
        else:
            self.lst = board
        self.board_size = size
        # self.dir = {(0, 0): 10, (0, 1): -1, (1, 0): -1, (1, 1): -8, (size-1, size-1): 10, (size-1, size-2): -1, (size-2, size-1): -1, (size-2, size-2): -8, (0, size-1): 10, (0, size-2): -1, (1, size-1): -1, (1, size-2): -8, (size-1, 0): 10, (size-1, 1): -1, (size-2, 0): -1, (size-2, 1): -8,}
        # for i in range(size):
        #     for j in range(size):
        #         if((i, j) not in self.dir.keys()):
        #             if i == self.board_size - 1 or i == 0 or j == self.board_size - 1 or j == 0:
        #                 self.dir[(i, j)] = 6
        #             if i == self.board_size - 2 or i == 1 or j == self.board_size - 2 or j == 1:
        #                 self.dir[(i, j)] = -5
        #             if i == self.board_size - 3 or i == 2 or j == self.board_size - 3 or j == 2:
        #                 self.dir[(i, j)] = 2
        #             self.dir[(i, j)] = 0
        # is this ok?
        


    def __getitem__(self, item) -> "list[int]":
        return self.lst[item]

    def __repr__(self) -> str:
        ret = "--" * 9 + "\n"
        for i in range(self.board_size):
            ret += "|" + "".join(map(lambda x: "  " if x == 0 else ("○ " if x == 1 else "● "), self[i])) + "|\n"
        ret += "--" * 9
        return ret

    def __str__(self) -> str:
        ret = "--" * 9 + "\n"
        for i in range(self.board_size):
            ret += "|" + "".join(map(lambda x: "  " if x == 0 else ("○ " if x == 1 else "● "), self[i])) + "|\n"
        ret += "--" * 9
        return ret

    def copy(self):
        return Board(list(map(list.copy, self.lst)), self.board_size)

    def in_board(self, i, j) -> bool:
        return self.board_size > i >= 0 and self.board_size > j >= 0

    def get_score(self, me: int) -> int:
        score = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                value = self[i][j]
                if value != 0:
                    if value == me:
                        score += 1
                    else:
                        score -= 1

        return score

    # TODO: readd penalty for things adjecect to edge
    def get_basic_rate_for_move(self, i: int, j: int) -> float:
        # TODO improve evaluation
        # should give higher favor for corners; better than just edge
        #if (i == self.board_size - 1 or i == 0) and (j == self.board_size - 1 or j == 0):
        if (i == self.board_size - 1 and j == self.board_size - 1) or (i == 0 and j == 0) or (j == self.board_size - 1 and i == 0) or (j == 0 and i == self.board_size - 1):
            return 1000
        if i == self.board_size - 1 or i == 0 or j == self.board_size - 1 or j == 0:
            return 5
        return 0

    def get_rating(self, me: int, depth: int) -> float:
        if depth == 0:
            # base evaluation
            return self.get_score(me)

        enemy = 3 - me

        max_eval = float("-inf")

        for i, j in self.get_valid_moves(me):
            new_board = self.copy()
            current_eval = new_board.do_move(me, i, j)
            current_eval += new_board.get_basic_rate_for_move(i, j) - new_board.get_rating(enemy, depth - 1)  # TODO: improve

            if current_eval > max_eval:
                max_eval = current_eval

        if max_eval == float("-inf"):
            return float("-inf") if self.get_score(me) < 0 else float("inf")
        return max_eval

    def is_valid(self, me: int, i: int, j: int) -> bool:
        if self[i][j] != 0:
            return False
        # check every direction
        enemy = 3 - me
        for di in range(-1, 2):
            for dj in range(-1, 2):
                current_j = j + dj
                current_i = i + di

                if not self.in_board(current_i, current_j) or self[current_i][current_j] != enemy:
                    continue
                if not (di == 0 == dj):
                    while self.in_board(current_i, current_j) and self[current_i][current_j] == enemy:
                        current_j += dj
                        current_i += di

                if not self.in_board(current_i, current_j) or self[current_i][current_j] != me:
                    continue

                return True

        return False

    def get_valid_moves(self, me: int) -> "list[tuple[int, int]]":
        moves = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.is_valid(me, i, j):
                    moves.append((i, j))

        return moves

    def do_move(self, me: int, i: int, j: int) -> int:
        enemy = 3 - me
        score = 0
        self.lst[i][j] = me
        for di in range(-1, 2):
            for dj in range(-1, 2):
                line = []
                current_j = j
                current_i = i

                current_j += dj
                current_i += di
                if not self.in_board(current_i, current_j) or self[current_i][current_j] != enemy:
                    continue

                while self.in_board(current_i, current_j) and self[current_i][current_j] == enemy:
                    line.append([current_i, current_j])
                    current_j += dj
                    current_i += di

                if not self.in_board(current_i, current_j) or self[current_i][current_j] != me:
                    continue

                for tile in line:
                    self[tile[0]][tile[1]] = me
                    score += 1
        return score


# A function to return your next move.
# 'board' is a 8x8 int array, with 0 being an empty cell and 1,2 being you and the opponent,
# determained by the input 'me'.
# TODO: I don't like this code
def get_move(me: int, board: "list[list[int]]"):
    board = Board(board, len(board))
    rate_for_moves = {}
    max = float("-inf")
    valid_moves = board.get_valid_moves(me)
    if len(valid_moves) == 0:
        return
    ret = random.choice(valid_moves)

    for move in valid_moves:
        board1 = board.copy()
        board1.do_move(me, move[0], move[1])
        rate = board1.get_rating(me, 3)
        rate_for_moves[move] = rate

    for key in rate_for_moves.keys():
        if rate_for_moves[key] > max:
            max = rate_for_moves[key]
            ret = key

    # if there is no valid move, the bot will never be called in the first place. For safety, we return an invalid result.
    return ret
