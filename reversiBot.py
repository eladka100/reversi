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
        return Board(self.lst.copy())

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

    # if the rating returned by this is equal or exceeds max_rating_for_use then it is not used and same for min_rating_for_use
    def get_rating(self, me: int, depth: int, min_rating_for_use: float=float("-inf"), max_rating_for_use: float=float("inf")) -> float:
        if depth == 0:
            # base evaluation
            return 0

        valid_moves, lines = self.get_valid_moves(me)
        enemy = 3 - me

        if len(valid_moves) == 0:
            if len(self.get_valid_moves(enemy)) == 0:
                return float("inf") if self.get_score(me) > 0 else float("-inf") # the game is over
            
            return -0.75 * self.get_rating(enemy, depth-1, -max_rating_for_use, -min_rating_for_use) # skip me's turn

        max_eval = min_rating_for_use

        for i, j in valid_moves:
            new_board = self.copy()
            changes = new_board.optimized_do_move(me, i, j, lines[(i,j)])
            current_eval = len(changes)
            for changed_i, changed_j in changes:
                current_eval += new_board.get_basic_rate_for_move(changed_i, changed_j)
            # max_rating_for_use calculation
            # this equation must be true for this move to be used:
            # current_eval - 3/4 * get_rating > max_eval
            # get_rating < (current_eval - max_eval) * 4/3
            # so the new max_rating_for_use is (current_eval - max_eval) * 4/3

            # min_rating_for_use calculation
            # this equation must be true for this move to be used:
            # max_rating_for_use > max_eval >= current_eval - 3/4 * get_rating
            # get_rating > (current_eval - max_rating_for_use) * 4/3
            # so the new min_rating_for_use is (current_eval - max_rating_for_use) * 4/3
            current_eval -= 0.75 * new_board.get_rating(enemy, depth - 1, (current_eval - max_rating_for_use) * 4/3, (current_eval - max_eval) * 4/3)

            if current_eval > max_eval:
                max_eval = current_eval
            
            if max_rating_for_use <= max_eval:
                return max_eval # if this is reached this move will not be played

        return max_eval
    
    def line_length(self, i, j, di, dj):
        me = self[i][j]
        enemy = 3 - me
        current_j = j + dj
        current_i = i + di
        length = 0

        while self.in_board(current_i, current_j) and self[current_i][current_j] == enemy:
            current_j += dj
            current_i += di
            length += 1

        if not self.in_board(current_i, current_j) or self[current_i][current_j] != 0:
            length = 0

        return length

    # def is_valid(self, me: int, i: int, j: int) -> bool:
    #     if self[i][j] != 0:
    #         return False
    #     # check every direction
    #     enemy = 3 - me
    #     for di in range(-1, 2):
    #         for dj in range(-1, 2):
    #             current_j = j + dj
    #             current_i = i + di

    #             if not self.in_board(current_i, current_j) or self[current_i][current_j] != enemy:
    #                 continue
    #             if not (di == 0 == dj):
    #                 while self.in_board(current_i, current_j) and self[current_i][current_j] == enemy:
    #                     current_j += dj
    #                     current_i += di

    #             if not self.in_board(current_i, current_j) or self[current_i][current_j] != me:
    #                 continue

    #             return True

    #     return False

    def get_valid_moves(self, me: int) -> "tuple[np.array[tuple[int, int]], dict[tuple[int, int], np.array[int]]]":
        valid_tiles = []
        tiles_to_lines = {}
        for i in range(8):
            for j in range(8):
                if self[i][j] != me:
                    continue
                for k in range(8):
                    di, dj = compute_direction(k)
                    l = self.line_length(i, j, di, dj)
                    if l>0:
                        m, n = i + (l+1)*di, j + (l+1)*dj
                        if not (m,n) in tiles_to_lines:
                            valid_tiles.append((m, n))
                            tiles_to_lines[(m, n)] = [0 for _ in range(8)]
                        tiles_to_lines[(m, n)][7-k] = l

        return valid_tiles, tiles_to_lines
    
    def optimized_do_move(self, me: int, i: int, j: int, lines: "np.array[int]") -> "np.array[tuple[int, int]]":
        changes = [(i, j)]
        self.lst[i][j] = me
        for k in range(8):
            di, dj = compute_direction(k)
            current_i, current_j = i + di, j + dj
            for _ in range(lines[k]):
                self[current_i][current_j] = me
                current_i += di
                current_j += dj
                changes.append((current_i, current_j))
        return changes

    # def do_move(self, me: int, i: int, j: int) -> "np.array[tuple[int, int]]":
    #     enemy = 3 - me
    #     self.lst[i][j] = me
    #     changes = [(i, j)]
    #     for di in range(-1, 2):
    #         for dj in range(-1, 2):
    #             line = []
    #             current_j = j
    #             current_i = i

    #             current_j += dj
    #             current_i += di
    #             if not self.in_board(current_i, current_j) or self[current_i][current_j] != enemy:
    #                 continue

    #             while self.in_board(current_i, current_j) and self[current_i][current_j] == enemy:
    #                 line.append([current_i, current_j])
    #                 current_j += dj
    #                 current_i += di

    #             if not self.in_board(current_i, current_j) or self[current_i][current_j] != me:
    #                 continue

    #             for tile in line:
    #                 self[tile[0]][tile[1]] = me
    #             changes += line
    #     return changes


def compute_direction(k) -> "tuple[int, int]":
        if k<4:
            return k % 3 - 1, k // 3 - 1
        return (k+1) % 3 - 1, (k+1) // 3 - 1

# A function to return your next move.
# 'board' is a 8x8 int array, with 0 being an empty cell and 1,2 being you and the opponent,
# determained by the input 'me'.
def get_move(me: int, array_board: "list[list[int]]"):
    array_board = np.array(array_board)
    board = Board(array_board)
    max_rating = float("-inf")
    valid_moves, lines = board.get_valid_moves(me)

    # if there is no valid move, the bot will never be called in the first place. For safety, we return an invalid result.
    if len(valid_moves) == 0:
        return

    ret = valid_moves[0]

    for move in valid_moves:
        board1 = board.copy()
        changes = board1.optimized_do_move(me, move[0], move[1], lines[move])
        rating = len(changes)
        for changed_i, changed_j in changes:
            rating += board1.get_basic_rate_for_move(changed_i, changed_j)
        rating += -0.75 * board1.get_rating(3 - me, 3, max_rating_for_use=-max_rating)

        if rating > max_rating:
            max_rating = rating
            ret = move

    return ret
