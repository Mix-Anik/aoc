import sys

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen, QFont
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtCore import Qt

from helpers import get_file_data

PIXEL_SIZE = 6
COLORS = {
    "BG": QColor("#222"),
    "DEFAULT": QColor("#111"),
    "GUARD": QColor("#f90"),
    "WALL": QColor("#a55"),
    "VISITED": QColor("#6f9"),
    "LOOP": QColor("#0ee")
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
            loop_paths[(cur_pos, direction)] = [x for x in loop_path if x not in visited]

        visited.add(cur_pos)
        cur_pos = new_pos

    return main_path, loop_paths


class GridAnimation(QGraphicsView):
    def __init__(self, data: list):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(COLORS['BG']))
        self.setScene(self.scene)
        self.setWindowTitle("AoC 2024 Day6 Part2 Visualizer")
        self.pen = QPen(COLORS['BG'])
        self.MW, self.MH = len(data[0]), len(data)
        self.setFixedSize(self.MW * PIXEL_SIZE + 4, self.MH * PIXEL_SIZE + 4 + 40)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.cycles_count = 0
        self.text_item = QGraphicsTextItem('Cycles Found: 0')
        self.text_item.setDefaultTextColor(COLORS['LOOP'])
        self.text_item.setFont(QFont("Arial", 16))
        self.text_item.setPos((self.MW * PIXEL_SIZE + 4) / 2 - 100, self.MH * PIXEL_SIZE + 4)
        self.scene.addItem(self.text_item)

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
        self.loops_visited = set()
        self.fading_pixels = {}
        self.drawn_loops = {}

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.draw_initial_grid()

        self.loops_timer = QTimer()
        self.loops_timer.timeout.connect(self.draw_loops)
        self.loops_timer.start(20)

        self.fading_timer = QTimer()
        self.fading_timer.timeout.connect(self.update_fading_pixels)
        self.fading_timer.start(20)

    def draw_initial_grid(self):
        for y in range(0, self.MH):
            for x in range(0, self.MW):
                char = self.grid[(x, y)]
                color = COLORS["WALL"] if char == '#' else COLORS["DEFAULT"]
                rect = QRectF(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                brush = QBrush(color)
                self.pixels[(x, y)] = self.scene.addRect(rect, brush=brush, pen=self.pen)

    def update_pixel(self, x, y, color):
        self.pixels[(x, y)].setBrush(QBrush(color))

    def tick(self):
        self.path_idx += 1
        if self.path_idx >= len(self.main_path):
            self.timer.stop()
            return

        prev_pos, direction = self.main_path[self.path_idx - 1]
        if prev_pos not in self.visited:
            self.visited.add(prev_pos)

        cur_pos, direction = self.main_path[self.path_idx]
        if cur_pos not in self.visited and cur_pos not in self.loops_visited:
            self.update_pixel(cur_pos[0], cur_pos[1], COLORS["VISITED"])
            self.fading_pixels[cur_pos] = (COLORS["VISITED"], 10)

        if (cur_pos, direction) in self.loop_paths:
            self.drawn_loops[(cur_pos, direction)] = (self.loop_paths[(cur_pos, direction)], COLORS["LOOP"], 4)
            self.loops_visited.add(cur_pos)

            # if cur_pos in self.fading_pixels:
            #     del self.fading_pixels[cur_pos]
            #
            # self.update_pixel(cur_pos[0], cur_pos[1], COLORS["LOOP"])
            self.cycles_count += 1
            self.text_item.setPlainText(f'Cycles Found: {self.cycles_count}')

    def update_fading_pixels(self):
        to_remove = []
        for (x, y), (color, steps) in self.fading_pixels.items():
            if steps <= 0:
                to_remove.append((x, y))
                self.visited.add((x, y))
                continue
            faded_color = color.darker(factor=115)
            self.pixels[(x, y)].setBrush(QBrush(faded_color))
            self.fading_pixels[(x, y)] = (faded_color, steps - 1)
        for key in to_remove:
            del self.fading_pixels[key]

    def draw_loops(self):
        to_remove = []
        for key, (path, color, steps) in self.drawn_loops.items():
            if steps <= 0:
                to_remove.append(key)
                continue

            faded_color = COLORS['DEFAULT'] if steps == 1 else color.darker(factor=115)
            for x, y in path:
                if (x, y) in self.loops_visited:
                    continue
                self.pixels[(x, y)].setBrush(QBrush(faded_color))
            self.drawn_loops[key] = (path, faded_color, steps - 1)
        for key in to_remove:
            del self.drawn_loops[key]


if __name__ == "__main__":
    grid_data = get_file_data('2024/python/inputs/day6', decode=True)

    app = QApplication(sys.argv)
    window = GridAnimation(grid_data)
    window.show()
    window.timer.start(8)
    sys.exit(app.exec_())
