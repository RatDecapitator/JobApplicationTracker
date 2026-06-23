import sqlite3

DATABASE_NAME = "job_applications.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        location TEXT NOT NULL,
        application_date TEXT NOT NULL,
        cv_used TEXT NOT NULL,
        status TEXT NOT NULL
        )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            response_date TEXT NOT NULL,
            content TEXT NOT NULL,
            response_type TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_application(application):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO job_applications
        (
            company_name,
            job_title,
            location,
            application_date,
            cv_used,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            application.company_name,
            application.job_title,
            application.location,
            application.application_date,
            application.cv_used,
            application.status.value,
        ),
    )

    connection.commit()
    application_id = cursor.lastrowid
    connection.close()

    return application_id


def get_all_applications_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM job_applications")
    rows = cursor.fetchall()

    connection.close()

    applications = []

    for row in rows:
        applications.append(
            {
                "id": row[0],
                "company_name": row[1],
                "job_title": row[2],
                "location": row[3],
                "application_date": row[4],
                "cv_used": row[5],
                "status": row[6],
            }
        )

    return applications


def get_application_by_id(application_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM job_applications WHERE id = ?",
        (application_id,),
    )

    row = cursor.fetchone()

    connection.close()

    return {
        "id": row[0],
        "company_name": row[1],
        "job_title": row[2],
        "location": row[3],
        "application_date": row[4],
        "cv_used": row[5],
        "status": row[6],
    }


def delete_application_by_id(application_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM job_applications WHERE id = ?", (application_id,))

    connection.commit()
    connection.close()


def update_application_status(application_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
        """,
        (status, application_id),
    )

    connection.commit()
    connection.close()


def save_company_response(application_id, response):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO company_responses
        (
            application_id,
            response_date,
            content,
            response_type
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            application_id,
            response.response_date,
            response.content,
            response.response_type.value,
        ),
    )

    connection.commit()
    connection.close()


def get_responses_for_application(application_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM company_responses
        WHERE application_id = ?
        """,
        (application_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_application_statistics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT status, COUNT(*) FROM job_applications GROUP BY status")
    rows = cursor.fetchall()

    connection.close()

    statistics = {
        "total": 0,
        "pending": 0,
        "accepted": 0,
        "rejected": 0,
    }

    for row in rows:
        status = row[0]
        count = row[1]

        statistics["total"] += count

        if status == "Pending":
            statistics["pending"] = count

        elif status == "Accepted":
            statistics["accepted"] = count

        elif status == "Rejected":
            statistics["rejected"] = count

    return statistics
