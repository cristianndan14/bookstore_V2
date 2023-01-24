from flask import render_template, redirect, url_for

def init_errors(app):
    @app.errorhandler(401)
    def unauthorized_page(error):
        return redirect(url_for('login'))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404