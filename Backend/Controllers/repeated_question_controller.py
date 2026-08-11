from flask import jsonify
from services.repeated_question_service import find_repeated_questions


def find_repeated_questions_api():

    try:

        total = find_repeated_questions()

        return jsonify({
            "success": True,
            "message": "Repeated question detection completed.",
            "total_repeated_questions": total
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500