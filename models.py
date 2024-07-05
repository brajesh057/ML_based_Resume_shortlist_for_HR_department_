from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)
    resume = db.Column(db.Text)
    category = db.Column(db.String(50))

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
