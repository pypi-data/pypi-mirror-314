from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import os
import shutil
import pkg_resources
import logging
from gtts import gTTS
import os

   
class UrduSpeech:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_ffmpeg(self):
        """
        Checks if ffmpeg is installed.
        """
        return shutil.which("ffmpeg") is not None

    def install_ffmpeg(self):
        """
        Installs ffmpeg if not already installed.
        """
        print("ffmpeg is not installed. Please install it to continue on your pc and set environment variable path.")
        # Provide instructions to the user for installing ffmpeg

    def text_to_speech(self, text, output_folder='.', output_file_name='output', format='mp3'):
        """
        Converts Urdu text to speech and saves it as an audio file with the specified format in the specified folder.
        """
        try:
            if not text.strip():
                print("Error: Input text is empty.")
                return

            supported_formats = ['mp3', 'wav', 'ogg']
            if format not in supported_formats:
                print(f"Error: Output file format '{format}' is not supported.")
                return

            output_file_name = f"{output_file_name}.{format}"
            output_path = os.path.join(output_folder, output_file_name)

            tts = gTTS(text=text, lang='ur', slow=False)
            tts.save(output_path)

            print(f"Speech saved to {output_path}")
            return output_path

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def speech_to_text(self, audio_file, format='mp3'):
        if not self.check_ffmpeg():
            self.install_ffmpeg()
            return

        if not os.path.exists(audio_file):
            return "Error: Audio file does not exist."

        if format not in ['mp3', 'wav']:
            return "Error: Invalid audio format. Supported formats are 'mp3' and 'wav'."

        recognizer = sr.Recognizer()

        if format != 'wav':
            wav_file = 'temp.wav'
            self.convert_audio_format(audio_file, wav_file, 'wav')
            audio_file = wav_file

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='ur-PK')
            return text
        except sr.UnknownValueError:
            return "Error: Speech Recognition could not understand the audio."
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"
        finally:
            if format != 'wav' and os.path.exists(wav_file):
                os.remove(wav_file)

    def convert_audio_format(self, input_file, output_file, format):
        """
        Converts an audio file to the specified format.
        """
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=format)