from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:getconnected@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    return render_template('all_entries.html', title='Build A Blog!')

# @app.route('/blog')  # displays all posts
#
#
@app.route('/newpost', methods=['POST', 'GET'])  # submits new post; after submitting, redirects to main blog page
def add_post():
    if request.method == 'GET':
        return render_template('new_entry.html', title="Build A Blog!")

    if request.method == 'POST':
        entry_title = request.form['title']
        entry_body = request.form['body']
        entry_id = request.form['id']
        new_blog = Blog(entry_title, entry_body)
        db.session.add(new_blog)
        db.session.commit()

        return render_template('all_entries.html', title="Build A Blog!")



if __name__ == '__main__':
    app.run()
