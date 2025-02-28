from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import pandas as pd
import sqlite3
from execute_query import execute_query  # Import query execution function
from generate_sql_query import generate_sql_query  # Import NLP to SQL function

app = Flask(__name__)
app.secret_key = '143415'  # Required for session management

# Correct dataset path (CSV files)
DATASET_FOLDER = r"your dataset file path" #your dataset file path
DATABASE_FILE = "college.db"

# Initialize the SQLite database
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    dob TEXT NOT NULL
)
''')
conn.commit()

# Load available CSV files and create corresponding tables
available_dbs = [f.replace(".csv", "") for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]
for db_name in available_dbs:
    csv_path = os.path.join(DATASET_FOLDER, f"{db_name}.csv")
    df = pd.read_csv(csv_path)
    
    columns = ", ".join([f'"{col}" TEXT' for col in df.columns])  # Assuming text format for simplicity
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{db_name}" ({columns});'
    cursor.execute(create_table_query)

    for _, row in df.iterrows():
        placeholders = ", ".join(["?" for _ in df.columns])
        insert_query = f'INSERT INTO "{db_name}" VALUES ({placeholders});'
        cursor.execute(insert_query, tuple(row))

conn.commit()

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', databases=available_dbs)  # Show index if logged in
    return redirect(url_for('login'))  # Redirect to login if not logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['email'] = email  # Save email in session
            return redirect(url_for('index'))  # Redirect to index after login
        else:
            flash('Invalid email or password')  # Show error if invalid
    return render_template('login.html')  # Render login page if not POST or invalid credentials

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        dob = request.form['dob']
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (first_name, last_name, email, password, username, dob) VALUES (?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, email, password, username, dob))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email or username already exists.')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    data = request.json
    user_query = data.get("user_query")
    db_name = data.get("db_name")

    if not user_query or not db_name:
        return jsonify({"error": "Invalid input"}), 400

    try:
        sql_query = generate_sql_query(user_query, db_name)  # Generate SQL query
        return jsonify({"sql_query": sql_query})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute_query', methods=['POST'])
def execute_sql():
    def df_to_tailwind_table(df):
        """Convert a DataFrame to a Tailwind CSS styled HTML table."""
        if df.empty:
            return "<p class='text-white'>No results found.</p>"

        html = '<table class="min-w-full divide-y divide-gray-700 table-auto border border-gray-600">'
        
        # Header
        html += '<thead class="bg-gray-700"><tr>'
        for col in df.columns:
            html += f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border border-gray-600">{col}</th>'
        html += '</tr></thead>'
        
        # Body
        html += '<tbody class="bg-gray-800 divide-y divide-gray-700">'
        for _, row in df.iterrows():
            html += '<tr>'
            for col in df.columns:
                html += f'<td class="px-6 py-4 whitespace-nowrap text-sm text-white border border-gray-600">{row[col]}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        
        return html

    data = request.json
    sql_query = data.get("sql_query")
    
    if not sql_query:
        return "No SQL query provided", 400
    
    try:
        results_df = execute_query(sql_query)  # This returns a DataFrame
        results_html = df_to_tailwind_table(results_df)  # Convert to Tailwind HTML table
        return results_html  # Return HTML string directly
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
