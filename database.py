import sqlite3

def get_analyses():
    connection = sqlite3.connect("phishlens.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM analyses
    """)

    analyses = cursor.fetchall()

    connection.close()

    return analyses




import sqlite3
from datetime import datetime


def save_analysis(sender, subject, score, risk):
    connection = sqlite3.connect("phishlens.db")
    cursor = connection.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO analyses (sender, subject, score, risk, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (sender, subject, score, risk, created_at))

    connection.commit()
    connection.close()


def get_analyses():
    connection = sqlite3.connect("phishlens.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM analyses
    """)

    analyses = cursor.fetchall()

    connection.close()

    return analyses