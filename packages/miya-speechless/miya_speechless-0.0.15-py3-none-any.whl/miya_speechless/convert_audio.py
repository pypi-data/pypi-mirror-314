"""
This module provides a utility function to convert audio files from one format to another using the `pydub` library.

The function `convert_audio` allows for easy conversion between
different audio formats by specifying an input file, an output file,
and an optional output format.
"""

from pydub import AudioSegment
import os
from typing import Optional


def convert_audio(
    input_path: str, output_path: str, output_format: Optional[str] = None
) -> None:
    """
    Convert an audio file from any supported format to another format.

    Parameters
    ----------
    input_path : str
        Path to the input audio file.
    output_path : str
        Path where the output audio file will be saved.
        The file extension determines the output format unless `output_format` is specified.
    output_format : Optional[str], default=None
        Desired output format (e.g., 'wav', 'flac', 'mp3').
        If not provided, the format is inferred from the `output_path` extension.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If the input or output file does not have a valid extension to determine its format.

    Examples
    --------
    Convert MP3 to WAV:

    >>> convert_audio("example.mp3", "example_converted.wav")

    Convert M4A to FLAC:

    >>> convert_audio("example.m4a", "example_converted.flac")

    Convert WAV to MP3 by specifying the output format:

    >>> convert_audio("example.wav", "example_converted.mp3", output_format="mp3")

    Convert any supported format to another by ensuring correct extensions:

    >>> convert_audio("example.ogg", "example_converted.aac")
    """
    try:
        # Validate input file existence
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file '{input_path}' does not exist.")

        # Infer input format from the file extension
        input_extension = os.path.splitext(input_path)[1]
        if not input_extension:
            raise ValueError("Input file must have a valid extension.")
        input_format = input_extension[1:].lower()

        # Determine output format
        if output_format:
            fmt = output_format.lower()
            # Ensure output_path has the correct extension
            output_extension = os.path.splitext(output_path)[1]
            if output_extension.lower() != f".{fmt}":
                output_path = os.path.splitext(output_path)[0] + f".{fmt}"
        else:
            output_extension = os.path.splitext(output_path)[1]
            if not output_extension:
                raise ValueError("Output file must have a valid extension.")
            fmt = output_extension[1:].lower()

        # Load the audio file with the inferred input format
        audio = AudioSegment.from_file(input_path, format=input_format)

        # Export the audio in the desired format
        audio.export(output_path, format=fmt)
        print(f"Successfully converted '{input_path}' to '{output_path}'")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error converting '{input_path}': {e}")
