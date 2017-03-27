import itertools as it
import random
import numpy as np

_words = open('b.txt').read().split('\n')

def get_words_of_length(l):
    for i in _words:
        if len(i) == l:
            yield i

words = {l: list(get_words_of_length(l)) for l in range(10)}

def get_word(l):
    return random.choice(words[l])

def get_words(*lengths):
    return [get_word(l) for l in lengths]

def get_neighbor_loc(x, y):
    return it.starmap(lambda a, b: (x+a, y+b), \
                      it.product([0, -1, 1], [0, -1, 1]))

def filter_neighbor_loc(x, y, maxx, maxy, minx, miny):
    for i in get_neighbor_loc(x, y):
        if i[0] < maxx and \
           i[1] < maxy and \
           i[0] > minx and \
           i[1] > miny and \
           i != (x, y):
            yield i

def extend(board, place):
    return filter_neighbor_loc(*place, len(board[0]), len(board), -1, -1)

def place_extend(board, x, y, word, index):
    letter = word[index]
    for ext in extend(board, (x, y)):
        a, b = ext
        nb = [[j[:] for j in i] for i in board[:]]
        if nb[b][a] == ' ':
            nb[b][a] = letter
            if index != len(word) - 1:
                yield from place_extend(nb, a, b, word, index + 1)
            else:
                yield nb

def place_word(board, word, loc):
    x, y = loc
    yield from place_extend(board, x, y, word, 0)

def join_tables(*tables):
    joinedTable = [i[:] for i in tables[0]]
    for table in tables[1:]:
        for ri, row in enumerate(table):
            for ci, col in enumerate(row):
                if joinedTable[ri][ci] == ' ' and col != ' ':
                    joinedTable[ri][ci] = col
                else:
                    return
    return joinedTable
    
def explicitly_join(*tables):
    w = len(tables[0][0])
    h = len(tables[0])
    joinedTable = np.copy(tables[0]).tolist()
    print(joinedTable)
    print()
    for table in tables[1:]:
        print(table)
        for ri, row in enumerate(table):
            print(ri, row)
            for ci, col in enumerate(row):
                print('\t', ri, row)
##        for (ri, ci), col in np.ndenumerate(table):
##            print(ri, ci, col)
##            col = row[ci]
##            print(ri, row)
##            print(ci, col)
                if joinedTable[ri][ci] == ' ' and col != ' ':
                    print('\t\tjoining', ri, ci, col, joinedTable[ri][ci])
                    print(joinedTable)
                    joinedTable[ri][ci] = col
                    print(joinedTable)
                else:
                    return False, joinedTable
        return True, joinedTable

def get_board(w, h, *lengths):
    board = np.repeat([[' '] * w], h, axis = 0).tolist()
    words = get_words(*lengths)
    print(words)
    boards = []
    for index,length in enumerate(lengths):
        boards.append([])
        for i in range(h):
            for j in range(w):
                boards[-1].extend(list(place_word(board, words[index], (i, j))))
    for boardl in it.combinations(boards, 2):
        for match in it.product(*boardl):
            joined = join_tables(match)
            if joined is not None:
                return joined
                    
for i in get_board(5, 5, 5, 5):
##    print(i)
    print('\n'.join(str(j) for j in i))
##                a=0
##                l = []
##                for j in i:
##                    l.append(boards[a][j])
##                    a += 1
