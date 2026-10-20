let boardState = Array(9).fill(" ");
let isGameOver = false;

const cells = document.querySelectorAll('.cell');
const statusText = document.getElementById('status-text');
const resetBtn = document.getElementById('reset-btn');

cells.forEach(cell => {
    cell.addEventListener('click', () => handleCellClick(cell));
});

resetBtn.addEventListener('click', resetGame);

async function handleCellClick(cell) {
    const index = parseInt(cell.getAttribute('data-index'));

    if (boardState[index] !== " " || isGameOver) return;

    // Render Human Move Locally First
    boardState[index] = "X";
    updateBoardUI();
    statusText.innerText = "AI Thinking (O)...";
    disableBoard(true);

    try {
        // Send move to Flask Python backend
        const response = await fetch('/api/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: boardState, move: index })
        });

        const data = await response.json();
        boardState = data.board;
        updateBoardUI();

        if (data.winner) {
            handleGameOver(data.winner, data.winning_line);
        } else {
            statusText.innerText = "Your Turn (X)";
            disableBoard(false);
        }
    } catch (error) {
        console.error("Error communicating with backend:", error);
        statusText.innerText = "Error connecting to server";
    }
}

function updateBoardUI() {
    cells.forEach((cell, i) => {
        const val = boardState[i];
        cell.innerText = val !== " " ? val : "";
        cell.classList.remove('x', 'o');
        if (val === 'X') cell.classList.add('x');
        if (val === 'O') cell.classList.add('o');
        cell.disabled = val !== " " || isGameOver;
    });
}

function handleGameOver(winner, winningLine) {
    isGameOver = true;
    disableBoard(true);

    if (winningLine) {
        winningLine.forEach(idx => cells[idx].classList.add('winner'));
    }

    if (winner === 'X') {
        statusText.innerText = "You Win! 🎉";
    } else if (winner === 'O') {
        statusText.innerText = "AI Wins! 🤖";
    } else {
        statusText.innerText = "It's a Draw! 🤝";
    }
}

function disableBoard(disabled) {
    cells.forEach((cell, i) => {
        if (boardState[i] === " " && !isGameOver) {
            cell.disabled = disabled;
        }
    });
}

function resetGame() {
    boardState = Array(9).fill(" ");
    isGameOver = false;
    cells.forEach(cell => {
        cell.classList.remove('winner', 'x', 'o');
        cell.disabled = false;
    });
    statusText.innerText = "Your Turn (X)";
    updateBoardUI();
}