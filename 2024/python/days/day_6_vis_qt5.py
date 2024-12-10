import sys
from time import sleep

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import QTimer, QRectF

from helpers import get_file_data

PIXEL_SIZE = 6
COLORS = {
    "DEFAULT": QColor("#555"),
    "GUARD": QColor("#f90"),
    "WALL": QColor("#f55"),
    "VISITED": QColor("#6f9"),
    "LOOP": QColor("#0ff")
}


def simulate(grid: dict, cur_pos, direction='^') -> tuple[list, dict]:
    TURN = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
    INCR = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
    main_path = []
    loop_paths = {}
    visited = set()

    def step(p, d):
        return p[0] + INCR[d][0], p[1] + INCR[d][1]

    def _has_loops(_grid: dict, _pos: tuple, _dir: str):
        _visited = set()

        while _pos in _grid:
            if (*_pos, _dir) in _visited:
                return [(_x, _y) for _x, _y, _ in _visited]

            _new_pos = step(_pos, _dir)

            if _grid.get(_new_pos) == '#':
                _dir = TURN.get(_dir)
                continue

            _visited.add((*_pos, _dir))
            _pos = _new_pos

        return []

    while cur_pos in grid:
        main_path.append((cur_pos, direction))
        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        _grid = {**grid, new_pos: '#'}
        loop_path = _has_loops(_grid, cur_pos, direction)
        if new_pos not in visited and loop_path:
            loop_paths[(cur_pos, direction)] = loop_path

        visited.add(cur_pos)
        cur_pos = new_pos

    return main_path, loop_paths


class GridAnimation(QGraphicsView):
    def __init__(self, data: list):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setWindowTitle("AoC 2024 Day6 Part2 Visualizer")
        self.setRenderHint(QPainter.Antialiasing)
        self.MW, self.MH = len(data[0]), len(data)
        self.setFixedSize(self.MW * PIXEL_SIZE + 4, self.MH * PIXEL_SIZE + 4)
        self.pixels = {}

        self.grid = {}
        for y in range(self.MH):
            for x in range(self.MW):
                value = data[y][x]
                self.grid[(x, y)] = value
                if value in "><^v":
                    self.cur_pos = (x, y)
                    self.direction = value

        self.main_path, self.loop_paths = simulate(self.grid, self.cur_pos, self.direction)
        self.path_idx = 0
        self.loop_drawn = False
        self.visited = set()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.draw_initial_grid()

    def draw_initial_grid(self):
        for y in range(self.MH):
            for x in range(self.MW):
                char = self.grid[(x, y)]
                color = COLORS["WALL"] if char == '#' else COLORS["DEFAULT"]
                self.add_pixel(x, y, color)

    def add_pixel(self, x, y, color):
        rect = QRectF(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        brush = QBrush(color)
        self.pixels[(x, y)] = self.scene.addRect(rect, brush=brush)

    def update_pixel(self, x, y, color):
        self.pixels[(x, y)].setBrush(QBrush(color))

    def tick(self):
        self.path_idx += 1
        if self.path_idx >= len(self.main_path):
            self.timer.stop()
            return

        prev_pos, direction = self.main_path[self.path_idx - 1]
        self.update_pixel(prev_pos[0], prev_pos[1], COLORS["VISITED"])
        self.visited.add(prev_pos)

        if self.loop_drawn:
            self.loop_drawn = False
            for x, y in self.loop_paths[(prev_pos, direction)]:
                if (x, y, direction) in self.loop_paths:
                    color = COLORS["LOOP"]
                elif (x, y) in self.visited:
                    color = COLORS["VISITED"]
                else:
                    color = COLORS["DEFAULT"]
                self.update_pixel(x, y, color)

        cur_pos, direction = self.main_path[self.path_idx]
        self.update_pixel(cur_pos[0], cur_pos[1], COLORS["GUARD"])

        if (cur_pos, direction) in self.loop_paths:
            self.loop_drawn = True
            for x, y in self.loop_paths[(cur_pos, direction)]:
                if (x, y) not in self.visited:  # just optimization to reduce amount of updated pixels
                    self.update_pixel(x, y, COLORS["LOOP"])


if __name__ == "__main__":
    grid_data = get_file_data('2024/python/inputs/day6', decode=True)

    app = QApplication(sys.argv)
    window = GridAnimation(grid_data)
    window.show()
    window.timer.start(8)
    sys.exit(app.exec_())
