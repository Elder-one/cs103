import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            if running:
                self.draw_grid()
                self.draw_lines()
                self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=True) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        k = self.cell_width
        m = self.cell_height
        if randomize:
            Grid = [[random.randint(0, 1) for _ in range(k)] for _1 in range(m)]
        else:
            Grid = [[0 for _ in range(k)] for _1 in range(m)]
        return Grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        a = self.cell_size
        for x in range(0, self.width, a):
            for y in range(0, self.height, a):
                i = x // a
                j = y // a
                color = "green" if self.grid[j][i] else "white"
                pygame.draw.rect(self.screen, pygame.Color(color), (x, y, a, a))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        row, col = cell
        k, m = self.cell_width, self.cell_height
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i >= 0 and i < m and j >= 0 and j < k:
                    if i != row or j != col:
                        neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        k = self.cell_width
        m = self.cell_height
        new_gen = [[0 for _ in range(k)] for _1 in range(m)]
        for i in range(m):
            for j in range(k):
                n = sum(self.get_neighbours((i, j)))
                if self.grid[i][j]:
                    if n in [2, 3]:
                        new_gen[i][j] = 1
                else:
                    if n == 3:
                        new_gen[i][j] = 1
        return new_gen


if __name__ == "__main__":
    GameOfLife().run()
