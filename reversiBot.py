import numpy as np
places_score = [
    [ 8, -2,  4,  4,  4,  4, -2,  8],
    [-2, -6, -4, -4, -4, -4, -6, -2],
    [ 4, -4,  2,  2,  2,  2, -4,  4],
    [ 4, -4,  2,  0,  0,  2, -4,  4],
    [ 4, -4,  2,  0,  0,  2, -4,  4],
    [ 4, -4,  2,  2,  2,  2, -4,  4],
    [-2, -6, -4, -4, -4, -4, -6, -2],
    [ 8, -2,  4,  4,  4,  4, -2,  8]                                                                                                  
]


class Board:
    def __init__(self, board: "np.array[np.array[int]]") -> None:
        self.lst = board

    def __getitem__(self, item) -> "np.array[int]":
        return self.lst[item]

    def __repr__(self) -> str:
        ret = "--" * 9 + "\n"
        for i in range(8):
            ret += "|" + "".join(map(lambda x: "  " if x == 0 else ("○ " if x == 1 else "● "), self[i])) + "|\n"
        ret += "--" * 9
        return ret

    def __str__(self) -> str:
        ret = "--" * 9 + "\n"
        for i in range(8):
            ret += "|" + "".join(map(lambda x: "  " if x == 0 else ("○ " if x == 1 else "● "), self[i])) + "|\n"
        ret += "--" * 9
        return ret

    def copy(self) -> "Board":
        return Board(np.array(map(np.array.copy, self.lst)))

    def in_board(self, i, j) -> bool:
        return 8 > i >= 0 and 8 > j >= 0

    def get_score(self, me: int) -> int:
        score = 0

        for i in range(8):
            for j in range(8):
                value = self[i][j]
                if value != 0:
                    if value == me:
                        score += 1
                    else:
                        score -= 1

        return score

    def get_basic_rate_for_move(self, i: int, j: int) -> float:
        # should give higher favor for corners; better than just edge
        return places_score[i][j]

    def get_rating(self, me: int, depth: int) -> float:
        if depth == 0:
            # base evaluation
            return self.get_score(me)

        enemy = 3 - me

        max_eval = float("-inf")

        for i, j in self.get_valid_moves(me):
            new_board = self.copy()
            changes = new_board.do_move(me, i, j)
            current_eval = len(changes)
            for changed_i, changed_j in changes:
                current_eval += new_board.get_basic_rate_for_move(changed_i, changed_j)
            current_eval -= 0.75 * new_board.get_rating(enemy, depth - 1)

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

    def get_valid_moves(self, me: int) -> "np.array[tuple[int, int]]":
        moves = []

        for i in range(8):
            for j in range(8):
                if self.is_valid(me, i, j):
                    moves.append((i, j))

        return moves

    def do_move(self, me: int, i: int, j: int) -> "np.array[tuple[int, int]]":
        enemy = 3 - me
        changes = [[i, j]]
        self[i][j] = me
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

                changes += line
        return changes


# A function to return your next move.
# 'board' is a 8x8 int array, with 0 being an empty cell and 1,2 being you and the opponent,
# determained by the input 'me'.
def get_move(me: int, board: "list[list[int]]") -> "tuple[int, int]":
    board = np.array(map(np.array, board))
    board_board = Board(board)
    max_rating = float("-inf")
    valid_moves = board_board.get_valid_moves(me)

    # if there is no valid move, the bot will never be called in the first place. For safety, we return an invalid result.
    if len(valid_moves) == 0:
        return "NO VAILD MOVES!!!!!!"

    ret = valid_moves[0]

    for move in valid_moves:
        board1 = board_board.copy()
        board1.do_move(me, move[0], move[1])
        rating = -board1.get_rating(3 - me, 3)

        if rating > max_rating:
            max_rating = rating
            ret = move

    return ret
