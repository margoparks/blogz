from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:GoGreenLiving789@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'MsZ=,C^mH3ps>'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column (db.Integer, db.ForeignKey('user.id'))
    
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner 

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref = 'owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

def verify_space(text):
    spaces = False
    for char in text:
        if char.isspace():
            spaces = True
    return spaces

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if verify_space (username):
            flash("Username cannot contain blanks")
            return render_template('register.html')
        elif verify_space (password):
            flash("Password cannot contain blanks")
            return render_template('register.html')
        elif password != verify:
            flash("Password does not match")
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("This username already exists")
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in to Blogz")
            return redirect('/newpost')
        elif user and user.password != password:
            flash("Invalid password")
            return render_template('login.html', name = "Login")
        elif user and user.username != username:
            flash("Invalid username")
            return render_template('login.html', name = "Login")
        elif not user:
            flash("This user does not exist. Please register for an account")
            return render_template('login.html')

    session['username'] = username
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect ('/blog')
    

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get("id")
    

    if id:
        blog = Blog.query.get(id)
        users = Blog.query.filter_by().all()
        user = User.query.filter_by().all()
        #TODO - get the hyperlink to author to become visible 
        return render_template('blog-post.html', blog = blog, users = users, user = user)      
    if 'user' in request.args:
        user = request.args.get("user")
        users = User.query.get(user)
        blogs = Blog.query.filter_by(owner = users)
        return render_template('singleUser.html', name = "User's Blogz" , blogs = blogs)
    else:
        blogs = Blog.query.filter_by().all()
        user = User.query.filter_by().all()
        return render_template('listings.html', name = 'Blogz', blogs = blogs, user = user )
        

@app.route('/', methods=['POST', 'GET'])
def index():

    users = User.query.filter_by().all()
    return render_template('index.html', name='Home', users = users)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    owner = User.query.filter_by(username = session['username']).first()

    if request.method == 'POST':
        blog_title = request.form["title"]
        blog_body =  request.form["body"]
        blog_id = request.form['id']
        new_blog=Blog(blog_title, blog_body, owner)
        db.session.add(new_blog)
        db.session.commit()
    
        blog = Blog.query.filter_by(owner = owner).all()
        return redirect("./blog?id=" + str(new_blog.id))
    else:
        return render_template('new-post.html', name = 'New Post')


if __name__ == '__main__':
    app.run()
