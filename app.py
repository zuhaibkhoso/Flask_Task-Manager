from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Flask App Initialization 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Task_Manager.db'
db = SQLAlchemy(app)


# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return '<task %r' % self.id
    

# Home Page
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html")
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


# Update Page
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html")
    else:
        return render_template("update.html", task=task)


# Delete Page
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)