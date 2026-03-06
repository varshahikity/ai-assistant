import json
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from analyzer import analyze_code


# Base directories for backend and frontend.
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = str(BASE_DIR.parent / "frontend")
DATABASE_PATH = BASE_DIR / "database.db"


app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


def init_database() -> None:
    """
    Create analysis_history table if it does not exist.
    """
    connection = sqlite3.connect(str(DATABASE_PATH))
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            language TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# Initialize DB on import so both `python app.py` and `flask run` work.
init_database()


def save_analysis(code: str, language: str, result: dict) -> None:
    """
    Store each analysis record in SQLite.
    """
    connection = sqlite3.connect(str(DATABASE_PATH))
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history (code, language, result, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            code,
            language,
            json.dumps(result),
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        ),
    )

    connection.commit()
    connection.close()


@app.route("/")
def serve_index():
    """
    Serve frontend page.
    """
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accept code from frontend and return analysis results.
    """
    data = request.get_json(silent=True) or {}

    code = data.get("code", "")
    language = data.get("language", "")

    if not code.strip():
        return jsonify({"error": "Code input is required."}), 400

    if language.lower() not in {"python", "java", "cpp", "c++"}:
        return jsonify({"error": "Language must be Python, Java, or C++."}), 400

    result = analyze_code(code, language)
    save_analysis(code, language, result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)



