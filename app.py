from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    text = db.Column(db.String)

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('home.html', todo_list=todo_list)

@app.route('/add', methods = ['POST'])
def todo_add():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        add_todo = Todo(title=title, text=text)
        db.session.add(add_todo)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return 'Bu todoni qo\'shishda muammo yuz berdi'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def todo_update(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'Bu todoni yangilashda muammo yuz berdi'

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return 'Bu todoni oʻchirishda xatolik yuz berdi'

if __name__ == '__main__':
    app.run()
