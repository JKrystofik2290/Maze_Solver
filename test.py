def solve_maze(maze, y, x, sol):
    N = len(maze) - 1
    # at end of maze?
    if x == N and y == N and maze[y][x] == 1:
        sol[y][x] = 1
        return True

    # is current spot valid?
    if x >= 0 and x <= N and y >= 0 and y <= N and maze[y][x] == 1 and sol[y][x] != 1:
        sol[y][x] = 1

        # check if x+1 is valid
        if solve_maze(maze, y, x+1, sol):
            return True

        # check if x-1 is valid
        if solve_maze(maze, y, x-1, sol):
            return True

        # check if y+1 is valid
        if solve_maze(maze, y+1, x, sol):
            return True

        # check if y-1 is valid
        if solve_maze(maze, y-1, x, sol):
            return True

        # set current spot to not valid
        sol[y][x] = 0
        return False

    return False



maze = [[1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1]]

sol =  [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

print(solve_maze(maze, 0, 0, sol))
print(sol)
