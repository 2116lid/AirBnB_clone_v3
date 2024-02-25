#!/usr/bin/python3
"""The flask web application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_app(exception):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def err_handle(exception):
    """
    handles 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    err_code = jsonify(data)
    err_code.status_code = 404

    return(err_code)


if __name__ == "__main__":
    app.run(os.getenv("HBNB_API_HOST"), os.getenv("HBNB_API_PORT"))
