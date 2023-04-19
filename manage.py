from flask_script import Manager, Server
from app.app import run_app
from config import config

configuracion = config['development']
app = run_app(configuracion)

manager = Manager(app)
manager.add_command('run', Server(host='127.0.0.1', port=5000))

if __name__ == '__main__':
    manager.run()
