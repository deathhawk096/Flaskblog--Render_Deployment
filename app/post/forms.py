from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import data_required,length




class Postform(FlaskForm):

    title = StringField("Title Of The Post",validators=[data_required(),length(min=2,max=40)])

    content=TextAreaField("Content",validators=[data_required()])

    submit=SubmitField('Post')