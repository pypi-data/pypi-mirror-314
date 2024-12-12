from itertools import count
from mutagen.mp3 import MP3
import os
from pydub.utils import mediainfo
from pydub import AudioSegment
import time
import io
import threading
from pydub.playback import play
import tempfile
tempfiledir='./tempfile'
os.path.exists(tempfiledir) or os.makedirs(tempfiledir)
tempfile.tempdir=tempfiledir

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from librosa.feature import melspectrogram
from librosa.display import specshow
import librosa

class CustomAudioOpt():
    def __init__(self, audio_file_path):
        self.file_path = audio_file_path
        self.suffix = os.path.splitext(audio_file_path)[-1].lower()
        self.audio = AudioSegment.from_file(self.file_path)
        self.audio_raw_data=self.audio.raw_data
        self.audio_data=self.audio.get_array_of_samples()
        # self.file_name = os.path.basename(audio_file_path)
        # self.file_size = os.path.getsize(audio_file_path)
    
    def load_audio(self, audio_file_path):
        self.file_path = audio_file_path
        self.suffix = os.path.splitext(audio_file_path)[-1].lower()
        if self.suffix in ['.mp3', '.wav', '.flac', '.ogg', '.aac']:
            self.audio = AudioSegment.from_file(self.file_path)
            self.audio_data=self.audio.get_array_of_samples()
            print(f"Audio loaded successfully from {self.file_path}")
        else:
            raise ValueError(f"Unsupported file type: {self.suffix}")
        return self
    
    def show_info(self):
        detailed_info = mediainfo(self.file_path)
        print("\nDetailed Info:")
        for key, value in detailed_info.items():
            print(f"{key}: {value}")
            
    def convert_to_wav(self,output_path,sr=48000,channels=1):
        try:
            self.audio.export(output_path, format="wav",parameters=["-ar", f"{sr}","-ac", f'{channels}'],codec="pcm_s16le")
            # self.load_audio(output_path)
            print(f"Audio converted and saved to {output_path}")
        except Exception as e:
            print(f"Error during conversion: {e}")
            
    def play_audio(self):
        # play(self.audio)#需修改NamedTemporaryFile("w+b", suffix=".wav",delete=False) 
        threading.Thread(target=play, args=(self.audio,), daemon=True).start()
        
    def plot_audio_and_mel(self):
        raw_data = np.array(self.audio_data)
        frame_rate = self.audio.frame_rate
        duration = len(raw_data) / frame_rate
        
        # Plot the raw waveform
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        time = np.linspace(0, duration, num=len(raw_data))
        plt.plot(time, raw_data)
        plt.title("Raw Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")

        # Convert AudioSegment to NumPy array and calculate Mel spectrogram
        samples = raw_data.astype(np.float32) / (2 ** (self.audio.sample_width * 8 - 1))  # Normalize PCM data
        mel_spect = melspectrogram(y=samples, sr=frame_rate, n_fft=2048, hop_length=512, n_mels=128)

        # Plot the Mel spectrogram
        plt.subplot(2, 1, 2)
        specshow(librosa.power_to_db(mel_spect, ref=np.max), sr=frame_rate, hop_length=512, x_axis='time', y_axis='mel')
        plt.title("Mel Spectrogram")
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()
            
            
mp3path=r'E:\高频常用函数\jcw_utils\audio\mp3\music\file_example_MP3_700KB.mp3'
wavpath=r'E:\高频常用函数\jcw_utils\audio\wav\instrument\Yamaha-TG77-Woodbass-C1.wav'
test=CustomAudioOpt(wavpath)
test.play_audio()
test.plot_audio_and_mel()
# test.load_audio(wavpath)
# test.play_audio()

