from main import app
from task import db

with app.app_context():
    db.create_all()
    print("Database created successfully.")
