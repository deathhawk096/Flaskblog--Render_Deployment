from itsdangerous import URLSafeTimedSerializer as Serializer
from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)

    username=db.Column(db.String(20),unique=True,nullable=False)

    email=db.Column(db.String(120),unique=True,nullable=False)

    password=db.Column(db.String(60),nullable=False)

    image_file=db.Column(db.String(300),nullable=True,default='https://res.cloudinary.com/dpqj7lbrj/image/upload/v1758270767/default_zb1f4a.jpg')
    

    posts=db.relationship('Post',backref='author',lazy=True)




    def get_reset_token(self):
        s=Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token,expires_sec=1800):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            # loads returns the original payload; extract the 'user_id' value)
            user_id=s.loads(token,expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User ('{self.id}','{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    title=db.Column(db.String(40),nullable=False)

    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    content=db.Column(db.String(500),nullable=False)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"