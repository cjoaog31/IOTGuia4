from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
from Controladores.ControladorAdmMesas import ControladorAdmMesas
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/registraduria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)


def loadFileConfig():
 with open('config.json') as f:
     data = json.load(f)
     return data


@app.route("/",methods=['GET'])
def test():
 json = {}
 json["message"]="Server running ..."
 return jsonify(json)

@app.route("/mesas",methods=['GET'])
def getMesa():
  json=ControladorAdmMesas.index()
  return jsonify(json)

@app.route("/mesas",methods=['POST'])
def crearMesa():
    data = request.get_json()
    json = ControladorAdmMesas.create(data)
    return jsonify(json)
'''
@app.route("/mesas/<string:id>",methods=['GET'])
def getMesas(id):
  json=miControladorAdmMesas.show(id)
  return jsonify(json)
'''
@app.route("/mesas/<string:id>",methods=['PUT'])
def modificarMesa(id):
  data = request.get_json()
  json=miControladorAdmMesas.update(id,data)
  return jsonify(json)

@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarMesa(id):
  json=miControladorAdmMesas.delete(id)
  return jsonify(json)


if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])




