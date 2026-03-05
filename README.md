# AI-Powered Developer Assistant for Automated Code Analysis

A simple full-stack web application that analyzes code snippets in **Python**, **Java**, and **C++**.

## Features

- Paste code and select language from the UI
- Analyze code using a Flask backend
- Shows:
  - Basic syntax check
  - Code improvement suggestions
  - Complexity analysis (lines, loops, functions, conditions)
  - Auto-generated documentation summary
  - Test case suggestions
- Stores analysis history in SQLite (`backend/database.db`)

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite

## Project Structure

```text
ai-developer-assistant/
|
|-- backend/
|   |-- app.py
|   |-- analyzer.py
|   `-- database.db (created automatically)
|
|-- frontend/
|   |-- index.html
|   |-- style.css
|   `-- script.js
|
|-- README.md
`-- requirements.txt
```

## How to Run

1. Open terminal in the project folder:

```bash
cd ai-developer-assistant
```

2. Create and activate virtual environment (recommended):

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start Flask server:

```bash
cd backend
python app.py
```

5. Open browser and visit:

```text
http://127.0.0.1:5000/
```

## Notes

- SQLite database file is created automatically at first run.
- Syntax checks for Java and C++ are lightweight and beginner-friendly.
- This is a simple educational project and not a full compiler/static analyzer.

