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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wciidqnhsvfnmq:dd8c2bbe0035f0dfa14b8dd90839633bedcd4da132daabe44c74e42eefb7e945@ec2-107-23-76-12.compute-1.amazonaws.com:5432/dce9k9vbnl9ga0'
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
