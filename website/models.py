from website import db
from flask_login import UserMixin 
from datetime import datetime

# (UserMixin - this is just a custom class that we can inherit that will give our user object somthing specific for flask login)
# flask_login is just a module that kinda helps us log users in and our user object needs to inherit from UserMixin which is what i am importing right here
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150)) 
    posts = db.relationship('Post',backref='author', lazy='dynamic',passive_deletes=True )
    posts_liked = db.relationship('Likes', backref='user', lazy='dynamic',passive_deletes=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic',passive_deletes=True)
    comment = db.relationship('Comments', backref='author', lazy='dynamic',passive_deletes=True)


    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter( followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id).order_by(Post.timestamp.desc()).limit(1)
        
        return followed.union(own).order_by(Post.timestamp.desc())

    def like_post(self, post):
        if not self.post_liked(post):
            like = Likes(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def dislike_post(self, post):
        if self.post_liked(post):
            Likes.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def post_liked(self, post):
        return Likes.query.filter(Likes.user_id == self.id,
               Likes.post_id == post.id).count() > 0
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    likes = db.relationship('Likes',backref='likes', lazy='dynamic',passive_deletes=True )
    comments = db.relationship('Comments', backref='comments', lazy='dynamic',passive_deletes=True)
    count_likes = db.Column(db.Integer)

    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete='CASCADE'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    notif = db.Column(db.String(50))
    other_user = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)








