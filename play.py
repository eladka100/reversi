import reversiBot

bot = reversiBot.get_move

board = reversiBot.Board([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
while any(0 in l for l in board.lst):
    i, j = bot(1, board.lst)
    board.optimized_do_move(1, i, j, board.get_valid_moves(1)[1][(i, j)])
    print(board)
    i, j = map(int, input().split(","))
    board.optimized_do_move(2, i, j, board.get_valid_moves(2)[1][(i, j)])
    print(board)
