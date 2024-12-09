"""Transcribe audio files using the OpenAI API."""

from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)


def transcribe_audio(audio_file) -> dict:
    """
    Transcribe an audio file using the OpenAI API.

    Parameters
    ----------
    audio_file : file-like object
        The audio file to transcribe.

    Returns
    -------
    dict
        The transcription of the audio file in segments.
    """
    client = OpenAI()

    try:
        # Transcribe the audio using OpenAI API
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    except Exception as e:
        logger.error(f"Failed to transcribe audio: {e}")
        return {}

    return transcript.to_dict()


def transcribe_audio_and_write(audio_file, destination_path: str):
    """
    Transcribe an audio file using the OpenAI API and write the transcription to a file.

    Parameters
    ----------
    audio_file : file-like object
        The audio file to transcribe.
    destination_path : str
        The full path (including filename) where the transcription will be saved.
    """
    transcription = transcribe_audio(audio_file)

    # Extract the transcription text
    transcription_text = transcription.get("text", "")

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    # Write the transcription to the destination file
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(transcription_text)
