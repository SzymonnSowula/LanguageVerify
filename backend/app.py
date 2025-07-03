from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Wczytanie zmiennych środowiskowych z pliku .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Dodajemy obsługę CORS dla całej aplikacji

# Klucz API z pliku .env
API_KEY = os.getenv("API_KEY")

# Funkcja do weryfikacji tłumaczenia
def verify_translation(source_text, translated_text, source_language, target_language):
    client = Groq(api_key=API_KEY)  # Autoryzacja API
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": f"In Short Answer.Check the translation of the following sentence.Check in terms of context. Source: {source_text} | Translation: {translated_text}. Source language: {source_language} | Target language: {target_language}."}
        ]
    )
    
    # Wyciągamy odpowiedź modelu
    response_data = response.choices[0].message.content
    
    return {"response": response_data}

# Endpoint API
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