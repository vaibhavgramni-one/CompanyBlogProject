#  inside puppycompanyblog.users.views.py file


from flask import render_template , redirect , url_for , request , flash , Blueprint
from flask_login import current_user , login_required , login_user , logout_user
from puppycompanyblog import db
from puppycompanyblog.users.forms import RegisterForm , LoginForm , UpdateForm
from puppycompanyblog.models import User , BlogPost
from puppycompanyblog.users.picture_handler import add_profile_pic

users = Blueprint('users' , __name__)

## register view ##
@users.route('/register' , methods = ['GET' , 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        user = User(email = form.email.data , username = form.username.data , password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!')

        return redirect(url_for('users.login'))


    return render_template('register.html' , form = form)

## login view ##
@users.route('/login' , methods = ['GET' , 'POST'])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if user and user.check_password(password = form.password.data):

            login_user(user)
            flash('user logged in successfully!')
            return redirect(url_for('core.home'))

    return render_template('login.html' , form = form)

## logout view ##

@users.route('/logout')
@login_required
def logout():

    logout_user()
    flash('User logout successfully !')
    return redirect(url_for('core.home'))

## update view ##

@users.route('/update' , methods = ['GET' , 'POST'])
@login_required
def update():

    form = UpdateForm()

    if form.validate_on_submit():

        if form.picture.data:
            pic = add_profile_pic(form.picture.data , current_user.username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('User updated successfully!')

        return redirect(url_for('core.home'))
    elif(request.method == 'GET'):

        form.email.data = current_user.email
        form.username.data = current_user.username

    profile_image = url_for('static' , filename = '/profile_pics' + current_user.profile_image)

    return render_template('update.html' , form = form , profile_image = profile_image)

## user's list of blogposts ##
@users.route('/<string:username>')
def user_posts(username):
    page = request.args.get('page' , 1 , type = int)
    user = User.query.filter_by(username = username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author = user).order_by(BlogPost.date.desc()).paginate(page =page , per_page = 5)
    return render_template('user_blog_posts.html' , blog_posts = blog_posts , user = user)