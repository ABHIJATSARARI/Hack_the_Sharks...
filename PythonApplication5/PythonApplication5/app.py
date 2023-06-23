
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from modules.scraper import fetch_research_papers
from modules.email_sender import send_recommendation_email
import sqlite3
import smtplib
import config

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database/users.db')
    conn.row_factory = sqlite3.Row
    return conn

# User registration and settings configuration
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        interests = request.form.getlist('interests')

        # Store user information in the database
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email, interests) VALUES (?, ?, ?)',
                     (name, email, ','.join(interests)))
        conn.commit()
        conn.close()

        return 'Registration successful!'

    return render_template('index.html')

# User settings configuration
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        email = request.form['email']
        interests = request.form.getlist('interests')

        # Update user information in the database
        conn = get_db_connection()
        conn.execute('UPDATE users SET interests = ? WHERE email = ?',
                     (','.join(interests), email))
        conn.commit()
        conn.close()

        return 'Settings updated successfully!'

    return render_template('settings.html')

def send_recommendations():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    for user in users:
        name = user['name']
        email = user['email']
        interests = user['interests'].split(',')

        # Fetch relevant research papers
        papers = fetch_research_papers(interests)

        # Send recommendation email
        send_recommendation_email(name, email, papers)

# Scheduler for weekly email sending
scheduler = BackgroundScheduler()
scheduler.add_job(send_recommendations, 'interval', weeks=1)
scheduler.start()

if __name__ == '__main__':
    app.run()

