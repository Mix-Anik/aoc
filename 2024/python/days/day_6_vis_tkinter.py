import tkinter as tk

from helpers import get_file_data


class C:
    DEFAULT = '#555'
    GUARD = '#f90'
    WALL = '#f55'
    VISITED = '#6f9'
    LOOP = '#0ff'

APP = tk.Tk()
CANVAS = tk.Canvas(APP, bg="#222", height=780, width=780, highlightthickness=0)
CANVAS.pack()
CGRID = {}
PIXEL_SIZE = 5

TURN = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
INCR = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
step = lambda p, d: tuple(map(sum, zip(p, INCR.get(d))))
data = get_file_data('2024/python/inputs/day6', decode=True)
MW, MH = len(data), len(data[0])
grid = {(x, y): data[y][x] for y in range(MH) for x in range(MW)}
cur_pos, direction = [(pos, val) for pos, val in grid.items() if val in '><^v'][0]
visited = set()

main_path = []
loop_positions = set()
PATH_IDX = 0
LOOP_DRAWN = False


def has_loops(grid: dict, pos: tuple, _direction: str):
    cur_pos = pos
    direction = _direction
    visited = set()

    while cur_pos in grid:
        if (*cur_pos, direction) in visited:
            return True

        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        visited.add((*cur_pos, direction))
        cur_pos = new_pos

    return False


def simulate():
    global cur_pos, direction, CANVAS, CGRID, loop_positions

    while cur_pos in grid:
        main_path.append(cur_pos)
        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        _grid = {**grid, new_pos: '#'}
        if new_pos not in visited and has_loops(_grid, cur_pos, direction):
            loop_positions.add(cur_pos)

        visited.add(cur_pos)
        cur_pos = new_pos


def tick(event=None):
    global PATH_IDX, LOOP_DRAWN, loop_positions

    PATH_IDX += 1
    if PATH_IDX >= len(main_path):
        return

    prev_pos = main_path[PATH_IDX-1]
    visited_color = C.LOOP if prev_pos in loop_positions else C.VISITED
    CANVAS.itemconfig(CGRID[prev_pos], fill=visited_color)
    pos = main_path[PATH_IDX]
    CANVAS.itemconfig(CGRID[pos], fill=C.GUARD)

    CANVAS.after(2, tick)


if __name__ == '__main__':
    simulate()

    for y in range(MH + 1):
        for x in range(MW + 1):
            x_shift = x * PIXEL_SIZE
            y_shift = y * PIXEL_SIZE
            fill = C.WALL if grid.get((x, y)) == '#' else C.DEFAULT
            CGRID[(x, y)] = CANVAS.create_rectangle(x+x_shift,
                                                          y+y_shift,
                                                          x+PIXEL_SIZE+x_shift,
                                                          y+PIXEL_SIZE+y_shift,
                                                          fill=fill, outline='')

    CANVAS.bind("<Button-1>", tick)
    CANVAS.itemconfig(CGRID[cur_pos], fill=C.GUARD)

    APP.mainloop()
