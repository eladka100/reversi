import numpy
import reversiBot

bot = reversiBot.get_move

nplist_board = numpy.array([   
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])
board = reversiBot.Board(nplist_board)

#FIXME: doesn't works with the new optimized systems nor with numpy arrays

board = reversiBot.Board()
while any(0 in l for l in board.lst):
    board.do_move(1, *bot(1, board.lst))
    print(board)
    board.do_move(2, *map(int, input().split(",")))
    print(board)
