from flask import Flask, request, jsonify, session, url_for
from flask_cors import CORS
import boto3
import json
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure Flask Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-session')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Initialize Flask Session
from flask_session import Session
Session(app)

CORS(app, resources={r"/*": {"origins": "*"}})   # for development

region = 'us-west-2'
boto3_session = boto3.session.Session(region_name=region)
bedrock = boto3_session.client(service_name='bedrock-runtime')

MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model_arn = f'arn:aws:bedrock:{region}::foundation-model/{MODEL_ID}'

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/fortune', methods=['POST'])
def get_fortune():
    try:
        print("Received request for fortune")
        data = request.get_json()
        print(data)
        user_input = data.get('input', '')
        print(user_input)
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
            
        # Create prompt for Claude model
        prompt = f"""
        Based on this input: "{user_input}", 
        generate a short, insightful fortune cookie wisdom (maximum 100 characters).
        Make it thoughtful and relevant to the input.
        
        """

        print(f"Generated prompt: {prompt}")
        
        # Call Bedrock with Claude model
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "temperature": 0,
                "top_p": 0.999,
                "top_k": 250,
                "stop_sequences": [],
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                 "text": prompt
                            }
                        ]
                    }
                ]
            })
        )
        
        response_body = json.loads(response.get('body').read())
        output_list = response_body.get("content", [])
        # Ensure response format handling is robust
        if output_list and isinstance(output_list, list):
            wisdom = output_list[0].get("text", "").strip()
        else:
            wisdom = ""

        # fortune = response_body.get('content')[0].get('text').strip()
        print(f"Generated wisdom: {wisdom}")
        return jsonify({"wisdom": wisdom}), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))