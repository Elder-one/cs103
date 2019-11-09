import pygame
from pygame.locals import *
import pathlib

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols*cell_size
        self.height = self.life.rows*cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)


    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        a = self.cell_size
        for x in range(0, self.width, a):
            for y in range(0, self.height, a):
                i = x // a
                j = y // a
                color = "green" if self.life.curr_generation[j][i] else "white"
                pygame.draw.rect(self.screen, pygame.Color(color), (x, y, a, a))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Начальная отрисовка списка клеток
        self.draw_grid()
        self.draw_lines()

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.pause():
                            running = False
                            
            if running:
                self.life.step()
                self.draw_grid()
                self.draw_lines()

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
                    self.change_status(event.pos)
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        self.life.save(pathlib.Path(input("path --> ")))

    def change_status(self, pos):
        x, y = pos
        a = self.cell_size
        x //= a
        y //= a
        k = self.life.curr_generation[y][x]
        self.life.curr_generation[y][x] = 1-k
        self.draw_grid()
        self.draw_lines()
        pygame.display.flip()

if __name__ == "__main__":
    GUI(GameOfLife((48, 64))).run()
