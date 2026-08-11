# ==========================================================
# ExamPilot AI
# PDF Routes
# ==========================================================

from flask import Blueprint, send_file, jsonify

from database import get_connection


# ==========================================================
# BLUEPRINT
# ==========================================================

pdf_bp = Blueprint(
    "pdf",
    __name__
)


# ==========================================================
# EXTRACT PDF TEXT
# ==========================================================

from controllers.pdf_controller import extract_pdf_text


@pdf_bp.route(
    "/extract",
    methods=["POST"]
)
def extract_pdf():

    return extract_pdf_text()


# ==========================================================
# OPEN PDF
# ==========================================================

@pdf_bp.route(
    "/open/<int:document_id>",
    methods=["GET"]
)
def open_pdf(document_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        id,
        filename,
        pdf_path
    FROM documents
    WHERE id = %s
    """

    cursor.execute(
        query,
        (document_id,)
    )

    document = cursor.fetchone()

    cursor.close()
    conn.close()

    # ------------------------------------------------------
    # DOCUMENT NOT FOUND
    # ------------------------------------------------------

    if not document:

        return jsonify({
            "success": False,
            "message": "Document not found."
        }), 404

    pdf_path = document.get("pdf_path")

    # ------------------------------------------------------
    # PDF PATH NOT FOUND
    # ------------------------------------------------------

    if not pdf_path:

        return jsonify({
            "success": False,
            "message": "PDF path is not available."
        }), 404

    # ------------------------------------------------------
    # SEND PDF
    # ------------------------------------------------------

    try:

        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=False,
            download_name=document.get(
                "filename",
                f"question_paper_{document_id}.pdf"
            )
        )

    except FileNotFoundError:

        return jsonify({
            "success": False,
            "message": "PDF file not found on server.",
            "pdf_path": pdf_path
        }), 404

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

@pdf_bp.route(
    "/download/<int:document_id>",
    methods=["GET"]
)
def download_pdf(document_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        id,
        filename,
        pdf_path
    FROM documents
    WHERE id = %s
    """

    cursor.execute(
        query,
        (document_id,)
    )

    document = cursor.fetchone()

    cursor.close()
    conn.close()

    if not document:

        return jsonify({
            "success": False,
            "message": "Document not found."
        }), 404

    pdf_path = document.get("pdf_path")

    if not pdf_path:

        return jsonify({
            "success": False,
            "message": "PDF path is not available."
        }), 404

    try:

        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=document.get(
                "filename",
                f"question_paper_{document_id}.pdf"
            )
        )

    except FileNotFoundError:

        return jsonify({
            "success": False,
            "message": "PDF file not found on server."
        }), 404

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500