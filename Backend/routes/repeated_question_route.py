from flask import Blueprint
from controllers.repeated_question_controller import find_repeated_questions_api

repeated_question_bp = Blueprint(
    "repeated_question_bp",
    __name__
)

@repeated_question_bp.route("/find", methods=["POST"])
def find_repeated_questions():

    return find_repeated_questions_api()