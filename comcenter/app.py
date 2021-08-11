from typing import Text
from flask import Flask, request
import requests
import json
from pymongo import MongoClient
import datetime as dt
import config

client = MongoClient('192.168.200.39', port= 27017, username="comcenter", password="p3Wu1Kg0Zs8O")
db =client["comcenter"]
colchat = db["chats"]
fecha_actual = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ww9oMNsM298mM3lGalrAAW6yYLEcbUhX'

#Function to access the Sender API
def callSendAPI(senderPsid, response, receivedMessage):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

    payload = {
    'recipient': {'id': senderPsid},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)

    chatMongo(senderPsid, response, receivedMessage)

def handlePostback(senderPsid, receivedPostback):

    if 'payload' in receivedPostback:

        if receivedPostback['payload'] == "si_1":
            response = {'text': '¡Entendido!'}
            callSendAPI(senderPsid, response, receivedPostback)
            respuesta = {'text': 'persec0'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "no_1":
            response = {'text': '¡Entendido!'}
            callSendAPI(senderPsid, response, receivedPostback)
            respuesta = {'text': 'tipos_asesoramiento'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "si_2":
            respuesta = {'text': 'tipo_persec'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "no_2":
            respuesta = {'text': 'crimenes_cualificados'}
            handleMessage(senderPsid, respuesta)

        # ASILO
        elif receivedPostback['payload'] == "raza_0":
            respuesta = {'text': 'proc_raza'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "religion_0":
            respuesta = {'text': 'proc_relig'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "nacion_0":
            respuesta = {'text': 'proc_nacion'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "razpol_0":
            respuesta = {'text': 'proc_razpol'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "gse_0":
            respuesta = {'text': 'proc_gse'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "otro_0":
            respuesta = {'text': 'proc_otro'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "end_0":
            respuesta = {'text': 'proc_end'}
            handleMessage(senderPsid, respuesta)

        # TIPO ASESORIA
        elif receivedPostback['payload'] == "asilo_0":
            respuesta = {'text': 'persec0'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "visau_0":
            respuesta = {'text': 'crimenes_cualificados'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "residencia_0":
            respuesta = {'text': 'proc_resid'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "pdc_0":
            respuesta = {'text': 'proc_pdc'}
            handleMessage(senderPsid, respuesta)

        # VISA U
        elif receivedPostback['payload'] == "si_3":
            respuesta = {'text': 'lista_crimenes'}
            handleMessage(senderPsid, respuesta)
        elif receivedPostback['payload'] == "no_3":
            respuesta = {'text': 'end_0'}
            handleMessage(senderPsid, respuesta)

        elif receivedPostback['payload'] == "nocomenzado_pdc":
            respuesta = {'text': 'no_comenzado'}
            handleMessage(senderPsid, respuesta)
        else:
            response = {'text': 'ERROR 404: Payload no se encuentra dentro de los posibles Postback'}
            callSendAPI(senderPsid, response, receivedPostback)


#Function for handling a message from MESSENGER
def handleMessage(senderPsid, receivedMessage):


    #check if received message contains text
    if 'text' in receivedMessage:

        if receivedMessage['text'].lower() == "empezar":
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¡Gracias por contactar con ComCenter! ¿Nos podrías indicar si te encuentras físicamente en Estados Unidos?",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Si",
                                "payload": "si_1"
                            },
                            {
                                "type": "postback",
                                "title": "No",
                                "payload": "no_1"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)

        elif "persec0" in receivedMessage['text']:
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¿Has sido víctima de algún tipo de persecusión?",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Si",
                                "payload": "si_2"
                            },
                            {
                                "type": "postback",
                                "title": "No",
                                "payload": "no_2"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)


        elif receivedMessage['text'].lower() == "hola":
            response = {'text': '¡Hola, bienvenido a ComCenter de SmartSales!, para comenzar con el proceso, por favor escribe "empezar" sin las comillas. :)'}
            callSendAPI(senderPsid, response, receivedMessage)

        
        # ASILO
        
        elif receivedMessage['text'] == "tipo_persec":
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¿Por cuál de los siguientes motivos?",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Raza",
                                "payload": "raza_0"
                            },
                            {
                                "type": "postback",
                                "title": "Religión",
                                "payload": "religion_0"
                            },
                            {
                                "type": "postback",
                                "title": "Nacionalidad",
                                "payload": "nacion_0"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": ".",
                            "buttons": [
        
                            {
                                "type": "postback",
                                "title": "Razón Política",
                                "payload": "razpol_0"
                            },
                            {
                                "type": "postback",
                                "title": "Grupo Social Específico",
                                "payload": "gse_0"
                            },
                            {
                                "type": "postback",
                                "title": "Otro",
                                "payload": "otro_0"
                            },
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)
        
        elif receivedMessage['text'].lower() == "proc_raza":

            response = {'text': 'Proceso registro Raza'}
            callSendAPI(senderPsid, response, receivedMessage)
        
        elif receivedMessage['text'].lower() == "proc_relig":

            response = {'text': 'Proceso registro Religión'}
            callSendAPI(senderPsid, response, receivedMessage)

        elif receivedMessage['text'].lower() == "proc_nacion":

            response = {'text': 'Proceso registro Nacionalidad'}
            callSendAPI(senderPsid, response, receivedMessage)
        
        elif receivedMessage['text'].lower() == "proc_razpol":

            response = {'text': 'Proceso registro Razón Política e impresión de lista de razones.'}
            callSendAPI(senderPsid, response, receivedMessage)
        
        elif receivedMessage['text'].lower() == "proc_gse":

            response = {'text': 'Proceso registro Grupo Social Específico e impresión de lista de GSEs'}
            callSendAPI(senderPsid, response, receivedMessage)

        elif receivedMessage['text'].lower() == "proc_otro":

            response = {'text': 'Otro proceso'}
            callSendAPI(senderPsid, response, receivedMessage)
        

        # OPCIONES DE PROCESOS

        elif receivedMessage['text'].lower() == "tipos_asesoramiento":
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¿En qué te podemos asesorar?",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Solicitud Asilo",
                                "payload": "asilo_0"
                            },
                            {
                                "type": "postback",
                                "title": "Visa U",
                                "payload": "visau_0"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "‏‏‎‏‏‎ ‎",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Residencia",
                                "payload": "residencia_0"
                            },
                            {
                                "type": "postback",
                                "title": "Proceso de Corte",
                                "payload": "pdc_0"
                            }

                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)

        # VISA U

        elif "crimenes_cualificados" in receivedMessage['text']:
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¿Ha sido víctima de actos criminales cualificados?",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Si",
                                "payload": "si_3"
                            },
                            {
                                "type": "postback",
                                "title": "No",
                                "payload": "no_3"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)

        # PROCESO DE CORTE
        elif receivedMessage['text'].lower() == "proc_pdc":
            response = {
                "attachment":{
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¿Hace cuánto empezó el Proceso de Corte? Porfavor escriba 'Fecha' seguido de la última fecha de su proceso. \n caso contrario seleccione 'No comenzado'.",
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "No comenzado",
                                "payload": "nocomenzado_pdc"
                            }
                            ]
                        }

                } 
            }
            callSendAPI(senderPsid, response, receivedMessage)
        
        elif receivedMessage['text'].lower() == "lista_crimenes":

            response = {'text': '¿Cuál o Cuáles? Imprime lista y selecciona alguno de ellos.'}
            callSendAPI(senderPsid, response, receivedMessage)
        
       
        elif receivedMessage['text'].lower() == "proc_resid":

            response = {'text': 'Proceso Residencia'}
            callSendAPI(senderPsid, response, receivedMessage)

       
       # PROCESO DE CORTE
    
        elif "fecha" in receivedMessage['text'].lower():

            response = {'text': 'Almacenando fecha.'}
            callSendAPI(senderPsid, response, receivedMessage)

        elif receivedMessage['text'].lower() == "no_comenzado":

            response = {'text': 'Inicio de Proceso de Corte.'}
            callSendAPI(senderPsid, response, receivedMessage)


        elif receivedMessage['text'].lower() == "end_0":

            response = {'text': 'Fin de Proceso.'}
            
            callSendAPI(senderPsid, response, receivedMessage)

        else:
            
            response = {"text": "Por favor, escribe 'empezar' sin las comillas para comenzar con el proceso."}
            callSendAPI(senderPsid, response, receivedMessage)

   
    # LIKES, STICKERS, IMÁGENES
    else:
        response = {"text": 'Este chatbot solo lee mensajes de texto.'}
        callSendAPI(senderPsid, response, receivedMessage)


def chatMongo(senderPsid, response, receivedMessage):
    if colchat["id_conversacion"] == senderPsid:

        colchat.update( {"id_conversacion" : senderPsid}, 
        {
            "$push" : { 
                "chat" :
                {
                    "usuario" : [receivedMessage['text'], fecha_actual],
                    "bot" : [response['text'], fecha_actual]
                }
            }
        })
    else:
        colchat.insert_one({
        "id_conversacion" : senderPsid,
        "fecha_inicio" : fecha_actual,
        "chat" : [
            {
                "usuario" : [receivedMessage['text'], fecha_actual],
                "bot" : [response['text'], fecha_actual]
            }
        ]})


@app.route('/', methods=["GET", "POST"])

def home():
    return 'HOME'

@app.route('/webhook', methods=["GET", "POST"])

def index():
    if request.method == 'GET':
        #do something.....
        VERIFY_TOKEN = config.VERIFY_TOKEN

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        return 'SOMETHING', 200


    if request.method == 'POST':
        #do something.....
        VERIFY_TOKEN = config.VERIFY_TOKEN

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))


        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])
                    #handlePostback(senderPsid, webhookEvent['postback'])
                elif 'postback' in webhookEvent:
                    handlePostback(senderPsid, webhookEvent['postback'])
                
                


                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404

if __name__ == '__main__':

    app.run(host='0.0.0.0', port='8888', debug=True)