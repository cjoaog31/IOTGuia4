from flask import Flask
from flask_cors import CORS
import json
from waitress import serve
from db import db
from Routes.Candidato import candidato
from Routes.Partido import partido
from Routes.Mesa import mesa
from Routes.ResultadoCandidato import resultadocandidato
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rqiqprrhyiyetm:190e9d67244f6d8641e38d26b856f63b283c71c0b9d126503f2d13e66d8c99ab@ec2-35-168-122-84.compute-1.amazonaws.com:5432/db6l8628tb3o8s'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SQLAlchemy(app)

app.register_blueprint(candidato)
app.register_blueprint(partido)
app.register_blueprint(mesa)
app.register_blueprint(resultadocandidato)


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
