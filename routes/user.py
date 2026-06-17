from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import dao as DAO
from Misc.functions import *
from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
    if request.method == 'POST':
        _form = request.form
        email = str(_form["email"])
        password = str(_form["password"])

        if len(email) < 1 or len(password) < 1:
            return render_template('signin.html', error="Email and password are required")

        hashed = hash(password)

        # Coba login sebagai admin dulu
        from Controllers.AdminManager import AdminManager
        from Models.DAO import DAO as DAOClass
        admin_manager_local = AdminManager(dao)
        d_admin = admin_manager_local.signin(email, hashed)

        if d_admin and len(d_admin) > 0:
            session['admin'] = int(d_admin["id"])
            return redirect("/admin/")

        # Kalau bukan admin, coba login sebagai user
        d = user_manager.signin(email, hashed)

        if d and len(d) > 0:
            session['user'] = int(d['id'])
            return redirect("/")

        return render_template('signin.html', error="Email or password incorrect")

    return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')

		if len(name) < 1 or len(email)<1 or len(password)<1:
			return render_template('signup.html', error="All fields are required")

		new_user = user_manager.signup(name, email, hash(password))

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")


		return render_template('signup.html', msg = "You've been registered!")


	return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	user_manager.update(name, email, hash(password), bio, user_manager.user.uid())

	flash('Your info has been updated!')
	return redirect("/user/")