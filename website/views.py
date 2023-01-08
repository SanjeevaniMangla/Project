import os
from flask import Blueprint, render_template, request, send_file, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from .models import User, Post
from . import db
from werkzeug.utils import secure_filename

# i am going to define this file is a blueprint of my application which means it has a bunch of routes inside of it or URL's. Its just a way to
# separate our app out so we don't have to all our views defined in one file 

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("profile.html", user=current_user)

@views.route('/search')
@login_required
def search():
    query = request.args.get('query')
    user = User.query.filter(User.first_name.contains(query)).all()
    return render_template('search_results.html', user=user)

@views.route('/user/<int:id>')
@login_required
def user_profile(id):
    user = User.query.get(int(id))
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, posts=posts)

@views.route('/upload_post', methods=['POST'])
def upload_post():
  # Save the uploaded image file to the server
  image_file = request.files['image_file']
  filename = secure_filename(image_file.filename)
#   image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
  image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', filename))
  # Create a new Post object in the database
  post = Post(img='/static/photos/' + filename, user_id=current_user.id)

#   post = Post(img=os.path.join(current_app.config['UPLOAD_FOLDER'], filename), user_id=current_user.id)
  db.session.add(post)
  db.session.commit()

  return redirect(url_for('views.profile', username=current_user.first_name))

@views.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(first_name=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, posts=posts)

@views.route('/follow/<first_name>')
@login_required
def follow(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    if user is None:
        flash('User {} not found.'.format(first_name))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('views.profile'.format(current_user.first_name), username=first_name))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}.'.format(user.first_name))
    return redirect(url_for('views.profile'.format(current_user.first_name), username=first_name, user=user))


@views.route('/unfollow/<first_name>')
@login_required
def unfollow(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    if user is None:
        flash('User {} not found.'.format(first_name))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('views.profile'.format(current_user.first_name), username=first_name))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(user.first_name))
    return redirect(url_for('views.profile'.format(current_user.first_name), username=first_name, user=user))

@views.route('/p/<id>')
def post_detail(id):

    post = Post.query.filter_by(id=id).first_or_404()
    user=current_user
    return render_template('post_detail.html', post=post, user=user)

@views.route('/explore')
@login_required
def explore():
    global posts
    posts = list()
    user = User.query.filter_by().all()
    posts = Post.query.filter_by().all()
    return render_template('explore.html', title='Explore', posts=posts, user=user)

@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    Post.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect('/profile/{}'.format(current_user.first_name))

@views.route('/like/<int:post_id>')
def like(post_id):
    user = current_user
    post = Post.query.get(post_id)
    user.like_post(post)
    db.session.commit()
    return redirect(request.referrer)

@views.route('/dislike/<int:post_id>')
def dislike(post_id):
    user = current_user
    post = Post.query.get(post_id)
    user.dislike_post(post)
    db.session.commit()
    return redirect(request.referrer)

@views.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(first_name=username).first_or_404()
    followers = user.followers.all()
    return render_template('followers.html',user=user,followers=followers)

@views.route('/following/<username>')
def following(username):
    user = User.query.filter_by(first_name=username).first_or_404()
    following = user.followed.all()
    return render_template('following.html',user=user, following=following)














