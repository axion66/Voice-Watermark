import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter


def save_audio(filename, data, samplerate):
    sf.write(filename, data, samplerate)

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def add_watermark(audio_data, watermark_signal, cutoff, samplerate):
    low_freq_audio = lowpass_filter(audio_data, cutoff, samplerate)
    combined_signal = low_freq_audio + watermark_signal
    return combined_signal

def combine_signals(original_audio, modified_low_freq_audio, cutoff, samplerate):
    low_freq_original = lowpass_filter(original_audio, cutoff, samplerate)
    high_freq_original = original_audio - low_freq_original
    combined_audio = high_freq_original + modified_low_freq_audio
    return combined_audio




