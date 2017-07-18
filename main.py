from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:getconnected@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])  # displays all posts
def show_posts():
    # displays single blog post
    if request.method == 'GET' and request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('single_blog.html', title='Build A Blog!', blog=blog)

    # displays all blog posts
    if request.method == 'GET' or request.method == 'POST':
        blogs = Blog.query.all()
        return render_template('all_blogs.html', title='Build A Blog!', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])  # submits new post; after submitting, redirects to main blog page
def add_post():
    # displays the add a post form
    if request.method == 'GET':
        return render_template('new_blog.html', title="Build A Blog!")

    # form handler for new posts
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        error = "This field cannot be left blank."
        title_error, body_error = "", ""

        if not blog_title:  # if blog title is missing, render error
            title_error = error
            return render_template('new_blog.html', title="Build A Blog!", title_error=title_error, blog_body=blog_body)

        if not blog_body:  # if blog body is missing, render error
            body_error = error
            return render_template('new_blog.html', title="Build A Blog!", body_error=body_error, blog_title=blog_title)

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id
            return redirect("/blog?id={}".format(blog_id))


if __name__ == '__main__':
    app.run()
