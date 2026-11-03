from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('main.detect'))
    if request.method == 'POST':
        name=request.form.get('name','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
        if not name or '@' not in email or len(password)<8: flash('Enter a name, valid email, and password of at least 8 characters.', 'danger')
        elif User.query.filter_by(email=email).first(): flash('An account with that email already exists.', 'warning')
        else:
            user=User(name=name,email=email); user.set_password(password); db.session.add(user); db.session.commit(); login_user(user); return redirect(url_for('main.detect'))
    return render_template('register.html')
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=User.query.filter_by(email=request.form.get('email','').strip().lower()).first()
        if user and user.check_password(request.form.get('password','')): login_user(user); return redirect(request.args.get('next') or url_for('main.detect'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')
@auth_bp.route('/logout')
def logout(): logout_user(); return redirect(url_for('main.index'))
