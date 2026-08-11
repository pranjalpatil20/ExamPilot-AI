# ==========================================================
# ExamPilot AI
# Question Routes
# ==========================================================

from flask import Blueprint, jsonify, request

from controllers.question_controller import (
    fetch_questions,
    extract_questions,
    fetch_repeated_questions,
    fetch_all_repeated_questions,
    fetch_search_questions
)


# ==========================================================
# BLUEPRINTa
# ==========================================================

question_bp = Blueprint(
    "question",
    __name__
)


# ==========================================================
# GET QUESTIONS BY DOCUMENT
# ==========================================================

@question_bp.route(
    "/<int:document_id>",
    methods=["GET"]
)
def get_questions(document_id):

    data = fetch_questions(
        document_id
    )

    return jsonify(data)


# ==========================================================
# EXTRACT QUESTIONS
# ==========================================================

@question_bp.route(
    "/extract/<int:document_id>",
    methods=["POST"]
)
def extract_document_questions(document_id):

    data = extract_questions(
        document_id
    )

    return jsonify(data)


# ==========================================================
# GET REPEATED QUESTIONS FOR DOCUMENT
# ==========================================================

@question_bp.route(
    "/repeated/<int:document_id>",
    methods=["GET"]
)
def repeated_questions(document_id):

    data = fetch_repeated_questions(
        document_id
    )

    return jsonify(data)


# ==========================================================
# GET ALL REPEATED QUESTIONS
# ==========================================================

@question_bp.route(
    "/repeated",
    methods=["GET"]
)
def all_repeated_questions():

    data = fetch_all_repeated_questions()

    return jsonify(data)


# ==========================================================
# SEARCH QUESTIONS
# ==========================================================

@question_bp.route(
    "/search",
    methods=["GET"]
)
def search():

    keyword = request.args.get(
        "query"
    )

    data = fetch_search_questions(
        keyword
    )

    return jsonify(data)