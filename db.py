from app import app, db

#Database Initialization
with app.app_context():
    db.create_all()
