"""Download and extract audio from a YouTube video as an mp3 file."""

import os
import re
import subprocess  # noqa: S404
from pytubefix import YouTube
from pytubefix.cli import on_progress
import traceback


def clean_filename(title):
    """
    Clean the video title to create a valid filename.

    Parameters
    ----------
    title : str
        The original title of the video.

    Returns
    -------
    str
        A cleaned version of the title suitable for a filename.
    """
    # Convert to lowercase
    title = title.lower()

    # Replace spaces with underscores
    title = title.replace(" ", "_")

    # Remove non-alphanumeric characters except underscores
    return re.sub(r"[^a-z0-9_]", "", title)


# There is a bug with pytube that causes an error when downloading audio streams
# Therefore, we use pytubefix, which is a fork of pytube that fixes this issue
def download_and_extract_audio(video_url, output_path="data/audio", overwrite=False):
    """
    Download a YouTube video and extract the audio as a mp3 file.

    Parameters
    ----------
    video_url : str
        The URL of the YouTube video to download.
    output_path : str
        The directory where the audio file will be saved (default is 'data/audio').
    overwrite : bool
        Whether to overwrite the audio file if it already exists (default is False).

    Raises
    ------
    RuntimeError
        If the ffmpeg conversion fails.
    ValueError
        If no audio stream is available for the video.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Create a YouTube object
        yt = YouTube(video_url, on_progress_callback=on_progress)
        cleaned_title = clean_filename(yt.title)

        # Get the audio stream (check available streams instead of using first)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        if not audio_stream:
            raise ValueError("No audio stream available.")

        temp_audio_file_path = os.path.join(output_path, f"{cleaned_title}.mp4")
        final_mp3_file_path = os.path.join(output_path, f"{cleaned_title}.mp3")

        # Check if the file already exists and handle overwriting
        if os.path.exists(final_mp3_file_path):
            if overwrite:
                print(f"File {final_mp3_file_path} exists. Overwriting.")
                os.remove(final_mp3_file_path)
            else:
                print(f"File {final_mp3_file_path} already exists. Skipping download.")
                return

        # Download the audio file as .mp4
        print(f"Downloading audio from: {yt.title}")
        audio_stream.download(output_path=output_path, filename=f"{cleaned_title}.mp4")

        # Convert the downloaded file to mp3 using ffmpeg with the -y flag to automatically overwrite
        command = [
            "ffmpeg",
            "-y",
            "-i",
            temp_audio_file_path,
            "-vn",
            "-acodec",
            "libmp3lame",
            final_mp3_file_path,
        ]

        result = subprocess.run(  # noqa: S603
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )

        if result.returncode != 0:
            error_message = result.stderr.decode()
            raise RuntimeError(f"ffmpeg conversion failed: {error_message}")

        # Remove the temporary .mp4 file after conversion
        os.remove(temp_audio_file_path)

        print(f"Audio extracted and saved as: {final_mp3_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
