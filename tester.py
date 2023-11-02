import reversiBot, basicBot, time, stableBot
bot1 = reversiBot.get_move
bot1_color = 1
bot1_total_time = 0
bot1_max_time = 0
bot1_total_moves = 0
bot1_wins = 0

bot2 = stableBot.get_move
bot2_color = 2
bot2_total_time = 0
bot2_max_time = 0
bot2_total_moves = 0
bot2_wins = 0

starting_boards = [
[   
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
],
[
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
],
[
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
],
[
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
]

turns = 0
for start in starting_boards:
    board = reversiBot.Board(start)

    while any(0 in l for l in board.lst):
        if len(board.get_valid_moves(bot1_color)) != 0:
            t1 = time.perf_counter()
            board.do_move(bot1_color, *bot1(bot1_color, board.lst))
            t2 = time.perf_counter()
            turns += 1
            bot1_total_time += t2 - t1
            bot1_max_time = max(bot1_max_time, t2 - t1)
            bot1_total_moves += 1  
        else:
            break    
        print(board)
        if len(board.get_valid_moves(bot2_color)) != 0:
            t1 = time.perf_counter()
            board.do_move(bot2_color, *bot2(bot2_color, board.lst))
            t2 = time.perf_counter()
            turns += 1
            bot2_total_time += t2 - t1
            bot2_max_time = max(bot2_max_time, t2 - t1)
            bot2_total_moves += 1 
        else:
            break      
        print(board)

    if board.get_score(bot1_color) > 0:
        bot1_wins += 1
    else:
        bot2_wins += 1

    print(f"score bot1: {board.get_score(bot1_color)}")
    print(f"score bot2: {board.get_score(bot2_color)}")

    print(f"bot1 average time: {round(bot1_total_time / bot1_total_moves, 4)}")
    print(f"bot2 average time: {round(bot2_total_time / bot2_total_moves, 4)}")



    while any(0 in l for l in board.lst):
        if len(board.get_valid_moves(bot2_color)) != 0:
            t1 = time.perf_counter()
            board.do_move(bot2_color, *bot2(bot2_color, board.lst))
            t2 = time.perf_counter()
            turns += 1
            bot2_total_time += t2 - t1
            bot2_total_moves += 1
        else:
            break  
        print(board)
        if len(board.get_valid_moves(bot1_color)) != 0:
            t1 = time.perf_counter()
            board.do_move(bot1_color, *bot1(bot1_color, board.lst))
            t2 = time.perf_counter()
            turns += 1
            bot1_total_time += t2 - t1
            bot1_total_moves += 1
        else:
            break
        print(board)
        
    if board.get_score(bot1_color) > 0:
        bot1_wins += 1
    else:
        bot2_wins += 1

    print(f"score bot1: {board.get_score(bot1_color)}")
    print(f"score bot2: {board.get_score(bot2_color)}")

    print(f"bot1 average time: {round(bot1_total_time / bot1_total_moves, 4)}")
    print(f"bot1 max time: {bot1_max_time}")
    print(f"bot2 average time: {round(bot2_total_time / bot2_total_moves, 4)}")
    print(f"bot2 max time: {bot2_max_time}")

print(f"bot1_wins: {bot1_wins}")
print(f"bot2_wins: {bot2_wins}")
