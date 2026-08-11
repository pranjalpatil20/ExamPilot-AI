# ==========================================================
# ExamPilot AI
# Update Metadata for Bulk Uploaded PDFs
# ==========================================================

import os
import re

from database import get_connection


# ==========================================================
# UPDATE METADATA
# ==========================================================

def update_metadata():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ------------------------------------------------------
    # Get bulk uploaded documents where metadata is missing
    # ------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            pdf_path,
            filename
        FROM documents
        WHERE branch IS NULL
           OR semester IS NULL
           OR subject IS NULL
           OR year IS NULL
           OR exam_type IS NULL
    """)

    documents = cursor.fetchall()

    print(f"Found {len(documents)} documents to update.")

    updated = 0
    failed = 0

    # ------------------------------------------------------
    # Process each document
    # ------------------------------------------------------

    for document in documents:

        document_id = document["id"]
        pdf_path = document["pdf_path"]
        filename = document["filename"]

        try:

            if not pdf_path:
                print(f"❌ ID {document_id}: No PDF path")
                failed += 1
                continue

            # --------------------------------------------------
            # Normalize Windows path
            # --------------------------------------------------

            normalized_path = pdf_path.replace("\\", "/")

            parts = normalized_path.split("/")

            # --------------------------------------------------
            # Find K-Scheme position
            #
            # Dataset/K-Scheme/
            # Branch/
            # 6th Sem/
            # Subject/
            # Summer-2026.pdf
            # --------------------------------------------------

            if "K-Scheme" not in parts:

                print(
                    f"⚠ ID {document_id}: "
                    f"K-Scheme path not found"
                )

                failed += 1
                continue

            k_index = parts.index("K-Scheme")

            # Need:
            # branch
            # semester
            # subject
            # filename

            if len(parts) <= k_index + 4:

                print(
                    f"⚠ ID {document_id}: "
                    f"Unexpected path: {pdf_path}"
                )

                failed += 1
                continue

            branch = parts[k_index + 1]

            semester_folder = parts[k_index + 2]

            subject = parts[k_index + 3]

            actual_filename = parts[k_index + 4]

            # --------------------------------------------------
            # Semester
            # --------------------------------------------------

            semester_match = re.search(
                r"(\d+)",
                semester_folder
            )

            if not semester_match:

                print(
                    f"⚠ ID {document_id}: "
                    f"Semester not found"
                )

                failed += 1
                continue

            semester = int(
                semester_match.group(1)
            )

            # --------------------------------------------------
            # Exam Type + Year
            #
            # Example:
            # Summer-2026.pdf
            # Winter-2025.pdf
            # --------------------------------------------------

            filename_without_ext = os.path.splitext(
                actual_filename
            )[0]

            exam_match = re.search(
                r"(Summer|Winter)[-_ ]?(\d{4})",
                filename_without_ext,
                re.IGNORECASE
            )

            if not exam_match:

                print(
                    f"⚠ ID {document_id}: "
                    f"Year/exam type not found "
                    f"from {actual_filename}"
                )

                failed += 1
                continue

            exam_type = exam_match.group(1).capitalize()

            year = int(
                exam_match.group(2)
            )

            # --------------------------------------------------
            # Update database
            # --------------------------------------------------

            update_query = """
                UPDATE documents
                SET
                    branch = %s,
                    semester = %s,
                    subject = %s,
                    year = %s,
                    exam_type = %s
                WHERE id = %s
            """

            cursor.execute(
                update_query,
                (
                    branch,
                    semester,
                    subject,
                    year,
                    exam_type,
                    document_id
                )
            )

            conn.commit()

            updated += 1

            print(
                f"✔ {updated}. "
                f"{branch} | "
                f"Sem {semester} | "
                f"{subject} | "
                f"{exam_type} {year}"
            )

        except Exception as e:

            failed += 1

            print(
                f"❌ ID {document_id}: {e}"
            )

    cursor.close()
    conn.close()

    # ------------------------------------------------------
    # Final result
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("METADATA UPDATE FINISHED")
    print("=" * 70)

    print("Total found :", len(documents))
    print("Updated     :", updated)
    print("Failed      :", failed)

    print("=" * 70)


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    update_metadata()