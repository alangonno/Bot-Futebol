import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

listaDePresenca = []
listaDeAusencia = []

BOT_NUMBER_ID = "621683704371456"

MY_TOKEN = "EAAR1UnHxltEBOZC5CjMIbXR33zPnX7TsHCkppiC0fZCM5XSjwANyhFpRnc4CzZACdn8kZBnpWZAVzkZBZAjA8pvlJylWHXHGWZCph897UyBaMFswx6S9TqQv5m96RDBQqPrbcX8Bvxk4SGCdFvrtBUxRLaLgTOu4AA3ZAGzeCGzZBlzEcdN0EheRtILZBSbrcFgYI48lKGZC2rvo8UQLJIakQZA7q8WOHT6pgfLJF0vJy4S8NiCiklLMZD"

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "EAAR1UnHxltEBOZC5CjMIbXR33zPnX7TsHCkppiC0fZCM5XSjwANyhFpRnc4CzZACdn8kZBnpWZAVzkZBZAjA8pvlJylWHXHGWZCph897UyBaMFswx6S9TqQv5m96RDBQqPrbcX8Bvxk4SGCdFvrtBUxRLaLgTOu4AA3ZAGzeCGzZBlzEcdN0EheRtILZBSbrcFgYI48lKGZC2rvo8UQLJIakQZA7q8WOHT6pgfLJF0vJy4S8NiCiklLMZD")


def send_messages(to, text):
    url = f"https://graph.facebook.com/v20.0/{BOT_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {MY_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Erro ao enviar mensagem {error}")
        return None


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
            if not request.args.get('hub.verify_token') == VERIFY_TOKEN:
                return 'Verification token mismatch', 403
            return request.args['hub.challenge'], 200
        return 'Hello World', 200
    
    if request.method == 'POST':
        data = request.get_json()

        #VERIFICA SE O METODO POST É SEU OU DO USUARIO
        if data['entry'][0]['changes'][0]['value'].get('messages'):
            message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
            message_text = message_data['text']['body'].lower()
            user = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            response_text = ""

            #ENVIANDO MENSAGENS
            try:
                if message_text == "presente":
                    listaDePresenca.append(user)
                    response_text = "ADICIONADO A LISTA DE PRESENTE"
                elif message_text == "ausente":
                    listaDeAusencia.append(user)
                    response_text = "ADICIONADO A LISTA DE AUSENTES"
                    
                if response_text:
                    destination = message_data['from']
                    send_messages(destination, response_text)
            except (KeyError, IndexError) as e:
                print(f"Erro ao processar os dados: {e}. Estrutura de dados inesperada.")

        return 'OK', 200
    
if __name__ == '__main__': # Verifica se esta rodando este arquivo ou se é o app usado em modularização
    app.run(debug=True, port=5000)


