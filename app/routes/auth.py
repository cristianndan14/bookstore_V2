from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from ..models.UserModel import UserModel

from ..models.entities.users import User

from ..validations.password_validation import PasswordValidator

from ..consts import *



def init_auth(app, db):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User(
                None, username, password, None, None, None, None
            )
            logged_user = UserModel.login(db, user)
            if logged_user != None:
                login_user(logged_user)
                flash(WELCOME_MESSAGE, 'success')
                return redirect(url_for('index'))
            else:
                flash(LOGIN_INVALIDCREDENTIALS, 'warning')
                return render_template('auth/login.html')
        else:
            return render_template('auth/login.html')
            

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == "POST":
            password = request.form['password']
            username = request.form['username']
            email = request.form['email']
            name = request.form['name']
            last_name = request.form['last_name']

            existing_user = UserModel.verify_user(db, username)

            validator = PasswordValidator()
            validation = validator.validate(password, username)
         
            if existing_user:
                flash(REGISTER_USERINVALID, 'warning')
                return render_template('auth/register.html')
            
            if validation[0] == False:
                for e in validation[1]:
                    print(e)
                    flash(e, 'warning')
                return render_template('auth/register.html')
                
            else:
                password_hash = generate_password_hash(password)
                new_user = User(None, username, password_hash, 2, email, name, last_name)
                push_user = UserModel.create_user(db, new_user)
                if push_user != None:
                    flash(REGISTER_SUCCESS, 'success')
                    return redirect(url_for('login'))
                else:
                    return render_template('auth/register.html')
        else:
            return render_template('auth/register.html')

    """------------------------"""

    
    # GENERADOR DE CONTRASEÑAS

    """ @app.route('/password/<password>')
    def new_password(password):
        hash_password = generate_password_hash(password)
        return "Tu contraseña es: {0} | Tu hash es: {1}".format(password, hash_password) """

    @app.route('/logout')
    def logout():
        logout_user()
        flash(LOGOUT, 'success')
        return redirect(url_for('login'))
