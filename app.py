import requests
import sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
if not CLERK_SECRET_KEY:
    raise ValueError("CLERK_SECRET_KEY not found in environment variables")
CLERK_API_URL = "https://api.clerk.com/v1"

app = Flask(__name__)

# Initialize SQLite3 database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_data (
            user_id TEXT PRIMARY KEY,
            preferred_theme TEXT DEFAULT 'light',
            last_activity TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Clerk API: Fetch user data
def get_user_by_id(user_id):
    url = f"{CLERK_API_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {CLERK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None

# API endpoint: Store or update user data in SQLite3
@app.route("/user/store", methods=["POST"])
def store_user_data():
    data = request.get_json()
    user_id = data.get("user_id")
    preferred_theme = data.get("preferred_theme", "light")
    last_activity = data.get("last_activity")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Verify user exists in Clerk
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Invalid user_id"}), 404

    # Store/update data in SQLite3
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users_data (user_id, preferred_theme, last_activity)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET preferred_theme = ?, last_activity = ?
    """, (user_id, preferred_theme, last_activity, preferred_theme, last_activity))
    conn.commit()
    conn.close()

    return jsonify({"message": "User data stored successfully"}), 200

# API endpoint: Retrieve user data from SQLite3
@app.route("/user/<user_id>", methods=["GET"])
def get_user_data(user_id):
    # Verify user exists in Clerk
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Invalid user_id"}), 404

    # Fetch data from SQLite3
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_data WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "user_id": row["user_id"],
            "preferred_theme": row["preferred_theme"],
            "last_activity": row["last_activity"]
        })
    else:
        return jsonify({"message": "No data found for this user"}), 404

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True, port=5000)