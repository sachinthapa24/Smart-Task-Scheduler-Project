from flask import Flask, render_template, request
from task import db, TaskModel, ScheduleModel, Task
from Scheduler import round_robin, sjf, priority_scheduling
from utils import log_execution
from gantt import draw_gantt_chart
import uuid
import os
import webbrowser
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tasks = []
        names = request.form.getlist("name")
        burst_times = request.form.getlist("burst_time")
        priorities = request.form.getlist("priority")
        arrival_times = request.form.getlist("arrival_time") 
        algorithm = request.form["algorithm"]
        tq = request.form.get("time_quantum", type=int)

        if not all(at.isdigit() and int(at) >= 0 for at in arrival_times):
            return "Invalid arrival times. Please enter non-negative integers."

        if algorithm == "rr":
            if tq is None or tq <= 0:
                return "Time Quantum is required and must be a positive integer for Round Robin scheduling."

        # Clear any previous schedule entries if needed
        # db.session.query(ScheduleModel).delete()
        # db.session.query(TaskModel).delete()

        # Save tasks to both Task object (for algorithm) and TaskModel (for DB)
        for name, bt, pr, at in zip(names, burst_times, priorities, arrival_times):
            task = Task(name, int(bt), int(pr), int(at))
            tasks.append(task)

            db_task = TaskModel(
                name=name,
                burst_time=int(bt),
                priority=int(pr),
                arrival_time=int(at),
                algorithm=algorithm
            )
            db.session.add(db_task)

        db.session.commit()

        # Run selected scheduling algorithm
        if algorithm == "rr":
            schedule = round_robin(tasks, tq)
        elif algorithm == "sjf":
            schedule = sjf(tasks)
        elif algorithm == "priority":
            schedule = priority_scheduling(tasks)
        else:
            return "Invalid Algorithm!"

        # Save schedule to DB
        for task_name, start, end in schedule:
            task_model = TaskModel.query.filter_by(name=task_name).first()
            if task_model:
                db_schedule = ScheduleModel(
                    task_id=task_model.id,
                    start_time=start,
                    end_time=end
                )
                db.session.add(db_schedule)

        db.session.commit()

        # Draw Gantt chart
        filename = f"{uuid.uuid4().hex}.png"
        chart_path = os.path.join("static", filename)
        draw_gantt_chart(schedule, output_file=chart_path)

        return render_template("result.html", schedule=schedule, chart_file=filename)

    return render_template("index.html")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, open_browser).start()
    app.run(debug=True)
