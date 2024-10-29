from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import google.generativeai as genai
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Initialize the generative AI model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Start a chat session with the model
g_model = genai.GenerativeModel('gemini-pro')
chat = g_model.start_chat(history=[])

# Create a Blueprint for the API
chat_api = Blueprint('chat_api', __name__, url_prefix='/api')
api = Api(chat_api)

# Initial instruction to the AI model
chat.send_message("From now on, you will generate questions based on requirements given by users. The question should guide students to write a code block fulfilling the specified requirements. Please ensure that your questions are clear and provide specific instructions on what the students need to do.")

class ChatAPI:
    class _QuestionGenerator(Resource):
        def post(self):
            ''' Handle generating a question based on user requirements '''
            try:
                body = request.get_json(force=True)
            except Exception as e:
                return {'message': f'Failed to decode JSON object: {e}'}, 400
            
            requirements = body.get('requirements')
            
            if not requirements:
                return {'message': 'Requirements are required'}, 400
            
            try:
                # Send requirements to the AI model and get a response
                message = f"Requirements: {requirements}\n\nGenerate a question that asks students to write a code block based on these requirements."
                response = chat.send_message(message)  # Use the chat to send message
                return jsonify({'question': response.text})  # Return the question generated by the model
            except Exception as e:
                return {'message': f'An error occurred: {e}'}, 500

# Add resources to the API
api.add_resource(ChatAPI._QuestionGenerator, '/generate-question')
