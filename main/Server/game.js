const express = require("express");
const http = require("http");
const socketIo = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let gameState = {
    board: Array(15).fill(0).map(() => Array(15).fill(0)),
    currentPlayer: 1,
};

io.on("connection", (socket) => {
    console.log("新玩家连接:", socket.id);

    socket.emit("gameData", gameState);

    socket.on("makeMove", (data) => {
        if (gameState.board[data.row][data.col] === 0) {
            gameState.board[data.row][data.col] = gameState.currentPlayer;
            gameState.currentPlayer = gameState.currentPlayer === 1 ? 2 : 1;
            io.emit("gameData", gameState);
        }
    });

    socket.on("disconnect", () => {
        console.log("玩家断开连接:", socket.id);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`服务器运行在 http://127.0.0.1:${PORT}`);
});
