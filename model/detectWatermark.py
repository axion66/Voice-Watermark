import numpy as np
import soundfile as sf
from scipy.fft import fft, fftfreq
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal
from flask import Flask, request, jsonify
from flask_cors import CORS
import io
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/detect', methods=['POST'])
def detect_watermark(watermark_freq=71, threshold=1e-3):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_content = file.read() # as file is IO bytes?
    
    #audio_data, sr = sf.read(file_content)
    try:
        audio_data, sr = librosa.load(io.BytesIO(file_content), sr=None)
    except Exception as e:
        return jsonify({"error": f"Error loading audio file: {str(e)}"}), 400

    t = np.arange(len(audio_data)) / sr # frames / sr 

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400


    watermark = np.sin(2 * np.pi * watermark_freq * t) / np.max(np.abs(np.sin(2 * np.pi * watermark_freq * t)))


    audio_data = audio_data / np.max(np.abs(audio_data))
    
    
    correlation = signal.correlate(audio_data, watermark, mode='valid')
    max_correlation = np.max(np.abs(correlation / len(audio_data)))
    
    
    watermarked = "1" if max_correlation > threshold else "-1"
    return jsonify({
            "is_detected": watermarked,
           # "correlation": float(correlation)
    })

    # watermark = np.sin(2 * np.pi * 71 * np.arange(len(original_audio)) / sr) * 0.01 

if __name__ == '__main__':
    app.run(debug=True, port=5001)