# ==========================================================
# ExamPilot AI
# Bulk PDF Processing Service
# ==========================================================

import os
import traceback

from database import get_connection
from services.pdf_service import extract_text, save_extracted_text
from services.question_service import extract_questions_from_text, save_questions


# ==========================================================
# DATASET FOLDER
# ==========================================================

DATASET_FOLDER = "Dataset/K-Scheme"


# ==========================================================
# PROCESS ALL PDFs
# ==========================================================

def process_all_pdfs():

    total = 0
    success = 0
    failed = 0

    for root, dirs, files in os.walk(DATASET_FOLDER):

        for file in files:

            if not file.lower().endswith(".pdf"):
                continue

            total += 1

            filepath = os.path.join(root, file)

            print("\n" + "=" * 70)
            print(f"Processing: {file}")
            print(f"Path      : {filepath}")
            print("=" * 70)

            conn = None
            cursor = None

            try:

                # --------------------------------------------------
                # CONNECT DATABASE
                # --------------------------------------------------

                conn = get_connection()
                cursor = conn.cursor()

                # --------------------------------------------------
                # INSERT DOCUMENT
                # --------------------------------------------------

                sql = """
                INSERT INTO documents
                (
                    title,
                    document_type,
                    filename,
                    pdf_path,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """

                values = (
                    file,
                    "PYQ",
                    file,
                    filepath,
                    "UPLOADED"
                )

                cursor.execute(sql, values)

                conn.commit()

                document_id = cursor.lastrowid

                # --------------------------------------------------
                # CLOSE DATABASE
                # --------------------------------------------------

                cursor.close()
                cursor = None

                conn.close()
                conn = None

                # --------------------------------------------------
                # EXTRACT PDF TEXT
                # --------------------------------------------------

                print("Extracting text...")

                text = extract_text(filepath)

                if not text:

                    print("⚠ No text extracted.")

                    failed += 1
                    continue

                # --------------------------------------------------
                # SAVE EXTRACTED TEXT
                # --------------------------------------------------

                print("Saving extracted text...")

                save_extracted_text(
                    document_id,
                    text
                )

                # --------------------------------------------------
                # EXTRACT QUESTIONS
                # --------------------------------------------------

                print("Extracting questions...")

                questions = extract_questions_from_text(
                    text
                )

                # --------------------------------------------------
                # SAVE QUESTIONS
                # --------------------------------------------------

                inserted_questions = save_questions(
                    document_id,
                    questions
                )

                # --------------------------------------------------
                # SUCCESS
                # --------------------------------------------------

                success += 1

                print(
                    f"✔ Success: {file}"
                )

                print(
                    f"  Document ID : {document_id}"
                )

                print(
                    f"  Questions   : {inserted_questions}"
                )

            except Exception as e:

                failed += 1

                print("\n" + "=" * 70)
                print(f"❌ Failed File : {filepath}")
                print(f"Error Type    : {type(e).__name__}")
                print(f"Error         : {e}")

                traceback.print_exc()

                print("=" * 70)

            finally:

                if cursor:

                    try:
                        cursor.close()
                    except:
                        pass

                if conn:

                    try:
                        conn.close()
                    except:
                        pass

    # ==========================================================
    # FINAL RESULT
    # ==========================================================

    print("\n")
    print("=" * 70)
    print("BULK PROCESSING FINISHED")
    print("=" * 70)

    print(f"Total   : {total}")
    print(f"Success : {success}")
    print(f"Failed  : {failed}")

    print("=" * 70)

    return {
        "total": total,
        "success": success,
        "failed": failed
    }
