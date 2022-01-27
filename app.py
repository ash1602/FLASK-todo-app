from flask import Flask, redirect, render_template, request
from sqlalchemy import desc
app = Flask(__name__)

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods=["get", "post"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        # print(title, desc)
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    print(alltodo)
    # return "<p>Hello, World!</p>"
    return render_template("index.html", alltodo=alltodo)

@app.route("/update/<int:sno>", methods=["get", "post"])
def Update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        # print(title, desc)
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    return render_template("update.html", alltodo=todo)
    
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)