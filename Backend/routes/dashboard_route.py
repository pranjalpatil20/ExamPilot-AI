from flask import Blueprint, jsonify
from database import get_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
def dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM documents")
    total_pdfs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM repeated_questions")
    repeated_questions = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "total_pdfs": total_pdfs,
        "total_questions": total_questions,
        "repeated_questions": repeated_questions
    })