import speech_recognition as sr
import os
import logging
from pydub import AudioSegment

logger = logging.getLogger(__name__)

async def recognize_speech(audio_file_path: str):
    try:
        audio = AudioSegment.from_file(audio_file_path)

        wav_path = audio_file_path.replace(os.path.splitext(audio_file_path)[1], '.wav')
        audio.export(wav_path, format='wav')

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                logger.info(f"Recognized speech: {text}")

                if os.path.exists(wav_path):
                    os.remove(wav_path)

                return text

            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                return None

    except Exception as e:
        logger.error(f"Error in speech recognition: {e}")
        return None
