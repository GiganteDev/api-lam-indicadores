__version__ = '1.0.0'
from flask import Flask, jsonify
import setup, dotenv, os

dotenv.load_dotenv(dotenv.find_dotenv())

app = Flask(__name__)

@app.route('/api/metas/')
def metas():
    meta = {}
    for registro in setup.registros:
        meta.update(setup.pegaIndicadores(registro, setup.registros[registro]))
    return jsonify(meta)

@app.route('/api/producao/')
def ProdLista():
    return setup.get_Plista()

if __name__ == '__main__':
    app.run(
        host = os.getenv('api_host'),
        port = os.getenv('api_port')
    )