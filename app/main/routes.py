from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_user, current_user, login_required,logout_user
from app.models import User,db
from app.forms import LoginForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/projects')
def projects():
    return render_template('projects.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # ✅ Fixed

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')  # 👈 handle redirects
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash("you have been logged out",'info')
    return redirect(url_for('main.login'))

@main.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        # checking username and password cannot be empty
        if not username:
            flash('Username cannot be empty', 'danger')
            return redirect(url_for('main.register'))

        if len(password) < 6:
            flash('Password must have at least 6 characters.', 'danger')
            return redirect(url_for('main.register'))
        
        # checking if username exits
        if User.query.filter_by(username=username).first():
            flash('username already exists', 'danger')
            return redirect(url_for('main.register'))

        # checking user and hash password
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')