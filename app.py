import openai
import twilio
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from twilio.rest import Client

import os

app = Flask(__name__)

openai_api_key=os.environ.get('OPENAIKEY')
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# Set up the OpenAI API client
openai.api_key = openai_api_key

client = Client(account_sid, auth_token)



'''
TODO: 
    - Add authentication for twilio phone numbers 
    - Add state for can hold conversations 

'''

# Set up a "webhook" to listen for incoming SMS messages
@app.route("/sms", methods=['GET', 'POST'])
def sms_webhook():
    resp = MessagingResponse()

    # Get the sender and body of the message
    sender = request.form["From"]
    body = request.form["Body"]

    response = openai.Completion.create(engine="text-davinci-002", prompt=body, max_tokens=1024)
    response_text = response.choices[0].text

    # Add a message
    print(sender)
    resp.message(to=sender,body=response_text, from_='+18304653338')

    message = client.messages.create(
                              body=response_text,
                              from_='+18304653338',
                              to=sender
                          )

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)