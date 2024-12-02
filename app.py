from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

user = 'User'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Task {self.id}>'

def create_tables():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully.")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task = Todo(content=task_content)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "[Error]: Adding task to database failed."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',user=user,tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "[Error] Problem in deleting the task."
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    to_update = Todo.query.get(id)
    if request.method == 'POST':
        to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "[Error] Error in updating the task."
    else:
        return render_template('update.html',task=to_update)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
