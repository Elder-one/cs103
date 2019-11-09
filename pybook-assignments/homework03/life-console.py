import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        for i in range(self.life.rows+2):
            if i == 0 or i == self.life.rows+1:
                screen.addstr(i, 0, "*"+('-'*self.life.cols)+'*')
            else:
                screen.addstr(i, 0, "|"+(' '*self.life.cols)+"|")

    def draw_grid(self, screen) -> None:
        k = self.life.rows
        for y in range(k):
            s = ''.join(['.' if i else ' ' for i in self.life.curr_generation[y]])
            screen.addstr(y+1, 1, s)

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:

            if running:
                self.life.step()
                self.draw_grid(screen)
            screen.refresh()

        curses.endwin()


if __name__ == "__main__":
    Console(GameOfLife((40, 64))).run()
