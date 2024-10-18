from flask import Flask, request, send_file,send_from_directory,render_template,make_response
from TTS.api import TTS
import torch
import time
from flask_cors import CORS
import io
import os
from addWatermark import *
app = Flask(__name__)
device = "cuda" if torch.cuda.is_available() else "cpu"
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data['text']

    # Initialize TTS
    tts = TTS("tts_models/en/jenny/jenny").to(device)
    file_path = "output.wav"
    tts.tts_to_file(text=text,file_path=file_path)

    original_audio, sr = sf.read("output.wav")

    watermark = np.sin(2 * np.pi * 71 * np.arange(len(original_audio)) / sr) * 0.01 

    cutoff_frequency = 10

    modified_low_freq_audio = add_watermark(original_audio, watermark, cutoff_frequency, sr)

    watermarked_audio = combine_signals(original_audio, modified_low_freq_audio, cutoff_frequency, sr)

    sf.write(file_path, watermarked_audio, sr)

    with open(file_path, 'rb') as f:
        file_content = f.read()
    response = make_response(file_content)
    response.headers.set('Content-Type', 'audio/wav')

    # remove the file
    os.remove(file_path)

    return response
if __name__ == '__main__':
    app.run(debug=True)
