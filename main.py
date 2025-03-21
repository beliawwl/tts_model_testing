import logging
import os
from flask import Flask, render_template, request, send_file
from gtts import gTTS
import tempfile

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_text():
    try:
        text = request.form.get('text', '').strip()
        if not text:
            return {'error': 'Please enter some text'}, 400

        # Create temporary file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts = gTTS(text=text, lang='ru')
        tts.save(temp_file.name)

        return send_file(temp_file.name, mimetype='audio/mp3')

    except Exception as e:
        logger.error(f"Error converting text to speech: {str(e)}")
        return {'error': 'Failed to convert text to speech'}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)