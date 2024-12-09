"""Diarize speakers in an audio file using the Falcon API."""

import pvfalcon
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def diarize_audio(audio_file: str, access_key: str) -> list:
    """
    Perform speaker diarization on an audio file using the Falcon API.

    Parameters
    ----------
    audio_file : str
        The path to the audio file to process.
    access_key : str
        The Falcon API access key.

    Returns
    -------
    list
        A list of speaker segments with the following attributes:
        - speaker_tag: The speaker tag assigned to the segment.
        - start_sec: The start time of the segment in seconds.
        - end_sec: The end time of the segment in seconds.
    """
    falcon = pvfalcon.create(access_key=access_key)
    segments = falcon.process_file(audio_file)
    for segment in segments:
        logger.info(
            "Speaker %d: %.2f-%.2f"
            % (segment.speaker_tag, segment.start_sec, segment.end_sec)
        )
    falcon.delete()
    return segments


def merge_transcript(transcription: dict, diarization: list, overlap=0.1) -> list:
    """
    Merge speaker diarization and transcription segments.

    Parameters
    ----------
    transcription : dict
        The transcription of the audio file.
    diarization : list
        A list of speaker segments with the following attributes:
        - speaker_tag: The speaker tag assigned to the segment.
        - start_sec: The start time of the segment in seconds.
        - end_sec: The end time of the segment in seconds.
    overlap : float
        The minimum overlap threshold for merging segments (default is 0.1).

    Returns
    -------
    list
        A list of merged speaker segments with the following attributes:
        - speaker: The speaker tag assigned to the segment.
        - start: The start time of the segment in seconds.
        - end: The end time of the segment in seconds.
        - text: The text of the segment.
    """
    merged_transcript = []
    processed_segments = []

    # Merge diarization and transcription
    for segment in diarization:
        speaker = f"Speaker {segment['speaker_tag']}"

        # Loop through each segment in the transcription
        for component in transcription["segments"]:
            # Check if the segment has already been processed, if so, skip it
            if component["id"] in processed_segments:
                continue

            # Determine the overlap between the diarization and transcription segments
            overlapped_start = max(segment["start_sec"], component["start"])
            overlapped_end = min(segment["end_sec"], component["end"])
            overlap_duration = overlapped_end - overlapped_start

            if overlap_duration <= 0:
                continue

            diarization_period = segment["end_sec"] - segment["start_sec"]
            transcription_period = component["end"] - component["start"]

            min_duration = min(diarization_period, transcription_period)

            # If the overlap duration is greater than the minimum duration multiplied by the overlap threshold
            # then consider the segments as overlapping
            if overlap_duration / min_duration > overlap:
                merged_transcript.append(
                    {
                        "speaker": speaker,
                        "start": overlapped_start,
                        "end": overlapped_end,
                        "text": component["text"],
                    }
                )
                processed_segments.append(component["id"])

    # Merge consecutive segments from the same speaker
    merged_transcript.sort(key=lambda x: (x["start"], x["speaker"]))
    finished_transcript = []

    for seg in merged_transcript:
        if finished_transcript:
            same_speaker = finished_transcript[-1]["speaker"] == seg["speaker"]
            short_gap = seg["start"] - finished_transcript[-1]["end"] < 1

            if same_speaker and short_gap:
                # Extend the end time and concatenate the text
                finished_transcript[-1]["end"] = seg["end"]
                finished_transcript[-1]["text"] += " " + seg["text"]
            else:
                finished_transcript.append(seg)
        else:
            # Add the first segment to finished_transcript
            finished_transcript.append(seg)

    # Return the finished transcript after processing all segments
    return finished_transcript
