import reversiBot

bot = reversiBot.get_move

board = reversiBot.Board()
#FIXME: doesn't works with the new optimized systems
while any(0 in l for l in board.lst):
    board.do_move(1, *bot(1, board.lst))
    print(board)
    board.do_move(2, *map(int, input().split(",")))
    print(board)
