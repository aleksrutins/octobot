from flask import Flask, app

from octobot.reload import CodeReloader

def create_app():
    app = Flask(__name__)

    @app.route('/api/reload')
    def reload_code():
        reloader = CodeReloader()
        return reloader.reload(), { 'Content-Type': 'text/event-stream' }

    @app.route('/')
    def index():
        return 'Hello, World!'
    
    return app