from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)


@views.route("/create-book", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        locker = (request.form.get("match"))
        if locker == "matchwithpairs":
            locker = "At Locker"
        else:
            locker = "At Home"
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id, in_locker=locker)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')

            return redirect(url_for('views.posts'))
    return render_template('create_post.html', user=current_user)



@views.route("/delete-book/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.posts'))
@views.route("/delete-book2/<id>")
@login_required
def delete_post2(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.posts2'))
@views.route("/change/<Id>")
@login_required
def Change(Id):
    post = Post.query.filter_by(id=Id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        Inlocker = post.in_locker
        if post.in_locker == "At Locker":
            Inlocker = "At Home"
        elif post.in_locker == "At Home":
            Inlocker = "At Locker"
        post.in_locker = Inlocker
        db.session.commit()
    return redirect(url_for('views.posts'))
@views.route("/change2/<Id>")
@login_required
def Change2(Id):
    post = Post.query.filter_by(id=Id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        Inlocker = post.in_locker
        if post.in_locker == "At Locker":
            Inlocker = "At Home"
        elif post.in_locker == "At Home":
            Inlocker = "At Locker"
        post.in_locker = Inlocker
        db.session.commit()
    return redirect(url_for('views.posts2'))
@views.route("/books")
@login_required
def posts():
    username = current_user.username
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)
@views.route("/HOMEbooks")
@login_required
def posts2():
    username = current_user.username
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts2.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.posts'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.posts'))
