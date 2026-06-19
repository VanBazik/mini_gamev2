import tkinter as tk
from tkinter import messagebox
import random

# --------------------- Главное меню ---------------------
class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Мини-игры")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Выберите игру", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Крестики-нолики", width=20,
                  command=self.run_tic_tac_toe).pack(pady=5)
        tk.Button(self.root, text="Шашки", width=20,
                  command=self.run_checkers).pack(pady=5)
        tk.Button(self.root, text="Сапёр", width=20,
                  command=self.run_minesweeper).pack(pady=5)

        self.root.mainloop()

    def run_tic_tac_toe(self):
        self.root.destroy()
        TicTacToe()

    def run_checkers(self):
        self.root.destroy()
        Checkers()

    def run_minesweeper(self):
        self.root.destroy()
        MineSweeper()

# --------------------- Крестики-нолики ---------------------
class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.resizable(False, False)

        self.current_player = "X"
        self.board = [[""] * 3 for _ in range(3)]
        self.buttons = [[None] * 3 for _ in range(3)]

        self.create_board()
        self.window.mainloop()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

    def make_move(self, row, col):
        if self.board[row][col] == "" and self.current_player:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_win(self.current_player):
                messagebox.showinfo("Игра окончена", f"Победил {self.current_player}!")
                self.reset_board()
                return
            elif self.is_draw():
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset_board()
                return

            self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_board(self):
        self.board = [[""] * 3 for _ in range(3)]
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

# --------------------- Шашки ---------------------
class Checkers:
    SIZE = 8
    EMPTY = 0
    WHITE = 1
    BLACK = -1

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Шашки")
        self.window.resizable(False, False)

        self.cell_size = 60
        self.board = [[self.EMPTY] * self.SIZE for _ in range(self.SIZE)]
        self.dame = [[False] * self.SIZE for _ in range(self.SIZE)]
        self.current_player = self.WHITE
        self.selected = None
        self.valid_moves = []

        self.init_board()
        self.canvas = tk.Canvas(self.window, width=self.SIZE * self.cell_size,
                                height=self.SIZE * self.cell_size, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.window.mainloop()

    def init_broad(self):
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.broad[row][col] = self.BLACK
                        self.dame[row][col] = False
                    elif row > 4:
                        self.broad[row][col] = self.WHITE
                        self.dame[tow][col] = False
                    else:
                        self.broad[row][col] = self.EMPTY
                        self.dame[row][col] = False

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.board[row][col] != self.EMPTY:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    radius = self.cell_size // 2 - 8
                    color = "white" if self.board[row][col] == self.WHITE else "black"
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                            fill=color, outline="gray", width=2)
                    if self.dame[row][col]:
                        self.canvas.create_text(x, y, text="Д", font=("Arial", 16, "bold"),
                                                fill="red" if self.board[row][col] == self.WHITE else "gold")

        if self.selected:
            sr, sc = self.selected
            x = sc * self.cell_size + self.cell_size // 2
            y = sr * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow", outline="")

        for (r, c) in self.valid_moves:
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="green", outline="")

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if not (0 <= row < self.SIZE and 0 <= col < self.SIZE):
            return

        if (row, col) in self.valid_moves:
            self.execute_move(row, col)
            return

        if self.board[row][col] == self.current_player:
            self.selected = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            self.draw_board()
        else:
            self.selected = None
            self.valid_moves = []
            self.draw_board()

    def get_valid_moves(self, row, col):
        moves = []
        player = self.board[row][col]
        if player == self.EMPTY:
            return moves

        jumps = self.get_jumps(row, col)
        if jumps:
            return jumps

        direction = -1 if player == self.WHITE else 1
        if not self.dame[row][col]:
            for dc in (-1, 1):
                nr, nc = row + direction, col + dc
                if 0 <= nr < self.SIZE and 0 <= nc < self.SIZE and self.board[nr][nc] == self.EMPTY:
                    moves.append((nr, nc))
        else:
            for dr in (-1, 1):
                for dc in (-1, 1):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.SIZE and 0 <= nc < self.SIZE and self.board[nr][nc] == self.EMPTY:
                        moves.append((nr, nc))
        return moves

    def get_jumps(self, row, col):
        jumps = []
        player = self.board[row][col]
        if player == self.EMPTY:
            return jumps

        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in dirs:
            r1, c1 = row + dr, col + dc
            if not (0 <= r1 < self.SIZE and 0 <= c1 < self.SIZE):
                continue
            if self.board[r1][c1] == self.EMPTY or self.board[r1][c1] == player:
                continue
            r2, c2 = row + 2 * dr, col + 2 * dc
            if 0 <= r2 < self.SIZE and 0 <= c2 < self.SIZE and self.board[r2][c2] == self.EMPTY:
                jumps.append((r2, c2))
        return jumps
                
    def execute_move(self, to_row, to_col):
        fr, fc = self.selected
        player = self.board[fr][fc]
        is_dame = self.dame[fr][fc]

        if abs(to_row - fr) == 2 and abs(to_col - fc) == 2:
            mid_r = (fr + to_row) // 2
            mid_c = (fc + to_col) // 2
            self.board[mid_r][mid_c] = self.EMPTY
            self.dame[mid_r][mid_c] = False

        self.board[to_row][to_col] = player
        self.dame[to_row][to_col] = is_dame
        self.board[fr][fc] = self.EMPTY
        self.dame[fr][fc] = False

        if player == self.WHITE and to_row == 0:
            self.dame[to_row][to_col] = True
        elif player == self.BLACK and to_row == self.SIZE - 1:
            self.dame[to_row][to_col] = True

        if self.check_win(player):
            winner = "Белые" if player == self.WHITE else "Чёрные"
            messagebox.showinfo("Игра окончена", f"Победили {winner}!")
            self.window.destroy()
            return

        self.current_player = self.BLACK if player == self.WHITE else self.WHITE
        self.selected = None
        self.valid_moves = []
        self.draw_board()

        if not self.has_any_move(self.current_player):
            winner = "Белые" if self.current_player == self.BLACK else "Чёрные"
            messagebox.showinfo("Игра окончена", f"Победили {winner} (нет ходов)!")
            self.window.destroy()

    def has_any_move(self, player):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.board[r][c] == player:
                    if self.get_valid_moves(r, c):
                        return True
        return False

    def check_win(self, player):
        opponent = self.BLACK if player == self.WHITE else self.WHITE
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.board[r][c] == opponent:
                    return False
        return True

# --------------------- Сапёр ---------------------
class MineSweeper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Сапёр")
        self.window.resizable(False, False)

        self.rows = 9
        self.cols = 9
        self.mines = 10
        self.cell_size = 40

        self.board = [[0] * self.cols for _ in range(self.rows)]  # 0 - пусто, -1 - мина, числа - количество мин вокруг
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        self.game_over = False

        self.buttons = [[None] * self.cols for _ in range(self.rows)]

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=10)

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(frame, width=2, height=1, font=("Arial", 12, "bold"),
                                command=lambda row=r, col=c: self.left_click(row, col))
                btn.bind("<Button-3>", lambda e, row=r, col=c: self.right_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

        # Кнопка "Новая игра"
        self.btn_new = tk.Button(self.window, text="Новая игра", font=("Arial", 12),
                                 command=self.new_game)
        self.btn_new.pack(pady=5)

    def new_game(self):
        # Сброс состояния
        self.game_over = False
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        self.board = [[0] * self.cols for _ in range(self.rows)]

        # Расстановка мин
        positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in positions:
            r = pos // self.cols
            c = pos % self.cols
            self.board[r][c] = -1

        # Подсчёт чисел
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == -1:
                            count += 1
                self.board[r][c] = count

        # Обновляем кнопки
        self.update_buttons()

    def update_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                if self.revealed[r][c]:
                    if self.board[r][c] == -1:
                        btn.config(text="💣", bg="red", state="disabled")
                    else:
                        val = self.board[r][c]
                        text = str(val) if val > 0 else ""
                        color = "black"
                        if val == 1: color = "blue"
                        elif val == 2: color = "green"
                        elif val == 3: color = "red"
                        elif val == 4: color = "darkblue"
                        elif val == 5: color = "darkred"
                        btn.config(text=text, fg=color, bg="lightgray", state="disabled")
                elif self.flagged[r][c]:
                    btn.config(text="🚩", bg="yellow", state="normal")
                else:
                    btn.config(text="", bg="SystemButtonFace", state="normal")

    def left_click(self, row, col):
        if self.game_over:
            return
        if self.flagged[row][col]:
            return
        if self.revealed[row][col]:
            return

        # Если мина - проигрыш
        if self.board[row][col] == -1:
            self.revealed[row][col] = True
            self.game_over = True
            self.update_buttons()
            messagebox.showinfo("Игра окончена", "Вы попали на мину! Попробуйте снова.")
            return



        self.reveal_cell(row, col)

        # Проверка победы
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Поздравляем!", "Вы выиграли! Все мины обезврежены.")

    def right_click(self, row, col):
        if self.game_over:
            return
        if self.revealed[row][col]:
            return
        # Переключение флажка
        self.flagged[row][col] = not self.flagged[row][col]
        self.update_buttons()

    def reveal_cell(self, row, col):
        # Открываем клетку, если она не открыта и не заминирована
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if self.revealed[row][col] or self.flagged[row][col]:
            return
        if self.board[row][col] == -1:
            return

        self.revealed[row][col] = True
        self.update_buttons()

        # Если число 0, открываем соседей рекурсивно
        if self.board[row][col] == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if not self.revealed[nr][nc] and not self.flagged[nr][nc]:
                            self.reveal_cell(nr, nc)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True

# --------------------- Запуск ---------------------
if __name__ == "__main__":
    MainMenu()  
