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


@app.route('/blog', methods=['POST', 'GET'])  # displays all posts
def display_all():
    # Of course, the difference is that in this use case it's a GET request with query parameters. So we'll want to handle the GET requests differently, returning a different template, depending on the contents (or lack thereof) of the dictionary request.args.

    if request.method == 'GET' and request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('single_blog.html', title='Build A Blog!', blog=blog)

    if request.method == 'GET' or request.method == 'POST':
        blogs = Blog.query.all()
        return render_template('all_blogs.html', title='Build A Blog!', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])  # submits new post; after submitting, redirects to main blog page
def add_post():
    if request.method == 'GET':
        return render_template('new_blog.html', title="Build A Blog!")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        # blog_id = request.form['id']
        error = "This field cannot be left blank."
        title_error, body_error = "", ""

        if not blog_title:
            title_error = error
            return render_template('new_blog.html', title="Build A Blog!", title_error=title_error, blog_body=blog_body)

        if not blog_body:
            body_error = error
            return render_template('new_blog.html', title="Build A Blog!", body_error=body_error, blog_title=blog_title)

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            # return render_template('all_blogs.html', title="Build A Blog!")
            blog_id = new_blog.id
            return redirect("/blog?id={}".format(blog_id))
            # return render_template('single_blog.html', title="Build A Blog!", blog=new_blog)

# @app.route('/single-blog/?id=<int:id>', methods=['POST'])
# def show_single_blog():
#     blog = Blog.query.filter_by(id=id)
#     blog_id = request.args.get(id)
#     return render_template('single-blog.html', blog=blog, id=blog_id)

# @app.route('/single-blog/<int:id>', methods=['GET'])
# def show_blog(id):
#     # show the post with the given id, the id is an integer
#     # return render_template('single-blog.html/%d', % id, blog=blog)
#     id = request.args.get(id)
#     return render_template('single-blog.html', blog=blog, id=id)


if __name__ == '__main__':
    app.run()
