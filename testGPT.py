import openai
import twilio
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

app = Flask(__name__)
openai_api_key="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"
# Set up the OpenAI API client
openai.api_key = openai_api_key

# Set up a "webhook" to listen for incoming SMS messages
@app.route("/sms", methods=['GET', 'POST'])
def sms_webhook():
    resp = MessagingResponse()

    # Get the sender and body of the message
    sender = request.form["From"]
    body = request.form["Body"]

    response = openai.Completion.create(engine="text-davinci-002", prompt=body, max_tokens=1024)
    response_text = response["choices"][0]["text"]

    # Add a message
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)