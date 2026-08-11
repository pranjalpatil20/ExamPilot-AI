from database import get_connection


def dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT COUNT(*) AS total FROM documents")
    total_pdf = cursor.fetchone()["total"]


    cursor.execute("SELECT COUNT(*) AS total FROM questions")
    total_questions = cursor.fetchone()["total"]


    cursor.execute("SELECT COUNT(*) AS total FROM repeated_questions")
    total_repeated = cursor.fetchone()["total"]


    cursor.close()
    conn.close()


    return {
        "total_pdf": total_pdf,
        "total_questions": total_questions,
        "total_repeated_questions": total_repeated
    }