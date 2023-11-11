from flask import Flask, app

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello, World!'
    
    return app