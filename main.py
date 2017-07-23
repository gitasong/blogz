from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:getconnected@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '*S#jmR^E!@FM*9hc&C74!GGpN'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'show_posts', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Successfully logged in!", 'logged_in')
            print(session)
            return redirect('/newpost')
        elif user and not user.password == password:
            flash('Invalid password', 'invalid_password')
            print(session)
            return redirect('/login')
        else:
            flash('Invalid username', 'invalid_username')
            return redirect('/login')

    return render_template('login.html')

    # if user does not have account and clicks "Create Account", they are directed to the /signup page

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data
        # if either username, password, or verify are blank, flash error message that affected fields are invalid
        # if either len(username) < 3 or len(password) <3, flash 'invalid username' or 'invalid password' message
        # if password and verify don't match, flash error message that passwords don't match

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('The username {0} is already in use. Please choose another.', 'duplicate_username')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])  # displays all posts
def show_posts():
    # displays single blog post
    if request.method == 'GET' and request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('single_blog.html', title='Blogz', blog=blog)

    # displays all blog posts
    if request.method == 'GET' or request.method == 'POST':
        blogs = Blog.query.all()
        return render_template('all_blogs.html', title='Blogz', blogs=blogs)

# owner = User.query.filter_by(username=session['username']).first()
# blogs = Blog.query.filter_by(owner=owner) (before new_blog)

@app.route('/newpost', methods=['POST', 'GET'])  # submits new post; after submitting, redirects to main blog page
def add_post():
    # displays the add a post form
    if request.method == 'GET':
        return render_template('new_blog.html', title="Blogz")

    # form handler for new posts
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        error = "This field cannot be left blank."
        title_error, body_error = "", ""

        if not blog_title:  # if blog title is missing, render error
            title_error = error
            return render_template('new_blog.html', title="Build A Blog!", title_error=title_error, blog_body=blog_body)

        if not blog_body:  # if blog body is missing, render error
            body_error = error
            return render_template('new_blog.html', title="Build A Blog!", body_error=body_error, blog_title=blog_title)

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id
            return redirect("/blog?id={}".format(blog_id))


if __name__ == '__main__':
    app.run()
