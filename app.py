import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

app = Flask(__name__)

# Wczytanie klucza API z .env lub z localStorage (w zależności od platformy)
API_KEY = os.getenv('API_KEY') or 'default_api_key'  # Jeśli nie ma klucza w .env, użyj domyślnego

# Funkcja weryfikacji tłumaczenia
def verify_translation(source_text, translated_text, source_language, target_language):
    client = Groq(api_key=API_KEY)
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": f"In Short Answer.Check the translation of the following sentence.Check in terms of context. Source: {source_text} | Translation: {translated_text}. Source language: {source_language} | Target language: {target_language}."}
        ]
    )
    
    # Wyciąganie odpowiedzi
    response_data = response.choices[0].message.content
    return {"response": response_data}

@app.route('/verify-translation', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        source_text = data['source_text']
        translated_text = data['translated_text']
        source_language = data['source_language']
        target_language = data['target_language']

        result = verify_translation(source_text, translated_text, source_language, target_language)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
