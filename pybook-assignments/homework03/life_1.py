# coding: utf8
import pygame
from pygame.locals import *
import random
import abc
import curses


class GameOfLife:
    def __init__(self, size, randomize = True, max_gen = None):
        self.rows, self.cols = size
        self.prev_gen = self.create_grid()
        self.curr_gen = self.create_grid(randomize)
        self.max_gens = max_gen
        self.gens = 1

    def create_grid(self, randomize = False):
        k = self.cols
        m = self.rows
        if randomize:
            Grid = [[random.randint(0, 1) for _ in range(k)] for _1 in range(m)]
        else:
            Grid = [[0 for _ in range(k)] for _1 in range(m)]
        return Grid

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        k, m = self.cols, self.rows
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i >= 0 and i < m and j >= 0 and j < k:
                    if i != row or j != col:
                        neighbours.append(self.curr_gen[i][j])
        return neighbours

    def get_next_generation(self):
        k = self.cols
        m = self.rows
        new_gen = [[0 for _ in range(k)] for _1 in range(m)]
        for i in range(m):
            for j in range(k):
                n = sum(self.get_neighbours((i, j)))
                if self.curr_gen[i][j]:
                    if n in [2, 3]:
                        new_gen[i][j] = 1
                else:
                    if n == 3:
                        new_gen[i][j] = 1
        return new_gen

    def step(self):
        self.prev_gen = self.curr_gen
        self.curr_gen = self.get_next_generation()
        self.gens += 1

    @property
    def is_max_generations_exceeded(self):
        if self.max_gens:
            return self.gens >= self.max_gens
        else:
            return False

    @property
    def is_changing(self):
        return (self.prev_gen != self.get_next_generation())

    @staticmethod
    def from_file(fname):
        grid = []
        with open(fname, 'r') as file:
            for line in file:
                grid.append([int(c) for c in line if c in '01'])
        rows = len(grid)
        cols = len(grid[0])
        life = GameOfLife((rows, cols))
        life.curr_gen = grid
        return life

    def save(self, fname):
        with open(fname, 'w') as file:
            for i in range(self.rows):
                file.write(''.join(map(str, self.curr_gen[i]))+'\n'*int(i < self.rows-1))
            
        
class UI(abc.ABC):
    def __init__(self, life):
        self.life = life

    @abc.abstractmethod
    def run(self):
        pass


class GUI(UI):
    def __init__(self, life, cell_size=10, speed=10):
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols*cell_size
        self.height = self.life.rows*cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """
        a = self.cell_size
        for x in range(0, self.width, a):
            for y in range(0, self.height, a):
                i = x // a
                j = y // a
                color = "green" if clist[j][i] else "white"
                pygame.draw.rect(self.screen, pygame.Color(color), (x, y, a, a))
        self.draw_grid()

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Начальная отрисовка списка клеток
        self.draw_cell_list(self.life.curr_gen)

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.pause():
                            running = False
                            
            if running:
                self.life.step()
                self.draw_cell_list(self.life.curr_gen)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def pause(self):
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        flag = False
                if event.type == QUIT:
                        return 1
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    a = self.cell_size
                    x //= a
                    y //= a
                    k = self.life.curr_gen[y][x]
                    self.life.curr_gen[y][x] = 1-k
                    self.draw_cell_list(self.life.curr_gen)
                    pygame.display.flip()
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        self.life.save(input())


class Console(UI):
    def __init__(self, life):
        super().__init__(life)
        

    def draw_borders(self, screen):
        for i in range(self.life.rows+2):
            if i == 0 or i == self.life.rows+1:
                screen.addstr(i, 0, "*"+('-'*self.life.cols)+'*')
            else:
                screen.addstr(i, 0, "|"+(' '*self.life.cols)+"|")

    def draw_grid(self, screen):
        k = self.life.rows
        for y in range(k):
            s = ''.join(['.' if i else ' ' for i in self.life.curr_gen[y]])
            screen.addstr(y+1, 1, s)

    def run(self):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(1)
        self.draw_borders(screen)

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:

            if running:
                self.life.step()
                self.draw_grid(screen)
            screen.refresh()

        curses.echo()
        curses.nocbreak()
        screen.keypad(0)
        curses.endwin()


if __name__ == '__main__':
    game = GameOfLife((30, 64))
    Console(game).run()