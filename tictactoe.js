<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe</title>
    <style>
        .game-container {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            gap: 5px;
            margin: 20px auto;
            width: 310px;
        }

        .cell {
            width: 100px;
            height: 100px;
            background: #fff;
            border: 2px solid #333;
            font-size: 40px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .cell:hover {
            background: #f0f0f0;
        }

        .status {
            text-align: center;
            font-size: 24px;
            margin: 20px;
            font-family: Arial, sans-serif;
        }

        .reset-btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="status" id="status">Player X's turn</div>
    <div class="game-container" id="board">
        <button class="cell" data-index="0"></button>
        <button class="cell" data-index="1"></button>
        <button class="cell" data-index="2"></button>
        <button class="cell" data-index="3"></button>
        <button class="cell" data-index="4"></button>
        <button class="cell" data-index="5"></button>
        <button class="cell" data-index="6"></button>
        <button class="cell" data-index="7"></button>
        <button class="cell" data-index="8"></button>
    </div>
    <button class="reset-btn" onclick="resetGame()">Reset Game</button>

    <script>
        let currentPlayer = 'X';
        let gameActive = true;
        let gameState = ['', '', '', '', '', '', '', '', ''];
        const winningCombos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6] // Diagonals
        ];

        document.getElementById('board').addEventListener('click', handleCellClick);

        function handleCellClick(event) {
            const cell = event.target;
            const cellIndex = parseInt(cell.dataset.index);

            if (gameState[cellIndex] !== '' || !gameActive) return;

            gameState[cellIndex] = currentPlayer;
            cell.textContent = currentPlayer;
            
            if (checkWin()) {
                document.getElementById('status').textContent = `Player ${currentPlayer} wins!`;
                gameActive = false;
                return;
            }

            if (checkDraw()) {
                document.getElementById('status').textContent = "Game ended in a draw!";
                gameActive = false;
                return;
            }

            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            document.getElementById('status').textContent = `Player ${currentPlayer}'s turn`;
        }

        function checkWin() {
            return winningCombos.some(combo => {
                return combo.every(index => {
                    return gameState[index] === currentPlayer;
                });
            });
        }

        function checkDraw() {
            return gameState.every(cell => cell !== '');
        }

        function resetGame() {
            currentPlayer = 'X';
            gameActive = true;
            gameState = ['', '', '', '', '', '', '', '', ''];
            document.querySelectorAll('.cell').forEach(cell => {
                cell.textContent = '';
            });
            document.getElementById('status').textContent = `Player ${currentPlayer}'s turn`;
        }
    </script>
</body>
</html>
