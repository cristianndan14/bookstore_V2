from flask import render_template, redirect, url_for

def init_errors(app):
    @app.errorhandler(401)
    def pagina_no_autorizada(error):
        return redirect(url_for('login'))

    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('errores/404.html'), 404