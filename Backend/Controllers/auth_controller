from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

def signup():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not name or not email or not password:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            cursor.close()
            conn.close()

            return jsonify({
                "status": "error",
                "message": "Email already exists."
            }), 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(%s, %s, %s)
            """,
            (name, email, hashed_password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "User registered successfully."
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required."
            }), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found."
            }), 404

        if not check_password_hash(user["password"], password):
            return jsonify({
                "status": "error",
                "message": "Invalid password."
            }), 401

        return jsonify({
            "status": "success",
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
