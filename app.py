from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()
@app.route('/')
def show_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=data)

@app.route('/add/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                msg = "User successfully added."
        except:
            conn.rollback()
            msg = "Error occurred while adding user."
        finally:
            return redirect(url_for('show_users'))
    return render_template('add.html')

@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, id))
                conn.commit()
                msg = "User successfully updated."
        except:
            conn.rollback()
            msg = "Error occurred while updating user."
        finally:
            return redirect(url_for('show_users'))
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        data = cursor.fetchone()
        conn.close()
        return render_template('edit.html', user=data)

@app.route('/delete/<int:id>/')
def delete_user(id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            msg = "User successfully deleted."
    except:
        conn.rollback()
        msg = "Error occurred while deleting user."
    finally:
        return redirect(url_for('show_users'))

if __name__ == '__main__':
    app.run(debug=True)
