from main import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.email}"
    

class MedicalTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    date_tested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, test_type, result):
        self.user_id = user_id
        self.test_type = test_type
        self.result = result

    def __repr__(self):
            return f"{self.user_id}, {self.test_type}, {self.result}, {self.date_tested}"
