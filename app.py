from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


# CREATE DATABASE
def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            aadhar TEXT UNIQUE,
            profession TEXT
        )
    """)

    conn.commit()
    conn.close()


# HOME PAGE
@app.route('/')
def index():

    return render_template('index.html')


# ADD RECORD
# ADD RECORD
@app.route('/add', methods=['POST'])
def add():

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['contact']
    aadhar = request.form['aadhar']
    profession = request.form['profession']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO people
            (name, age, gender, contact, aadhar, profession)

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, age, gender, contact, aadhar, profession)
        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        return render_template(
            'index.html',
            error="Aadhar number already exists!"
        )

    conn.close()

    return redirect('/records')


# VIEW RECORDS
@app.route('/records')
def records():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people")

    data = cursor.fetchall()

    conn.close()

    return render_template('records.html', records=data)


# DELETE RECORD
# DELETE RECORD
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # DELETE RECORD
    cursor.execute(
        "DELETE FROM people WHERE id = ?",
        (id,)
    )

    # SHIFT IDS
    cursor.execute("""
        UPDATE people
        SET id = id - 1
        WHERE id > ?
    """, (id,))

    # RESET AUTOINCREMENT
    cursor.execute("""
        DELETE FROM sqlite_sequence
        WHERE name='people'
    """)

    conn.commit()
    conn.close()

    return redirect('/records')


if __name__ == '__main__':

    init_db()
    app.run()