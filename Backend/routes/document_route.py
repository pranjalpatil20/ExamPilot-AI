# ==========================================================
# ExamPilot AI
# Document Routes
# ==========================================================

from flask import Blueprint

from controllers.document_controller import (
    upload_document,
    get_documents,
    open_document,
    download_document,
    update_metadata
)


document_bp = Blueprint(
    "document",
    __name__
)


# ==========================================================
# UPLOAD DOCUMENT
# ==========================================================

@document_bp.route(
    "/upload",
    methods=["POST"]
)
def upload_document_route():

    return upload_document()


# ==========================================================
# SEARCH DOCUMENTS
# ==========================================================

@document_bp.route(
    "/search",
    methods=["GET"]
)
def get_documents_route():

    return get_documents()


# ==========================================================
# OPEN PDF
# ==========================================================

@document_bp.route(
    "/open/<int:document_id>",
    methods=["GET"]
)
def open_document_route(document_id):

    return open_document(
        document_id
    )


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

@document_bp.route(
    "/download/<int:document_id>",
    methods=["GET"]
)
def download_document_route(document_id):

    return download_document(
        document_id
    )


# ==========================================================
# UPDATE METADATA
# ==========================================================

@document_bp.route(
    "/<int:document_id>/metadata",
    methods=["PUT"]
)
def update_metadata_route(document_id):

    return update_metadata(
        document_id
    )