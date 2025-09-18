from flask import Blueprint,redirect,render_template,url_for,flash,abort,request
from flask_login import login_required,current_user
from app import db
from app.models import Post
from app.post.forms import Postform




posts=Blueprint('posts',__name__)

@posts.route("/post/new",methods=['POST','GET'])
@login_required
def new_post():
    form = Postform()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content = form.content.data,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Post Has Been Created!!','success')
        return redirect(url_for('main.home'))
    return render_template("new_post.html",form=form,title="Create Post",legend="Create Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template("post.html",title=post.title,post=post)


@posts.route("/post/<int:post_id>/update_post",methods=["POST","GET"])
@login_required
def Update_post(post_id):
    form=Postform()
    post=Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        flash("Forbidden!! You don't have the permission to access the requested resource.","danger")
        return redirect(url_for('main.home'))
#        abort(403)

    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash(f"Post Edited Successfully!!",'success')
        return redirect(url_for('posts.post',post_id=post_id))
    elif request.method == "GET":
        form.title.data=post.title
        form.content.data=post.content
    return render_template("new_post.html",form=form,title=post.title,legend="Update Post")

@posts.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("You're Post has been deleted!",'success')
    return redirect(url_for('main.home'))