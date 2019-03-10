from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f65f45fcdd0efc41239cc3ba3a59d3f8a024046d1b3806a2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1738342:a87qEXcVNzLGmMn@csmysql.cs.cf.ac.uk:3306/c1738342'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes