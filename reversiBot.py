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
    
    def __hash__(self) -> int:
        return hash(tuple(map(tuple, self.lst)))
    
    def __eq__(self, other) -> bool:
        return self.lst == other.lst

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
    # the cache contains a Board as a key and (int, float) as value
    # if the int is 0 then the eval is the number, if it is 1 then the eval is bigger then or equal to the number and if it is 2 then the eval is less then or equal to the number
    # a potential problem is if the value in the cache is evaluated with less depth but this is rare so I did not include a check for it
    def get_rating(self, me: int, depth: int, cache: dict, min_rating_for_use: float=float("-inf"), max_rating_for_use: float=float("inf")) -> float:
        board_cache = cache.get(self, None)
        if board_cache is not None:
            if board_cache[0] == 0:
                return board_cache[1]
            if board_cache[0] == 1:
                if board_cache[1] >= max_rating_for_use:
                    return board_cache[1]
                if board_cache[1] > min_rating_for_use:
                    min_rating_for_use = board_cache[1] - 0.01
            else:
                if board_cache[1] <= min_rating_for_use:
                    return board_cache[1]
                if board_cache[1] < max_rating_for_use:
                    max_rating_for_use = board_cache[1] + 0.01

        if depth == 0:
            # base evaluation
            return 0

        valid_moves, lines = self.get_valid_moves(me)
        enemy = 3 - me

        if len(valid_moves) == 0:
            if len(self.get_valid_moves(enemy)) == 0:
                return float("inf") if self.get_score(me) > 0 else float("-inf") # the game is over
            
            return -0.75 * self.get_rating(enemy, depth-1, cache, -max_rating_for_use, -min_rating_for_use) # skip me's turn

        max_rating = min_rating_for_use

        for i, j in valid_moves:
            new_board = self.copy()
            changes = new_board.optimized_do_move(me, i, j, lines[(i, j)])
            current_rating = len(changes)
            for changed_i, changed_j in changes:
                current_rating += new_board.get_basic_rate_for_move(changed_i, changed_j)
            # max_rating_for_use calculation
            # this equation must be true for this move to be used:
            # current_rating - 3/4 * get_rating > max_rating
            # get_rating < (current_rating - max_rating) * 4/3
            # so the new max_rating_for_use is (current_rating - max_rating) * 4/3

            # min_rating_for_use calculation
            # this equation must be true for this move to be used:
            # max_rating_for_use > max_rating >= current_rating - 3/4 * get_rating
            # get_rating > (current_rating - max_rating_for_use) * 4/3
            # so the new min_rating_for_use is (current_rating - max_rating_for_use) * 4/3
            current_rating -= 0.75 * new_board.get_rating(enemy, depth - 1, cache, (current_rating - max_rating_for_use) * 4/3, (current_rating - max_rating) * 4/3)

            if current_rating > max_rating:
                max_rating = current_rating
            
            if max_rating_for_use <= max_rating:
                cache[self] = (1, max_rating_for_use)
                return max_rating # if this is reached this move will not be played

        if max_rating <= min_rating_for_use:
            cache[self] = (2, min_rating_for_use)
        else:
            cache[self] = (0, min_rating_for_use)

        return max_rating
    
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

    def get_valid_moves(self, me: int) -> "tuple[list[tuple[int, int]], dict[tuple[int, int], list[int]]]":
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
                changes.append((current_i, current_j))
                current_i += di
                current_j += dj
        return changes


def compute_direction(k) -> "tuple[int, int]":
        if k < 4:
            return k % 3 - 1, k // 3 - 1
        return (k + 1) % 3 - 1, (k + 1) // 3 - 1

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
        current_rating = len(changes)
        for changed_i, changed_j in changes:
            current_rating += board1.get_basic_rate_for_move(changed_i, changed_j)

        # max_rating_for_use calculation
        # this equation must be true for this move to be used:
        # current_rating - 3/4 * get_rating > max_rating
        # get_rating < (current_rating - max_rating) * 4/3
        # so the new max_rating_for_use is (current_rating - max_rating) * 4/3
        current_rating -= 0.75 * board1.get_rating(3 - me, 3, dict(), max_rating_for_use=(current_rating - max_rating) * 4/3)

        if current_rating > max_rating:
            max_rating = current_rating
            ret = move

    return ret
