import pygame
import requests

width = 550
bc = (30,50,40)
ec = (153,204,155)
buffer = 5
api_endpoint = 'https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}'
response = requests.get(api_endpoint)
grid = response.json()['newboard']['grids'][0]['value']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def draw_grid(win, myfont):
    win.fill(bc)
    for i in range(0, 10):
        if (i % 3 == 0):
            pygame.draw.line(win, (251, 251, 251), (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, (251, 251, 251), (50, 50 + 50 * i), (500, 50 + 50 * i), 6)

        pygame.draw.line(win, (251, 251, 251), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (251, 251, 251), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (0 < grid[i][j] < 10):
                value = myfont.render(str(grid[i][j]), True, ec)
                win.blit(value, ((j + 1) * 50 + 21, (i + 1) * 50 + 15))
    pygame.display.update()

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # Puzzle solved
    row, col = empty_cell

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True  # If puzzle is solved with the current num
            board[row][col] = 0  # Backtrack if current num doesn't lead to a solution

    return False  # No number from 1 to 9 can be placed in this cell

def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

def is_safe(board, row, col, num):
    # Check if num is not present in current row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if num is not present in current 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def main():
    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Sudoku")
    myfont = pygame.font.SysFont('Roboto', 37)

    draw_grid(win, myfont)

    solve_button_rect = pygame.Rect(50, 510, 100, 35)
    solve_button_color = (0, 0, 0)

    solve_button_text = myfont.render("Solve", True, ec)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if solve_button_rect.collidepoint(mouse_x, mouse_y):
                    solve_sudoku(grid)
                    draw_grid(win, myfont)

        pygame.draw.rect(win, solve_button_color, solve_button_rect)
        win.blit(solve_button_text, (solve_button_rect.x + 14, solve_button_rect.y + 10))

        pygame.display.update()

main()
