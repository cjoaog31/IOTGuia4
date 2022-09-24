from flask import Flask
from flask_cors import CORS
import json
from waitress import serve
from db import db
from Routes.Registro import registro
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eutkfugswkrajr' \
                                        ':043eb67db576a61f211f1b317483c0558abe3d74f57929d6b34f02ae4cdf2d93@ec2-3-214' \
                                        '-2-141.compute-1.amazonaws.com:5432/d8jqbih468nvko '
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SQLAlchemy(app)

app.register_blueprint(registro)


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
