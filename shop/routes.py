import os
from flask import render_template, url_for, request, redirect, session, flash
from shop import app, db
from shop.models import Author, Book, User, Review
from shop.forms import RegistrationForm, LoginForm, PaymentForm, ReviewForm
from flask_login import login_user, logout_user, LoginManager
from datetime import datetime
now = datetime.now()

@app.route("/")

@app.route("/home/<int:sort_method>")
def home(sort_method):
	if sort_method:
		if sort_method == 1:
			sort = 'price'
		elif sort_method == 2:
			sort = 'title'
		books = Book.query.order_by(sort).all()
	else:
		books = Book.query.all()
	return render_template('home.html', title='Home', books=books)
	
@app.route("/about")
def about():
	return render_template('about.html', title='About')
	
@app.route("/book/<int:book_id>", methods=['GET', 'POST'])
def book(book_id):
	form = ReviewForm()
	book = Book.query.get_or_404(book_id)
	reviews = Review.query.filter(Review.book_id == book_id)
	
	if form.validate_on_submit():
		if session['logged_in']:
			review = Review(book_id=book_id, rating=form.rating.data, review=form.review.data, username=session['username'])
			db.session.add(review)
			db.session.commit()
			flash('Thanks for taking the time to review this product!')
			return redirect(url_for('book', book_id=book_id))
		else:
			flash('You must be logged in to leave a review.')
	
	return render_template('book.html', title=book.title, book=book, reviews=reviews, form=form)
	
@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('registrationthanks'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			session['logged_in'] = True
			session['username'] = user.username
			return redirect(url_for('home', sort_method=0))
	return render_template('login.html', title='Login', form=form)
	
@app.route("/logout")
def logout():
	logout_user()
	session.pop('username', None)
	session.pop('cart', None)
	session.pop('total',None)
	session['logged_in'] = False
	return redirect(url_for('home', sort_method=0))

@app.route("/registrationthanks")
def registrationthanks():
	return render_template('registrationthanks.html', title='Thanks')
	
@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
	if "cart" not in session:
		session["cart"] = []
	session["cart"].append(book_id)
	flash("The book is added to your shopping cart!")
	return redirect("/cart")
	
@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
	if "cart" not in session:
		flash('There is nothing in your cart.')
		return render_template('cart.html', display_cart = {}, total = 0)
	else:
		items=session["cart"]
		cart = {}
		
		total_price = 0
		total_quantity = 0
		for item in items:
			book = Book.query.get_or_404(item)
			total_price += book.price
			if book.id in cart:
				cart[book.id]["quantity"] += 1
			else:
				cart[book.id] = {"quantity":1, "title":book.title, "price":book.price}
			total_quantity = sum(item['quantity'] for item in cart.values())
		return render_template("cart.html", title='Your Shopping Cart', display_cart=cart, total=total_price, total_quantity=total_quantity)
	return render_template('cart.html')
	
@app.route("/delete_book/<int:book_id>", methods=['POST'])
def delete_book(book_id):
	if 'cart' not in session:
		session["cart"] = []
	session["cart"].remove(book_id)
	flash("The book has been removed from your shopping cart!")
	session.modified = True
	return redirect("/cart")
	
@app.route("/checkout",  methods=['GET', 'POST'])
def checkout():
	form = PaymentForm()
	if form.validate_on_submit():
		flash("Thankyou, your payment was accepted.")
	return render_template("checkout.html", title="Checkout", form=form)