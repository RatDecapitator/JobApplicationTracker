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
    connection.close()


def get_all_applications_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM job_applications")
    rows = cursor.fetchall()

    connection.close()

    return rows


def get_application_by_id(application_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM job_applications WHERE id = ?",
        (application_id,),
    )

    row = cursor.fetchone()

    connection.close()

    return row


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
