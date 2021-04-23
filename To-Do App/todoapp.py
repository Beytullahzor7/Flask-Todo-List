from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Monster/Desktop/To-Do App/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>") #id 1-2-3 ve daha farklı id ler olabilecegi için dinamik url olarak string:id olarak kullandık
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete #if-else in pratik hali
    db.session.commit() #Sadece 3 satır kodla veri tabanındaki bilgiyi değiştirdik ORM nin avantajından yararlanarak

    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__": #Flaskta serveri ayağa kaldırdık
    db.create_all()
    app.run(debug=True)

