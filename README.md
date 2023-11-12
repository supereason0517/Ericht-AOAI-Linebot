# Flask Azure OpenAI with Linebot Project

Welcome to the Flask Azure OpenAI Project! This project is designed to interact with the Line messaging platform using the OpenAI Chat Completion model.

## Overview

This Flask application integrates with the Line messaging platform to create a chatbot powered by the OpenAI Chat Completion model. Users can send messages to the Line API at the '/line' endpoint, and the chatbot responds based on the conversation history.

## Usage

- Send messages to the Line API at the '/line' endpoint.
- To reset the conversation history, send the command '!clean' to clear the chat history.

## Example

1. Send a message to initiate a conversation.
2. Use '!clean' to clear the conversation history.
3. Continue the conversation, and the assistant will respond based on the chat history.

Feel free to explore and interact with the API!

## Setup

### Prerequisites

- Python 3.10
- Flask
- Line Developer Channel (for Line Channel Access Token and Line Channel Secret)
- Azure OpenAI subscription (for Azure OpenAI key and deployment module name and Azure OpenaAI Endpoint)
- Replace placeholders like `<Your Line Channel Access Token>`, `<Your Line Channel Secret>`, `<Your Azure OpenAI key>`, `<Your Azure OpenAI deployment module name>`,`<Your Azure OpenaAI Endpoint>`


Made with ❤️ by Stanley Shih
