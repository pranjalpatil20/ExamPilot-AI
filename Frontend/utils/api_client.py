# ==========================================================
# ExamPilot AI
# API Client
# Streamlit Frontend → Flask Backend
# ==========================================================

import requests

from utils.api import BASE_URL

# ==========================================================
# COMMON REQUEST HANDLER
# ==========================================================

def handle_response(response):

    try:
        data = response.json()
    except Exception:
        data = {
            "message": response.text
        }

    if response.ok:
        return data

    return {
        "error": data.get(
            "message",
            "Something went wrong"
        )
    }


# ==========================================================
# DASHBOARD
# ==========================================================

def get_dashboard_stats():

    try:

        response = requests.get(
            f"{BASE_URL}/dashboard/stats",
            timeout=10
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend request timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# DOCUMENT SEARCH
# ==========================================================

def search_documents(
    query="",
    branch=None,
    semester=None,
    subject=None,
    year=None,
    exam_type=None
):

    try:

        params = {}

        if query:
            params["query"] = query

        if branch:
            params["branch"] = branch

        if semester:
            params["semester"] = semester

        if subject:
            params["subject"] = subject

        if year:
            params["year"] = year

        if exam_type:
            params["exam_type"] = exam_type

        response = requests.get(
            f"{BASE_URL}/documents/search",
            params=params,
            timeout=10
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend request timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# GET DOCUMENT
# ==========================================================

def get_document(document_id):

    try:

        response = requests.get(
            f"{BASE_URL}/documents/{document_id}",
            timeout=10
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# OPEN PDF
# ==========================================================

def get_pdf_url(document_id):

    return (
        f"{BASE_URL}/pdf/open/{document_id}"
    )

# ==========================================================
# DOWNLOAD PDF
# ==========================================================
def get_download_url(document_id):

    return (
        f"{BASE_URL}/pdf/download/{document_id}"
    )


# ==========================================================
# GET QUESTIONS
# ==========================================================

def get_questions(document_id):

    try:

        response = requests.get(
            f"{BASE_URL}/questions/{document_id}",
            timeout=10
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend request timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# GET REPEATED QUESTIONS
# ==========================================================

def get_repeated_questions(document_id):

    try:

        response = requests.get(
            f"{BASE_URL}/questions/repeated/{document_id}",
            timeout=10
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend request timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# UPLOAD DOCUMENT
# ==========================================================

def upload_document(
    file,
    title,
    document_type,
    branch,
    semester,
    subject,
    year,
    exam_type
):

    try:

        files = {
            "file": (
                file.name,
                file,
                "application/pdf"
            )
        }

        data = {
            "title": title,
            "document_type": document_type,
            "branch": branch,
            "semester": semester,
            "subject": subject,
            "year": year,
            "exam_type": exam_type
        }

        response = requests.post(
            f"{BASE_URL}/documents/upload",
            files=files,
            data=data,
            timeout=60
        )

        return handle_response(response)

    except requests.exceptions.ConnectionError:

        return {
            "error": "Flask backend is not running."
        }

    except requests.exceptions.Timeout:

        return {
            "error": "PDF upload timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }