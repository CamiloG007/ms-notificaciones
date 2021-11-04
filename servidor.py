# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 22:10:46 2021

@author: JAIME
"""

# save this as app.py
from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import request
from twilio.rest import Client

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/correo")
def enviarCorreo():
    destino = request.args.get("destino")
    asunto = request.args.get("asunto")
    mensaje = request.args.get("mensaje")
    hashString = request.args.get("hash")
    print(hashString, "-", os.environ.get("email_from"))
    if hashString == os.environ.get('SECURITY_HASH'):
        message = Mail(
            from_email=os.environ.get('email_from'),
            to_emails=destino,
            subject=asunto,
            html_content=mensaje)
        print(message)
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print("ENVIADO")
            return "OK"

        except Exception as e:
            print(e.message)
            return "KO"
    else:
        print("HASH ERROR")
        return "KO"


@app.route("/sms")
def enviarSms():
    destino = request.args.get("destino")
    mensaje = request.args.get("mensaje")
    hashString = request.args.get("hash")
    print(hashString, "-", os.environ.get("email_from"))
    if hashString == os.environ.get('SECURITY_HASH'):
        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                body=mensaje,
                                from_='+16673828010',
                                to="+57"+destino
                            )

            print(message.sid)
            print("ENVIADO SMS")
            return "OK"

        except Exception as e:
            print(e.message)
            return "KO"
    else:
        print("HASH ERROR")
        return "KO"


if __name__ == "__main__":
    app.run()

# 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 <label style="color:green; border: 2px solic red ">hola mundo</label>
# project-trabajos-notificaciones  <label><h1>HOLA</h1></label>
