import os


class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    VERIFIED_SENDER_EMAIL = os.environ.get('VERIFIED_SENDER_EMAIL')

