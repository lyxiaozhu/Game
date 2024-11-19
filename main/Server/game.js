const express = require('express');
const socketIO = require('socket.io');
const http = require('http');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

let board = Array.from({ length: 15 }, () => Array(15).fill(0));
let currentPlayer = 1; // 1: 黑棋, 2: 白棋

function checkWin(row, col) {
    const player = board[row][col];
    const directions = [
        [[0, 1], [0, -1]], // 水平
        [[1, 0], [-1, 0]], // 竖直
        [[1, 1], [-1, -1]], // 斜对角
        [[1, -1], [-1, 1]]  // 反斜对角
    ];

    for (const direction of directions) {
        let count = 1;

        for (const [dx, dy] of direction) {
            let x = row + dx;
            let y = col + dy;
            while (x >= 0 && x < 15 && y >= 0 && y < 15 && board[x][y] === player) {
                count++;
                x += dx;
                y += dy;
            }
        }

        if (count >= 5) return player; // 找到五子连珠
    }
    return 0; // 还没有赢
}

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.emit('gameData', { board, currentPlayer });

    socket.on('makeMove', (data) => {
        const { row, col } = data;

        if (board[row][col] === 0) {
            board[row][col] = currentPlayer;
            const winner = checkWin(row, col);
            currentPlayer = currentPlayer === 1 ? 2 : 1; // 切换玩家
            io.emit('gameData', { board, currentPlayer, winner }); // 通知所有客户端
        }
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

server.listen(3000, '127.0.0.1', () => {
    console.log('Server is running on http://127.0.0.1:3000');
});

