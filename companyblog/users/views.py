# users/views.py copied
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.google import make_google_blueprint, google
from companyblog import db
from companyblog.models import User, BlogPost
from companyblog.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic


###########################################################################
#### IMPORTANT NOTE!!! HERE IS SOME CODE FOR THIS TO WORK LOCALLY ########
#### YOU SHOULD ONLY NEED THIS CODE FOR LOCAL TESTING  ##################
#### PLEASE REFER TO THE FLASK_DANCE DOCS FOR MORE INFO ################
#######################################################################
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = 'true'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = 'true'
#######################################################################
#######################################################################


users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):

            login_user(user)
            flash('Log in Success! You can create posts now! ')

            # next = request.args.get('next')
            #
            # if next ==None or not next[0]=='/':
            #     next = url_for('core.index')

            return redirect(url_for('core.index'))

    return render_template('login.html',form=form)

# login with google
@users.route('/oalogin/google',methods=['GET','POST'])
def oalogin_google():
    if not google.authorized:
        return redirect(url_for('users.google.login'))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()['email']
    username = email.split('@')[0]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email,
                    username=username,
                    password=username)

        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('core.index'))

# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)

