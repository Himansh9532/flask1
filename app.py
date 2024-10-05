from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///himanshu.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()  # Ensure allTodo is always available
    return render_template('index.html', allTodo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")


 # Renders an update form
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    # Query the existing todo item
    todo = Todo.query.filter_by(sno=sno).first()

    # Check if the todo exists
    if not todo:
        return "Todo not found", 404  # Handle case where todo is not found

    if request.method == 'POST':
        # Update the existing todo's attributes
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()  # Commit the changes
        return redirect("/")  # Redirect to home

    return render_template('update.html', todo=todo)  # Render the update form


if __name__ == "__main__":
    app.run(debug=True)
