import os
from flask import render_template, url_for, request, redirect
from shop import app, db
from shop.models import Author, Book, User
from shop.forms import RegistrationForm, LoginForm
from shop.models import Author, Book
from flask_login import login_user, logout_user

@app.route("/")
@app.route("/home")
def home():
	books = Book.query.all()
	return render_template('home.html', title='Home', books=books)
	
@app.route("/about")
def about():
	return render_template('about.html', title='About')
	
@app.route("/book/<int:book_id>")
def book(book_id):
	book = Book.query.get_or_404(book_id)
	return render_template('book.html', title=book.title, book=book)
	
@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('registrationthanks'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)
	
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@app.route("/registrationthanks")
def registrationthanks():
	return render_template('registrationthanks.html', title='Thanks')
	
