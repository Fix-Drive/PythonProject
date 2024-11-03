
from flask import Flask, request, jsonify

import banco 



app = Flask(__name__)

@app.route('/identificar_automovel', methods=["POST"])
def cadastrar_automovel():
    dados_automovel = request.get_json()

    try:
        dados_api = banco.identificar_veiculo_api(dados_automovel["placa"])
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
