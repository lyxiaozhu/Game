import tkinter as tk
from tkinter import messagebox
import socketio

# 创建 Socket.IO 客户端
sio = socketio.Client()


class GomokuGame:
    def __init__(self, root_):
        self.current_player = None
        self.root = root_
        self.root.title("五子棋游戏")
        self.canvas = tk.Canvas(root_, width=600, height=600, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)

        self.current_player_label = tk.Label(root_, text="当前玩家: 黑棋")
        self.current_player_label.pack()

        # 初始化棋盘状态
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.draw_board()

        # 连接到服务器
        sio.connect('http://127.0.0.1:3000')
        sio.on('gameData', self.update_game_state)

    def draw_board(self):
        for i in range(14):
            self.canvas.create_line(40, 40 + i * 40, 560, 40 + i * 40)
            self.canvas.create_line(40 + i * 40, 40, 40 + i * 40, 560)

    def update_game_state(self, data):
        self.board = data['board']
        print("Current board state:", self.board)  # 打印棋盘状态
        self.current_player = data['currentPlayer']
        self.current_player_label.config(text="当前玩家: 黑棋" if self.current_player == 1 else "当前玩家: 白棋")
        self.redraw_board()

    def redraw_board(self):
        self.canvas.delete("all")
        self.draw_board()
        for row in range(15):
            for col in range(15):
                if self.board[row][col] == 1:  # 黑棋
                    self.draw_piece(row, col, "black")
                elif self.board[row][col] == 2:  # 白棋
                    self.draw_piece(row, col, "white")

    def click(self, event):
        x, y = event.x, event.y
        row, col = (y - 20) // 40, (x - 20) // 40

        if 15 > row >= 0 == self.board[row][col] and 0 <= col < 15:
            # 向服务器发送落子
            sio.emit('makeMove', {'row': row, 'col': col})

    def draw_piece(self, row, col, color):
        x0, y0 = 40 + col * 40 - 15, 40 + row * 40 - 15
        x1, y1 = 40 + col * 40 + 15, 40 + row * 40 + 15
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
