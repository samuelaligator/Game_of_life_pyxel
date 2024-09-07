import pyxel
import numpy as np

LIST_OFFSET = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

class GameOfLife:
    def __init__(self):
        pyxel.init(100, 100, "Game of Life", 15, pyxel.KEY_ESCAPE, 20)
        self.table = np.zeros((100, 100), dtype=int)
        self.mouse_x, self.mouse_y = 0, 0
        self.start = False
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_start()
        if not self.start:
            pyxel.mouse(True)
            self.update_mouse()
            self.update_click()
            self.update_random()
        else:
            pyxel.mouse(False)
            self.update_life()

    def draw(self):
        self.draw_table()

    def update_mouse(self):
        self.mouse_x, self.mouse_y = pyxel.mouse_x, pyxel.mouse_y

        self.mouse_x = min(self.mouse_x, 99)
        self.mouse_y = min(self.mouse_y, 99)

    def update_click(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.table[self.mouse_y, self.mouse_x] = not int(self.table[self.mouse_y, self.mouse_x])
            self.count_cells(self.mouse_y, self.mouse_x)

    def update_random(self):
        if pyxel.btn(pyxel.KEY_R):
            self.table = np.random.randint(2, size=(100, 100), dtype=int)

        if pyxel.btnp(pyxel.KEY_V):
            self.table = np.zeros((100, 100), dtype=int)

    def update_start(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start = not self.start


    def update_life(self):
        new_table = np.copy(self.table)

        for y in range(self.table.shape[1]):
            for x in range(self.table.shape[0]):
                living_cells_around = self.count_cells(x, y)

                if self.table[x, y] == 0 and living_cells_around == 3:
                    new_table[x, y] = 1

                elif self.table[x, y] == 1 and (living_cells_around < 2 or living_cells_around > 3):
                    new_table[x, y] = 0

        self.table = new_table

    def count_cells(self, x, y):
        living_cells_around = 0
        for offset_x, offset_y in LIST_OFFSET:
            final_x = (x + offset_x) % self.table.shape[0]
            final_y = (y + offset_y) % self.table.shape[1]

            living_cells_around += self.table[final_x, final_y]

        return living_cells_around

    def draw_table(self):
        for y in range(self.table.shape[1]):
            for x in range(self.table.shape[0]):
                pyxel.rect(y, x, 1, 1, int(self.table[x, y]))

GameOfLife()