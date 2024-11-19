import tkinter as tk
from tkinter import messagebox

import socketio

# 创建 Socket.IO 客户端
sio = socketio.Client()


class GomokuGame:
    def __init__(self, root_):
        self.current_player = 1  # 1代表黑棋，2代表白棋
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
        for i in range(15):
            self.canvas.create_line(40, 40 + i * 40, 560, 40 + i * 40)  # 横线
            self.canvas.create_line(40 + i * 40, 40, 40 + i * 40, 560)  # 竖线

    def update_game_state(self, data):
        self.board = data['board']
        self.current_player = data['currentPlayer']
        self.redraw_board()

        winner = data.get('winner')
        if winner:
            messagebox.showinfo("游戏结束", f"{'黑棋' if winner == 1 else '白棋'} 获胜!")
            self.reset_game()

        self.current_player_label.config(text="当前玩家: 黑棋" if self.current_player == 1 else "当前玩家: 白棋")

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
        row, col = (y - 40) // 40, (x - 40) // 40  # 修正边界

        if 15 > row >= 0 == self.board[row][col] and 0 <= col < 15:
            # 向服务器发送落子
            sio.emit('makeMove', {'row': row, 'col': col})

    def draw_piece(self, row, col, color):
        x0, y0 = 40 + col * 40 - 15, 40 + row * 40 - 15
        x1, y1 = 40 + col * 40 + 15, 40 + row * 40 + 15
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def reset_game(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.current_player = 1
        self.redraw_board()
        self.current_player_label.config(text="当前玩家: 黑棋")


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
