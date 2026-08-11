# import fitz  # PyMuPDF

# def extract_text(pdf_path):
#     text = ""

#     pdf = fitz.open(pdf_path)

#     for page in pdf:
#         text += page.get_text()

#     pdf.close()

#     return text

# ===============================================================================================

import fitz
from database import get_connection

def extract_text(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)

    for page in pdf:
        page_text = page.get_text()

        page_text = page_text.replace("P.T.O.", "")
        page_text = page_text.replace("p.t.o.", "")
        page_text = page_text.replace("P.T.O", "")
        page_text = page_text.replace("p.t.o", "")

        text += page_text

    pdf.close()

    return text

def save_extracted_text(document_id, text):

    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO extracted_text(document_id, extracted_text)
    VALUES(%s, %s)
    """
    values = (document_id, text)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()