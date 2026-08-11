# ==========================================================
# ExamPilot AI
# Document Service
# ==========================================================

import os
import uuid

from database import get_connection


# ==========================================================
# UPLOAD / SAVE DOCUMENT
# ==========================================================

def save_document(file, data):

    connection = None
    cursor = None

    try:

        upload_folder = os.path.join(
            os.getcwd(),
            "uploads"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        # --------------------------------------------------
        # Create UNIQUE filename
        # --------------------------------------------------

        original_filename = file.filename

        unique_filename = (
            str(uuid.uuid4())
            + "_"
            + original_filename
        )

        file_path = os.path.join(
            upload_folder,
            unique_filename
        )

        # --------------------------------------------------
        # Save PDF
        # --------------------------------------------------

        file.save(file_path)

        # --------------------------------------------------
        # Database
        # --------------------------------------------------

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            INSERT INTO documents
            (
                title,
                branch,
                semester,
                subject,
                year,
                exam_type,
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
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (
            data.get("title"),
            data.get("branch"),
            data.get("semester"),
            data.get("subject"),
            data.get("year"),
            data.get("exam_type"),
            original_filename,
            file_path,
            "UPLOADED"
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        document_id = cursor.lastrowid

        return {
            "success": True,
            "message": "Document uploaded successfully.",
            "document_id": document_id
        }

    except Exception as e:

        if connection:
            connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================================
# SEARCH DOCUMENTS
# ==========================================================

def search_documents(
    branch=None,
    semester=None,
    subject=None,
    year=None,
    exam_type=None
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                title,
                branch,
                semester,
                subject,
                year,
                exam_type,
                filename,
                pdf_path,
                status,
                created_at
            FROM documents
            WHERE 1 = 1
        """

        params = []

        # --------------------------------------------------
        # BRANCH
        # --------------------------------------------------

        if branch:

            query += """
                AND LOWER(TRIM(branch))
                = LOWER(TRIM(%s))
            """

            params.append(branch)

        # --------------------------------------------------
        # SEMESTER
        # --------------------------------------------------

        if semester is not None:

            semester_value = str(
                semester
            ).strip()

            if semester_value.lower().startswith(
                "semester "
            ):

                semester_number = (
                    semester_value[9:]
                    .strip()
                )

            else:

                semester_number = semester_value

            query += """
                AND (
                    TRIM(CAST(semester AS CHAR)) = %s
                    OR
                    LOWER(
                        TRIM(
                            CAST(semester AS CHAR)
                        )
                    ) = LOWER(%s)
                    OR
                    LOWER(
                        TRIM(
                            CAST(semester AS CHAR)
                        )
                    ) = LOWER(
                        CONCAT(
                            'Semester ',
                            %s
                        )
                    )
                )
            """

            params.extend([
                semester_number,
                semester_value,
                semester_number
            ])

        # --------------------------------------------------
        # SUBJECT
        # --------------------------------------------------

        if subject:

            query += """
                AND LOWER(TRIM(subject))
                = LOWER(TRIM(%s))
            """

            params.append(subject)

        # --------------------------------------------------
        # YEAR
        # --------------------------------------------------

        if year is not None:

            query += """
                AND CAST(year AS CHAR) = %s
            """

            params.append(
                str(year).strip()
            )

        # --------------------------------------------------
        # EXAM TYPE
        # --------------------------------------------------

        if exam_type:

            query += """
                AND LOWER(TRIM(exam_type))
                = LOWER(TRIM(%s))
            """

            params.append(exam_type)

        # --------------------------------------------------
        # ORDER
        # --------------------------------------------------

        query += """
            ORDER BY year DESC, id DESC
        """

        print("\n========================================")
        print("DOCUMENT SEARCH")
        print("========================================")
        print("Branch:", branch)
        print("Semester:", semester)
        print("Subject:", subject)
        print("Year:", year)
        print("Exam Type:", exam_type)
        print("Parameters:", params)
        print("========================================")

        cursor.execute(
            query,
            params
        )

        documents = cursor.fetchall()

        print(
            "Documents Found:",
            len(documents)
        )

        return documents

    except Exception as e:

        print(
            "Search documents error:",
            str(e)
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================================
# GET DOCUMENT BY ID
# ==========================================================

def get_document_by_id(document_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                title,
                branch,
                semester,
                subject,
                year,
                exam_type,
                filename,
                pdf_path,
                status,
                created_at
            FROM documents
            WHERE id = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (document_id,)
        )

        document = cursor.fetchone()

        return document

    except Exception as e:

        print(
            "Get document error:",
            str(e)
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================================
# UPDATE DOCUMENT METADATA
# ==========================================================

def update_document_metadata(
    document_id,
    branch,
    semester,
    subject,
    year,
    exam_type
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            UPDATE documents
            SET
                branch = %s,
                semester = %s,
                subject = %s,
                year = %s,
                exam_type = %s
            WHERE id = %s
        """

        values = (
            branch,
            semester,
            subject,
            year,
            exam_type,
            document_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "Document not found."
            }

        return {
            "success": True,
            "message": "Document metadata updated successfully."
        }

    except Exception as e:

        if connection:
            connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()