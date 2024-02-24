#!/usr/bin/python3
"""The flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_app():
    """calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    api_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    api_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=api_host,
        port=api_port,
        threaded=True
    )
