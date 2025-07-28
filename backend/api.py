from flask import Flask, request, jsonify
from flask_cors import CORS # Importar CORS
from webscraper import scrape_maps

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas as rotas (ou defina origens específicas)

@app.route("/", methods=["GET"])
def home():
    return "Hello there"


@app.route("/getResults", methods=["POST"])
def getResults():
    # Captura os dados da requisição JSON do frontend
    # As chaves correspondem às enviadas pelo JavaScript do seu frontend
    search_term = request.json.get("niche")
    region = request.json.get("region") # Ex: "São Paulo, SP"
    num_items = request.json.get("maxResults")

    # Divide a 'region' em cidade e estado para a função scrape_maps
    city_param = ""
    state_param = ""
    if region:
        parts = [p.strip() for p in region.split(',')]
        if len(parts) > 1:
            city_param = parts[0]
            state_param = parts[1]
        else:
            city_param = parts[0]
            state_param = "" # Se for apenas a cidade, o estado fica vazio

    # Chama a função de scraping com os parâmetros corretos
    scraped_data = scrape_maps(search_term, city_param, state_param, num_items)

    # Retorna os dados raspados como JSON
    return jsonify({"results": scraped_data})


if __name__ == "__main__":
    # Para desenvolvimento local:
    # certifique-se de ter a variável de ambiente OPENWEATHER_KEY configurada.
    # Ex: set OPENWEATHER_KEY=sua_chave_aqui (Windows) ou export OPENWEATHER_KEY=sua_chave_aqui (Linux/macOS)
    app.run(debug=True, port=5000)

    # Para deploy em produção, geralmente você usa um servidor WSGI como Gunicorn:
    # gunicorn api:app -w 4 -b 0.0.0.0:8000
