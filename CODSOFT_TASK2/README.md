# Task 2: Unbeatable AI Tic Tac Toe Game

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![Algorithm](https://img.shields.io/badge/Algorithm-Minimax%20with%20Alpha--Beta%20Pruning-orange)
![Internship](https://img.shields.io/badge/CodSoft-AI%20Internship-purple)

A full-stack, responsive web implementation of the classic game of Tic Tac Toe using an unbeatable **Minimax Decision Algorithm with Alpha Beta Pruning**. This project was made as a part of the CodSoft Artificial Intelligence Internship.

---

## 📌 Project Overview
The application gives the user a modern web interface to play against an AI opponent that uses graph decision trees to make the best possible decisions. The AI checks every possible state to make sure it never loses.

### Important Features
* **Unbeatable Minimax AI:** An optimal decision making algorithm that ensures the AI wins or draws.
* **Alpha Beta Pruning:** Optimizes decision tree evaluation and makes the move instantly.
* **Modern Web Interface:** A dark mode glassmorphic UI designed using HTML5, CSS3, and JavaScript.
* **Automated Unit Tests:** Full coverage of game logic, winning conditions and Minimax depth with pytest.

---


## 📁 Project Structure

```text
CODSOFT_TASK2/
├── app.py                  # Flask Web Server and API Endpoints
├── game_logic.py           # Game Board State and Minimax Algorithm
├── requirements.txt        # Project Dependencies
├── README.md               # Documentation
├── .gitignore              # Git Ignored Files
├── templates/
│   └── index.html          # Webpage Structure
├── static/
│   ├── css/
│   │   └── style.css       # Glassmorphism Design Style
│   └── js/
│       └── app.js          # Interactive Game Logic
└── tests/
    └── test_game.py        # Unit Tests




🛠️ Technology Stack
Language: Python 3.10+

Backend Framework: Flask

AI Engine: Minimax Algorithm with Alpha-Beta Pruning

Frontend: HTML5, Modern CSS3 (Glassmorphism), Vanilla JavaScript (ES6)

Testing Suite: Pytest





    Set Up Virtual Environment:

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

Install Dependencies:

Bash
pip install -r requirements.txt

Run Unit Tests:

Bash
python -m pytest

Start Application Server:

Bash
python app.py

Open http://127.0.0.1:5000 in your web browser.

📊 Learning Outcomes
Designed decision trees using game theory principles and adversarial search.

Reduced computational evaluation steps using Alpha-Beta Pruning.

Connected Python AI algorithms with modern asynchronous JavaScript APIs.

👤 Author