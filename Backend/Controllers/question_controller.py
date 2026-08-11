# ==========================================================
# ExamPilot AI
# Question Controller
# ==========================================================

from services.question_service import (
    get_questions_by_document,
    get_repeated_questions,
    get_all_questions,
    search_questions,
    extract_and_save_questions
)

from services.similarity_service import (
    find_repeated_questions
)


# ==========================================================
# GET QUESTIONS BY DOCUMENT
# ==========================================================

def fetch_questions(document_id):

    questions = get_questions_by_document(
        document_id
    )

    return {
        "document_id": document_id,
        "total_questions": len(questions),
        "questions": questions
    }


# ==========================================================
# EXTRACT AND SAVE QUESTIONS
# ==========================================================

def extract_questions(document_id):

    return extract_and_save_questions(
        document_id
    )


# ==========================================================
# GET REPEATED QUESTIONS
# ==========================================================

def fetch_repeated_questions(document_id):

    questions = get_questions_by_document(
        document_id
    )

    repeated = find_repeated_questions(
        questions,
        threshold=0.40
    )

    return {
        "document_id": document_id,
        "total_repeated": len(repeated),
        "repeated_questions": repeated
    }


# ==========================================================
# GET ALL REPEATED QUESTIONS
# ==========================================================

def fetch_all_repeated_questions():

    questions = get_all_questions()

    repeated = find_repeated_questions(
        questions,
        threshold=0.75
    )

    return {
        "total_questions_checked": len(questions),
        "total_repeated": len(repeated),
        "repeated_questions": repeated
    }


# ==========================================================
# SEARCH QUESTIONS
# ==========================================================

def fetch_search_questions(keyword):

    questions = search_questions(
        keyword
    )

    return {
        "query": keyword,
        "total_results": len(questions),
        "results": questions
    }