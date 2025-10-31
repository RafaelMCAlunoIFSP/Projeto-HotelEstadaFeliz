from flask import Flask
from controllers.perfil import perfil_blueprint

app = Flask(__name__)
app.register_blueprint(perfil_blueprint, url_prefix = "")

app.config['SECRET_KEY'] = 'bunda'

if __name__ == '__main__':
    app.run(debug=True)