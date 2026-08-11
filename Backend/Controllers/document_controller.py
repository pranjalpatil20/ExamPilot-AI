# ==========================================================
# ExamPilot AI
# Document Controller
# ==========================================================

from flask import request, jsonify, send_file
import os

from services.document_service import (
    save_document,
    search_documents,
    get_document_by_id,
    update_document_metadata
)


# ==========================================================
# UPLOAD DOCUMENT
# ==========================================================

def upload_document():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400

    data = {
        "title": request.form.get("title"),
        "branch": request.form.get("branch"),
        "semester": request.form.get("semester"),
        "subject": request.form.get("subject"),
        "year": request.form.get("year"),
        "exam_type": request.form.get("exam_type")
    }

    result = save_document(
        file,
        data
    )

    if result.get("success"):

        return jsonify(result), 201

    return jsonify(result), 400


# ==========================================================
# SEARCH DOCUMENTS
# ==========================================================

def get_documents():

    branch = request.args.get("branch")
    semester = request.args.get("semester")
    subject = request.args.get("subject")
    year = request.args.get("year")
    exam_type = request.args.get("exam_type")

    documents = search_documents(
        branch=branch,
        semester=semester,
        subject=subject,
        year=year,
        exam_type=exam_type
    )

    return jsonify(documents), 200


# ==========================================================
# OPEN PDF
# ==========================================================

def open_document(document_id):

    print("\n========================================")
    print("OPEN PDF")
    print("Document ID:", document_id)
    print("========================================")

    document = get_document_by_id(
        document_id
    )

    # ------------------------------------------------------
    # Document not found
    # ------------------------------------------------------

    if not document:

        print(
            "DOCUMENT NOT FOUND:",
            document_id
        )

        return jsonify({
            "success": False,
            "message": "Document not found.",
            "document_id": document_id
        }), 404

    print(
        "Document:",
        document
    )

    # ------------------------------------------------------
    # PDF PATH
    # ------------------------------------------------------

    pdf_path = document.get(
        "pdf_path"
    )

    if not pdf_path:

        return jsonify({
            "success": False,
            "message": "PDF path not found.",
            "document_id": document_id
        }), 404

    # ------------------------------------------------------
    # Convert relative path to absolute path
    # ------------------------------------------------------

    if not os.path.isabs(pdf_path):

        pdf_path = os.path.join(
            os.getcwd(),
            pdf_path
        )

    pdf_path = os.path.normpath(
        pdf_path
    )

    print(
        "PDF PATH:",
        pdf_path
    )

    # ------------------------------------------------------
    # Check physical file
    # ------------------------------------------------------

    if not os.path.exists(pdf_path):

        print(
            "PDF FILE DOES NOT EXIST:",
            pdf_path
        )

        return jsonify({
            "success": False,
            "message": "PDF file does not exist on server.",
            "document_id": document_id,
            "pdf_path": pdf_path
        }), 404

    # ------------------------------------------------------
    # SEND PDF
    # ------------------------------------------------------

    try:

        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=False
        )

    except Exception as e:

        print(
            "PDF OPEN ERROR:",
            str(e)
        )

        return jsonify({
            "success": False,
            "message": "Unable to open PDF.",
            "error": str(e)
        }), 500


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

def download_document(document_id):

    document = get_document_by_id(
        document_id
    )

    if not document:

        return jsonify({
            "success": False,
            "message": "Document not found."
        }), 404

    pdf_path = document.get(
        "pdf_path"
    )

    if not pdf_path:

        return jsonify({
            "success": False,
            "message": "PDF path not found."
        }), 404

    if not os.path.isabs(pdf_path):

        pdf_path = os.path.join(
            os.getcwd(),
            pdf_path
        )

    pdf_path = os.path.normpath(
        pdf_path
    )

    if not os.path.exists(pdf_path):

        return jsonify({
            "success": False,
            "message": "PDF file does not exist."
        }), 404

    try:

        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=document.get(
                "filename",
                "question_paper.pdf"
            )
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Unable to download PDF.",
            "error": str(e)
        }), 500


# ==========================================================
# UPDATE METADATA
# ==========================================================

def update_metadata(document_id):

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No metadata received."
        }), 400

    branch = data.get("branch")
    semester = data.get("semester")
    subject = data.get("subject")
    year = data.get("year")
    exam_type = data.get("exam_type")

    if not all([
        branch,
        semester,
        subject,
        year,
        exam_type
    ]):

        return jsonify({
            "success": False,
            "message": "All metadata fields are required."
        }), 400

    result = update_document_metadata(
        document_id,
        branch,
        semester,
        subject,
        year,
        exam_type
    )

    if not result["success"]:

        return jsonify(result), 404

    return jsonify(result), 200