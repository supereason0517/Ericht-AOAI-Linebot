#from flask_ngrok import run_with_ngrok
from flask import Flask, request,abort
from linebot import LineBotApi , WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import  TextSendMessage
import json
import openai

app = Flask(__name__)
conversation_history = []

openai.api_key = "<--AzureOpenAI key-->"
openai.api_type = "azure"
openai.api_base = "<--Your Azure OpenaAI Endpoint-->"
openai.api_version = "2023-07-01-preview"
deployment_name = "<--Deployment module name-->"

line_bot_api = LineBotApi("<--Line Channel Access Token-->")
handler = WebhookHandler("<--Line Channel Secert-->") 

@app.route('/')
def home():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #333333;
                color: white;
            }
            img {
                width: 300px;
                border-radius: 8px;
                margin-top: 20px;
                margin-left: auto; /* Align the image to the right */
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Flask Azure OpenAI Project!!</h1>

        <p>This API is designed to interact with the Line messaging platform using the OpenAI Chat Completion model.</p>

        <h2>Usage:</h2>
        <ul>
            <li>Send messages to the Line API at the '/line' endpoint.</li>
            <li>To reset the conversation history, send the command '!clean' to clear the chat history.</li>
        </ul>

        <h2>Example:</h2>
        <ol>
            <li>Send a message to initiate a conversation.</li>
            <li>Use '!clean' to clear the conversation history.</li>
            <li>Continue the conversation, and the assistant will respond based on the chat history.</li>
        </ol>

        <p>Feel free to explore and interact with the API!</p>
        <h3>Made by: Stanley Shih</h3>
    </body>
    </html>
    """

@app.route('/line', methods=['POST'])
def process_text():
    global conversation_history
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    
    try:
        if 'events' in json_data and json_data['events']:  # Ensure 'events' exists and is not empty
            tk = json_data['events'][0]['replyToken']
            msg = json_data['events'][0]['message']['text']
            conversation_history.append({"role": "user", "content": msg})

            if "!clean" in msg.lower():
                conversation_history = []
                print("history cleaned")
                text_message = TextSendMessage(text="History Cleaned!!! OwO")
                line_bot_api.reply_message(tk, text_message)
                return "OK"

            answer = openai.ChatCompletion.create(
                temperature=0.5,
                max_tokens=500,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": "Your name is Ericht.You are a Cloud support agent whose primary goal is to help users with issues they are experiencing with their Microsoft 365 services and Azure Services. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Microsoft or Azure."},
                    *conversation_history  # Include the entire conversation history
                ]
            )

            # Extract the assistant's reply from the response
            reply_msg = answer['choices'][0]['message']['content']
            print(reply_msg)
            text_message = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(tk, text_message)
        else:
            # Handle the case where 'events' key is empty or not present
            print("No events found in the JSON data.")
    except InvalidSignatureError:
        abort(400)
    return 'OK'


if __name__ == "__main__":
    #run_with_ngrok(app)
    app.run()

