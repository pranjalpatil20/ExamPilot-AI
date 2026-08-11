from flask import request, jsonify
from services.pdf_service import extract_text
import os

UPLOAD_FOLDER = "uploads"

def extract_pdf_text():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    text = extract_text(filepath)

    return jsonify({
        "success": True,
        "filename": file.filename,
        "text": text
    })