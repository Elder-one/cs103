import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        k = self.cols
        m = self.rows
        if randomize:
            Grid = [[random.randint(0, 1) for _ in range(k)] for _1 in range(m)]
        else:
            Grid = [[0 for _ in range(k)] for _1 in range(m)]
        return Grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell
        k, m = self.cols, self.rows
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i >= 0 and i < m and j >= 0 and j < k:
                    if i != row or j != col:
                        neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        k = self.cols
        m = self.rows
        new_gen = [[0 for _ in range(k)] for _1 in range(m)]
        for i in range(m):
            for j in range(k):
                n = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j]:
                    if n in [2, 3]:
                        new_gen[i][j] = 1
                else:
                    if n == 3:
                        new_gen[i][j] = 1
        return new_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return (self.prev_generation != self.get_next_generation())


    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, 'r') as file:
            for line in file:
                grid.append([int(c) for c in line if c in '01'])
        rows = len(grid)
        cols = len(grid[0])
        life = GameOfLife((rows, cols))
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as file:
            for i in range(self.rows):
                file.write(''.join(map(str, self.curr_generation[i]))+'\n'*int(i < self.rows-1))
