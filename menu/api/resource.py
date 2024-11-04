from flask import Flask, jsonify, request

from banco import identificar_veiculo_api

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/identificar_veiculo', methods=['POST'])
def identificar_veiculo():
    data = request.get_json()
    placa = data.get('placa')
    
    if not placa:
        return jsonify({"error": "Placa do veículo é necessária"}), 400

    try:
        dados_veiculo = identificar_veiculo_api(placa)
        return jsonify(dados_veiculo), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro ao identificar o veículo"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
