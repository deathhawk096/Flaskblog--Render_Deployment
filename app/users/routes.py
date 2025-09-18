from flask import Blueprint,render_template,redirect,flash,url_for,request
from flask_login import login_user,logout_user,current_user,login_required
from app.users.forms import (RegistrationForm,LoginForm,update_form,
                                    RequestResetForm,ResetPasswordForm)
from app.users.utils import save_pic,send_email
from app import db,bcrypt
from app.models import User,Post

users=Blueprint('users',__name__)


@users.route("/register",methods=["POST","GET"])
def register():
    form=RegistrationForm()
    if current_user.is_authenticated:
        flash("Already Logged In","info")
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_passord=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1=User(username=form.username.data,email=form.email.data,password=hashed_passord)
        db.session.add(user1)
        db.session.commit()
        flash("Registration Successfull! You can now Log In","success")
        return redirect(url_for('users.login'))
    return render_template("register.html",form=form)
 

@users.route("/login",methods=['POST','GET'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        flash("Already Logged In","info")
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember_me.data)
            flash(f"Logged In as {user.username} Successfully","success")
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessfull! Please Check Your Email and Password","danger")
    return render_template("login.html",form=form)

@users.route("/logout")
def log_out():
    flash(f"{current_user.username} Logged Out Successfully!","success")
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",methods=["POST","GET"])
@login_required
def my_account():
    form=update_form()
    if form.validate_on_submit():
        if form.pic.data:
            picture=save_pic(form.pic.data)
#            if current_user.image_file != "default.jpg": another way to delete the pic
#                os.remove(f"D:\\VsCode\\Python\\own project\\flask_blog\\static\\profile_pics\\{current_user.image_file}")
            current_user.image_file=picture
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account Updated Successfully!!","success")
        return redirect(url_for('users.my_account'))
    elif request.method == "GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for("static",filename=f"profile_pics/{current_user.image_file}")
    return render_template("account.html",image_file=image_file,form=form)


@users.route('/user_posts/<string:username>')
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',title=f'{user.username}-Posts',user=user,posts=posts)


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    form=RequestResetForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent with the instructions to reset your password!','info')
        return redirect(url_for('users.login'))
    
    return render_template('request_form.html',title='Reset_form',form=form)


@users.route('/reset_password/<token>',methods=['POST','GET'])
def reset_password(token):
    form=ResetPasswordForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("The password has been Updated Successfully!You are now able to log in.",'info')
        return redirect(url_for('users.login'))


    return render_template('reset_password.html',title='Reset_password',form=form)