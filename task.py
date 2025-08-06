import threading
import time
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    burst_time = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    arrival_time = db.Column(db.Integer, nullable=False)
    algorithm = db.Column(db.String(20), nullable=False)

class ScheduleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)


class Task:
    def __init__(self, name, burst_time, priority=0, arrival_time=0):
        self.name = name
        self.burst_time = burst_time
        self.priority = priority
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.waiting_time = 0

    def run(self):
        print(f"Task {self.name} started.")
        time.sleep(self.burst_time)  
        print(f"Task {self.name} completed.")

