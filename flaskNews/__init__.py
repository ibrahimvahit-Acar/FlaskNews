from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'f4bee220cdf2593aee24b87089fd6275'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)    
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'























from flaskNews import routes