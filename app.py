from flask import Flask, render_template, request, redirect,session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            location TEXT,
            date TEXT,
            contact TEXT,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect('/')
        else:
            return redirect('/login')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    if not session.get('is_admin'):
        return "Unauthorized", 403

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# HOME
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    lost = c.execute("SELECT COUNT(*) FROM items WHERE type='lost'").fetchone()[0]
    found = c.execute("SELECT COUNT(*) FROM items WHERE type='found'").fetchone()[0]

    conn.close()
    return render_template('home.html', lost=lost, found=found, total=lost+found)


# ADD ITEM
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        contact = request.form['contact']
        item_type = request.form['type']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (title, description, location, date, contact, type) VALUES (?, ?, ?, ?, ?, ?)",
                  (title, description, location, date, contact, item_type))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_item.html')


# LOST ITEMS
@app.route('/lost')
def lost_items():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    items = c.execute("SELECT * FROM items WHERE type='lost'").fetchall()
    conn.close()
    return render_template('lost_items.html', items=items)


# FOUND ITEMS
@app.route('/found')
def found_items():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    items = c.execute("SELECT * FROM items WHERE type='found'").fetchall()
    conn.close()
    return render_template('found_items.html', items=items)




if __name__ == '__main__':
    app.run(debug=True)