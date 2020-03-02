# inside blogpost.views.py file #
from flask import render_template , redirect , url_for , request , flash , abort , Blueprint
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blogpost.forms import BlogPostForm
from flask_login import login_required , current_user

blog_posts = Blueprint('blog_posts' , __name__)


# create post
@blog_posts.route('/create' , methods = ['GET' , 'POST'])
@login_required
def create_post():

    form = BlogPostForm()

    if form.validate_on_submit():

        post = BlogPost(title = form.title.data , text = form.text.data , user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('core.home'))

    return render_template('create_post.html' , form = form)


# read post(blog_post view)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html' , post = blog_post)




# update post
@blog_posts.route('/<int:blog_post_id>/update', methods = ['GET' , 'POST'])
@login_required
def update(blog_post_id):

    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.text = form.text.data

        db.session.commit()
        flash('post updated successfully!')
        return redirect(url_for('core.home'))

    elif(request.method == 'GET'):

        form.text.data = post.text
        form.title.data = post.title

    return render_template('create_post.html' , title = 'updating' , form = form)

# delete post
@blog_posts.route('/<int:blog_post_id>/delete_post')
@login_required
def delete_post(blog_post_id):

    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('post deleted successfully!')

    return redirect(url_for('core.home'))


