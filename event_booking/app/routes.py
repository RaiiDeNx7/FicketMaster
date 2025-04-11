from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/events')
def events():
    return render_template('events.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # for admin or user-specific content
