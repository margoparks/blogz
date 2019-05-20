from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    id = request.args.get("id")
    if not id:
        blogs = Blog.query.filter_by().all()
        return render_template('listings.html', name = 'Home Blog', blogs = blogs)
    else:
        blog = Blog.query.get(id)
        return render_template('blog-post.html', blog = blog)
    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form["title"]
        blog_body =  request.form["body"]
        blog_id = request.form['id']
        new_blog=Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
    
        blog = Blog.query.filter_by().all()
        return redirect("./blog?id=" + str(new_blog.id))
    else:
        return render_template('new-post.html', name = 'New Post')


if __name__ == '__main__':
    app.run()
