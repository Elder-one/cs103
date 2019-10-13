from typing import Tuple, List, Set, Optional
from random import randint


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    result = []
    i = 0

    for _ in range(n):

        result.append([])

        for _1 in range(n):

            result[-1].append(values[i])
            i += 1

    return result


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    result = []

    for row in grid:
        result.append(row[pos[1]])

    return result


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos

    row = row // 3 * 3
    col = col // 3 * 3

    result = []

    for i in range(row, row + 3):

        for j in range(col, col + 3):

            result.append(grid[i][j])

    return result


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '.':
                return (i, j)

    return (-1, -1)


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    result = set()

    for ch in '123456789':
        if ch not in get_row(grid, pos):
            if ch not in get_col(grid, pos):
                if ch not in get_block(grid, pos):
                    result.add(ch)

    return result


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(grid)

    if empty_pos == (-1, -1):
        return grid

    values = find_possible_values(grid, empty_pos)

    if len(values) == 0:
        return

    row, col = empty_pos

    for value in values:

        grid[row][col] = value

        result = solve(grid)

        if result:
            return result

    grid[row][col] = '.'
    return #комментарий, чтобы закоммитить эту ф-цию



def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in range(9):
        for j in range(9):
            block = get_block(solution, (i, j))
            row = get_row(solution, (i, j))
            col = get_col(solution, (i, j))

            if len(block) > len(set(block)):
                return False

            if len(row) > len(set(row)):
                return False

            if len(col) > len(set(col)):
                return False

    return True


def transp(matrix):
    buff = []
    n = len(matrix)

    for i in range(n):
        buff.append([])
        for j in range(n):
            buff[i].append(matrix[j][i])

    return buff


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    base_grid = [[str((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)]

    for _ in range(40): #40 перетасовок

        choice  = randint(1, 5)

        if choice == 1: #транспонирование

            base_grid = transp(base_grid)

        elif choice == 2: #перемещение районов строк

            n1 = randint(0, 2)

            n2 = randint(0, 2)

            while n1 == n2:
                n2 = randint(0, 2)

            n1 *= 3
            n2 *= 3

            for i in range(3):
                base_grid[n1], base_grid[n2] = base_grid[n2], base_grid[n1]
                n1 += 1
                n2 += 1

        elif choice == 3: #перемещение районов столбцов

            base_grid = transp(base_grid)

            n1 = randint(0, 2) #поменять районы строк

            n2 = randint(0, 2)

            while n1 == n2:
                n2 = randint(0, 2)

            n1 *= 3
            n2 *= 3

            for i in range(3):
                base_grid[n1], base_grid[n2] = base_grid[n2], base_grid[n1]
                n1 += 1
                n2 += 1

            base_grid = transp(base_grid)

        elif choice == 4: #перемещение строк в пределах района

            n = randint(0, 2) #выбор района

            n1 = randint(0, 2)
            n2 = randint(0, 2)

            while n1 == n2:
                n2 = randint(0, 2)

            n1 += n*3
            n2 += n*3

            base_grid[n1], base_grid[n2] = base_grid[n2], base_grid[n1]

        else: #перемещение столбцов в пределах района

            base_grid = transp(base_grid)

            n = randint(0, 2) #выбор района

            n1 = randint(0, 2)
            n2 = randint(0, 2)

            while n1 == n2:
                n2 = randint(0, 2)

            n1 += n*3
            n2 += n*3

            base_grid[n1], base_grid[n2] = base_grid[n2], base_grid[n1]

            base_grid = transp(base_grid)

    forbiden = set()
    for _ in range(81-N):

        i = randint(0, 8)
        j = randint(0, 8)

        while (i, j) in forbiden:
            i = randint(0, 8)
            j = randint(0, 8)

        base_grid[i][j] = '.'

        forbiden.add((i, j))

    return base_grid

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
