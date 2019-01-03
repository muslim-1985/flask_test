from flask import Blueprint
from flask import render_template
from models import Post
from .forms import PostForm
from flask import request
from flask import redirect
from flask import url_for
from app import db
from flask_security import login_required

bot = Blueprint('bot', __name__, template_folder='templates')

@bot.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect(url_for('bot.index'))

    form = PostForm()
    return render_template('bot/create_post.html', form=form)

@bot.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('bot.post_detail'), slug=slug)
    form = PostForm(obj=post)
    return render_template('bot/edit.html', post=post, form=form)

@bot.route('/')
def index():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.id.desc())

    pages = posts.paginate(page=page, per_page=2)
    return render_template('bot/index.html', posts=posts, pages=pages)

@bot.route('/<slug>')
def post_detail (slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('bot/post_detail.html', post=post, tags=tags)