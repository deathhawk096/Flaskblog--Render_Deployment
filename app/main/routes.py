from flask import Blueprint
from flask import request,render_template
from app.models import Post



main=Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get("page",1,type=int)
    post=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template("home.html",posts=post)




@main.route("/about")
def about():
    return render_template("about.html")