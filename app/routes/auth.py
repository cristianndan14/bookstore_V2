from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from ..models.ModeloUsuario import ModeloUsuario

from ..models.entities.Usuario import Usuario

from ..validations.password_validation import PasswordValidator

from ..consts import *



def init_auth(app, db):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            usuario = Usuario(
                None, request.form['usuario'], request.form['password'], None
            )
            usuario_logueado = ModeloUsuario.login(db, usuario)
            if usuario_logueado != None:
                login_user(usuario_logueado)
                flash(MENSAJE_BIENVENIDA, 'success')
                return redirect(url_for('index'))
            else:
                flash(LOGIN_CREDENCIALESINVALIDAS, 'warning')
                return render_template('auth/login.html')
        else:
            return render_template('auth/login.html')


    """CONTINUE BUILDING REGISTER FEATURE"""

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == "POST":
            password = request.form['password']
            usuario = request.form['usuario']

            existe = ModeloUsuario.verificar_usuario_existente(db, usuario)

            validator = PasswordValidator()
            validation = validator.validate(password, usuario)
         
            if existe:
                flash(REGISTER_USUARIOEXISTENTE, 'warning')
                return render_template('auth/register.html')
            
            if validation[0] == False:
                for e in validation[1]:
                    flash(e, 'warning')
                return render_template('auth/register.html')
                
            else:
                password_hash = generate_password_hash(password)
                usuario_nuevo = Usuario(None, usuario, password_hash, 2)
                usuario_creado = ModeloUsuario.crear_nuevo_usuario(db, usuario_nuevo)
                if usuario_creado != None:
                    flash(REGISTER_SUCCESS, 'success')
                    return redirect(url_for('login'))
                else:
                    return render_template('auth/register.html')
        else:
            return render_template('auth/register.html')

    """------------------------"""

    """ 
    GENERADOR DE CONTRASEÑAS

    @app.route('/password/<password>')
    def new_password(password):
        hash_password = generate_password_hash(password)
        return "Tu contraseña es: {0} | Tu hash es: {1}".format(password, hash_password) """

    @app.route('/logout')
    def logout():
        logout_user()
        flash(LOGOUT, 'success')
        return redirect(url_for('login'))
