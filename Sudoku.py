def flatten_lst(alist):
    if alist == []:
        return alist
    if isinstance(alist[0], list):
        return flatten_lst(alist[0]) + flatten_lst(alist[1:])
    return alist[:1] + flatten_lst(alist[1:])


def sudoku(grid):
    def get_row(i):
        return grid[i]
    
    def get_other_rows(i, flatten=False):
        a, b = i // 3, i % 3
        if b == 0:
            if flatten:
                return grid[a*3 + 1] + grid[a*3 + 2]
            return [grid[a*3 + 1], grid[a*3 + 2]]
        if b == 1:
            if flatten:
                return grid[a*3] + grid[a*3 + 2]
            return [grid[a*3], grid[a*3 + 2]]
        if b == 2:
            if flatten:
                return grid[a*3] + grid[a*3 + 1]
            return [grid[a*3], grid[a*3 + 1]]
    
    def get_2_row(i, j):
        b =  j % 3
        if b == 0:
            return [grid[i][j+1], grid[i][j+2]]
        if b == 1:
            return [grid[i][j-1], grid[i][j+1]]
        if b == 2:
            return [grid[i][j-2], grid[i][j-1]]
    
    def get_col(j):
        return list(map(lambda row: row[j], grid))
    
    def get_other_cols(j, flatten=False):
        a, b = j // 3, j % 3
        if b == 0:
            if flatten:
                return get_col(a*3+1) + get_col(a*3+2)
            return [get_col(a*3+1), get_col(a*3+2)]
        if b == 1:
            if flatten:
                return get_col(a*3) + get_col(a*3+2)
            return [get_col(a*3), get_col(a*3+2)]
        if b == 2:
            if flatten:
                return get_col(a*3) + get_col(a*3+1)
            return [get_col(a*3), get_col(a*3+1)]
    
    def get_2_col(i, j):
        b =  i % 3
        if b == 0:
            return [grid[i+1][j], grid[i+2][j]]
        if b == 1:
            return [grid[i-1][j], grid[i+1][j]]
        if b == 2:
            return [grid[i-2][j], grid[i-1][j]]
    
    def get_square(i, j, flatten=False):
        rows = grid[(i // 3)*3:(i // 3)*3 + 3]
        if flatten:
            return flatten_lst(list(map( lambda row: row[(j // 3)*3:(j // 3)*3 + 3], rows)))
        return list(map( lambda row: row[(j // 3)*3:(j // 3)*3 + 3], rows))
    
    def check_col(i,j, n, a):
        b = [0, 1, 2]
        x = b.pop(i%3)
        if get_other_cols(j)[n][(i//3)*3 + x] == 0:
            return False
        if not 0 in get_other_cols(j)[n][(i//3)*3:(i//3)*3 + 3]:
            return True
        if (get_other_cols(j)[n][(i//3)*3 + b[0]] == 0) and (get_other_cols(j)[n][(i//3)*3 + b[1]] != 0):
            if a in get_row((i//3)*3 + b[0]):
                return True
        if (get_other_cols(j)[n][(i//3)*3 + b[1]] == 0) and (get_other_cols(j)[n][(i//3)*3 + b[0]] != 0):
            if a in get_row((i//3)*3 + b[1]):
                return True
        if (get_other_cols(j)[n][(i//3)*3 + b[0]] == 0) and (get_other_cols(j)[n][(i//3)*3 + b[1]] == 0):
            if (a in get_row((i//3)*3 + b[0])) and (a in get_row((i//3)*3 + b[1])):
                return True
        return False
    
    def check_row(i, j, n, a):
        b = [0, 1, 2]
        x = b.pop(j%3)
        if get_other_rows(i)[n][(j//3)*3 + x] == 0:
            return False
        if not 0 in get_other_rows(i)[n][(j//3)*3:(j//3)*3 + 3]:
            return True
        if (get_other_rows(i)[n][(j//3)*3 + b[0]] == 0) and (get_other_rows(i)[n][(j//3)*3 + b[1]] != 0):
            if a in get_col((j//3)*3 + b[0]):
                return True
        if (get_other_rows(i)[n][(j//3)*3 + b[1]] == 0) and get_other_rows(i)[n][(j//3)*3 + b[0]] != 0:
            if a in get_col((j//3)*3 + b[1]):
                return True
        if (get_other_rows(i)[n][(j//3)*3 + b[0]] == 0) and (get_other_rows(i)[n][(j//3)*3 + b[1]] == 0):
            if (a in get_col((j//3)*3 + b[0])) and (a in get_col((j//3)*3 + b[1])):
                return True
        return False
        
    
    Not_Done = True
    while Not_Done:
        Not_Done = False
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    Not_Done = True
                else: 
                    continue
                for a in range(1, 10):
                    if not(a in get_square(i, j, flatten=True)) and not(a in get_row(i)) and not(a in get_col(j)):    # general condition -> check square, row and column
                        
                        if ( not 0 in get_row(i)[:j] + get_row(i)[j+1:] ) and (not a in get_row(i)):   # row full with no a
                            grid[i][j] = a
                            break
                        
                        if ( not 0 in get_col(j)[:i] + get_col(j)[i+1:] ) and (not a in get_col(j)):   # col full with no a
                            grid[i][j] = a
                            break
                        
                        if not 0 in get_square(i, j, flatten=True)[:(i//3)*3+(j//3)] + get_square(i, j, flatten=True)[(i//3)*3+(j//3)+1:]:  # square full with no a
                            grid[i][j] = a
                            break
                        
                        if (( a in get_other_cols(j)[0] ) and ( a in get_other_cols(j)[1] )) or \
                           (( check_col(i, j, 0, a)) and ( check_col(i, j, 1, a) )) or \
                           (( a in get_other_cols(j)[0] ) and ( check_col(i, j, 1, a) )) or \
                           (( check_col(i, j, 0, a) ) and ( a in get_other_cols(j)[1] )):
                               
                            if (not 0 in get_2_col(i, j)): 
                                grid[i][j] = a
                                break
                            elif ( a in get_other_rows(i)[0] ) and ( a in get_other_rows(i)[1] ):
                                grid[i][j] = a
                                break
                            elif (get_2_col(i, j)[0] != 0) and ( a in get_other_rows(i)[1] ):
                                grid[i][j] = a
                                break
                            elif (get_2_col(i, j)[1] != 0) and ( a in get_other_rows(i)[0] ):
                                grid[i][j] = a
                                break
                        
                        if (( a in get_other_rows(i)[0] ) and ( a in get_other_rows(i)[1] )) or \
                           (( check_row(i, j, 0, a) ) and ( check_row(i, j, 1, a) )) or \
                           ( ( a in get_other_rows(i)[0] ) and ( check_row(i, j, 1, a) )) or \
                           ( ( check_row(i, j, 0, a) ) and ( a in get_other_rows(i)[1] )):
                                
                            if (not 0 in get_2_row(i, j)): 
                                grid[i][j] = a
                                break
                            elif ( a in get_other_cols(j)[0] ) and ( a in get_other_cols(j)[1] ):
                                grid[i][j] = a
                                break
                            elif (get_2_row(i, j)[0] != 0) and ( a in get_other_cols(j)[1] ):
                                grid[i][j] = a
                                break
                            elif (get_2_row(i, j)[1] != 0) and ( a in get_other_cols(j)[0] ):
                                grid[i][j] = a
                                break
                            
                        
    
    return str(grid).replace("],", "]\n")


l = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]

l1 = [[0, 0, 0, 3, 0, 7, 4, 0, 0],
     [9, 0, 0, 0, 0, 4, 0, 0, 8],
     [3, 7, 0, 0, 0, 0, 0, 6, 0],
     [8, 2, 0, 9, 0, 0, 6, 0, 0],
     [0, 0, 1, 2, 0, 0, 9, 0, 4],
     [0, 4, 0, 0, 3, 8, 0, 5, 0],
     [2, 0, 8, 6, 9, 0, 7, 0, 0],
     [0, 9, 0, 0, 0, 0, 0, 0, 0],
     [7, 5, 0, 0, 0, 0, 0, 0, 6]
     ]

l2 =[[0, 0, 0, 0, 0, 5, 4, 0, 9],
     [4, 5, 1, 0, 0, 2, 3, 0, 0],
     [9, 8, 2, 0, 0, 0, 5, 6, 1],
     [6, 0, 7, 0, 0, 0, 9, 8, 0],
     [0, 0, 3, 4, 6, 0, 0, 0, 0],
     [5, 0, 0, 2, 8, 7, 0, 1, 0],
     [0, 4, 0, 0, 7, 0, 0, 9, 6],
     [3, 0, 0, 0, 0, 0, 7, 0, 0],
     [0, 0, 5, 9, 4, 6, 8, 0, 2]
     ]

l3 =[[4, 2, 7, 1, 0, 0, 0, 6, 8],
     [0, 0, 5, 0, 0, 6, 3, 0, 0],
     [6, 0, 3, 0, 0, 0, 1, 0, 0],
     [2, 0, 0, 0, 1, 0, 4, 0, 0],
     [3, 4, 0, 0, 6, 7, 0, 5, 1],
     [8, 0, 1, 0, 5, 0, 0, 2, 0],
     [0, 9, 0, 0, 0, 0, 7, 3, 0],
     [7, 0, 4, 3, 0, 0, 2, 0, 9],
     [0, 3, 2, 0, 9, 4, 6, 0, 0]
     ]

l4 =[[0, 6, 0, 0, 8, 0, 4, 2, 0],
     [0, 1, 5, 0, 6, 0, 3, 7, 8],
     [0, 0, 0, 4, 0, 0, 0, 6, 0],
     [1, 0, 0, 6, 0, 4, 8, 3, 0],
     [3, 0, 6, 0, 1, 0, 7, 0, 5],
     [0, 8, 0, 3, 5, 0, 0, 0, 0],
     [8, 3, 0, 9, 4, 0, 0, 0, 0],
     [0, 7, 2, 1, 3, 0, 9, 0, 0],
     [0, 0, 9, 0, 2, 0, 6, 1, 0]
     ]


print(sudoku(l4), sep='\n')

print()