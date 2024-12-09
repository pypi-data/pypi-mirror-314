"""ONNX utilities for speechless."""

import onnxruntime as ort
from itertools import permutations
import librosa
import numpy as np
from tqdm import tqdm
from typing import Union


INITIAL_SAMPLE_OFFSET = 0
FRAME_STEP_SIZE = 270
NUM_SPEAKERS = 2


class PickableInferenceSession:
    """
    A picklable wrapper around the ONNX InferenceSession.
    """

    def __init__(self, model_path: str):
        """
        Initializes the ONNX InferenceSession.

        Parameters
        ----------
        model_path : str
            The path to the ONNX model file.
        """
        self.model_path = model_path
        self.sess = self._init_session(self.model_path)

    def __getstate__(self):
        """Prepares the object for pickling by only storing the model path."""
        return {"model_path": self.model_path}

    def __setstate__(self, state):
        """Restores the object from a pickled state."""
        self.model_path = state["model_path"]
        self.sess = self._init_session(self.model_path)

    def run(self, *args):
        """Forward method for running inference."""
        return self.sess.run(*args)

    def _init_session(self, model_path: str) -> ort.InferenceSession:
        """
        Initializes the ONNX Runtime session.

        Parameters
        ----------
        model_path : str
            The path to the ONNX model file.
        """
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = 1
        opts.log_severity_level = 3
        return ort.InferenceSession(model_path, sess_options=opts)


class PyannoteONNX:
    """Pyannote Speaker Diarization using ONNX model"""

    def __init__(
        self,
        sample_rate: int,
        path_to_onnx_model: str = "segmentation-3.0.onnx",
        show_progress: bool = False,
    ):
        """
        Initialize Pyannote Speaker Diarization using ONNX model

        Parameters
        ----------
        sample_rate : int
            Sample rate of th
        path_to_onnx_model : str
            Path to ONNX model
        show_progress : bool
            Show progress bar, by default False
        """
        self.sample_rate = sample_rate
        self.show_progress = show_progress
        self.num_speakers = NUM_SPEAKERS

        self.session = PickableInferenceSession(path_to_onnx_model)

    def __call__(self, x, step=None, return_chunk=False):
        """
        Perform speaker diarization

        Parameters
        ----------
        x : np.ndarray
            Audio waveform
        step : int, optional
            Step size, by default None
        return_chunk : bool, optional
            Return chunk, by default False

        Yields
        ------
        np.ndarray
            Speaker probabilities
        """
        duration_multiplier = 0.9
        # Estimate the duration from the input
        duration = self.estimate_duration(x)

        if step is None:
            step = duration // 2
        else:
            step = int(step * self.sample_rate)
        step = max(min(step, duration_multiplier * duration), duration // 2)

        windows = list(self.sliding_window(x, duration, step))
        if self.show_progress:
            progress_bar = tqdm(
                total=len(windows),
                desc="Pyannote processing",
                unit="frames",
                bar_format="{l_bar}{bar}{r_bar} | {percentage:.2f}%",
            )

        overlap = self.sample2frame(duration - step)
        overlap_chunk = np.zeros((overlap, self.num_speakers))

        for idx, (window_size, window) in enumerate(windows):
            if self.show_progress:
                progress_bar.update(1)

            ort_outs = self.session.run(None, {"input": window[None, None, :]})[0][0]

            # Exponentiate the outputs to interpret them as probabilities
            ort_outs = np.exp(ort_outs)

            # Aggregate probabilities for speaker #1 and speaker #2 only
            ort_outs[:, 1] += ort_outs[
                :, 4
            ]  # Add overlap between speaker #1 and speaker #2 to speaker #1

            ort_outs[:, 2] += ort_outs[
                :, 4
            ]  # Add overlap between speaker #1 and speaker #2 to speaker #2

            # Select only the relevant columns (speaker #1 and speaker #2)
            ort_outs = ort_outs[:, [1, 2]]

            ort_outs = self.reorder(overlap_chunk, ort_outs)
            if idx != 0:
                ort_outs[:overlap, :] = (ort_outs[:overlap, :] + overlap_chunk) / 2
            if idx != len(windows) - 1:  # noqa: WPS504
                overlap_chunk = ort_outs[-overlap:, :]
                ort_outs = ort_outs[:-overlap, :]
            else:
                ort_outs = ort_outs[: self.sample2frame(window_size), :]

            if return_chunk:
                yield ort_outs
            else:
                for out in ort_outs:  # noqa: WPS526
                    yield out

    @staticmethod
    def sample2frame(x):
        """
        Sample to frame conversion

        Parameters
        ----------
        x : int
            Sample value

        Returns
        -------
        int
            Frame value
        """
        return (x - INITIAL_SAMPLE_OFFSET) // FRAME_STEP_SIZE

    @staticmethod
    def frame2sample(x):
        """
        Frame to sample conversion

        Parameters
        ----------
        x : int
            Frame value

        Returns
        -------
        int
            Sample value
        """
        return (x * FRAME_STEP_SIZE) + INITIAL_SAMPLE_OFFSET

    @staticmethod
    def sliding_window(waveform, window_size, step_size):
        """
        Slide window over waveform

        Parameters
        ----------
        waveform : np.ndarray
            Waveform to slide window over
        window_size : int
            Window size
        step_size : int
            Step size

        Yields
        ------
        Tuple[int, np.ndarray]
            Window size and window data
        """
        windows = []
        start = 0
        num_samples = len(waveform)
        while start <= num_samples - window_size:
            windows.append((start, start + window_size))
            yield window_size, waveform[start : start + window_size]
            start += step_size
        # last incomplete window
        if num_samples < window_size or (num_samples - window_size) % step_size > 0:
            last_window = waveform[start:]
            last_window_size = len(last_window)
            if last_window_size < window_size:
                last_window = np.pad(last_window, (0, window_size - last_window_size))
            yield last_window_size, last_window

    @staticmethod
    def reorder(x, y):
        """
        Reorder the speakers and aggregate

        Parameters
        ----------
        x : np.ndarray
            Overlap chunk
        y : np.ndarray
            Speaker probabilities

        Returns
        -------
        np.ndarray
            Reordered speaker probabilities
        """
        perms = [np.array(perm).T for perm in permutations(y.T)]
        diffs = np.sum(
            np.abs(
                np.sum(np.array(perms)[:, : x.shape[0], :] - x, axis=1)
            ),  # noqa: WPS221
            axis=1,
        )
        return perms[np.argmin(diffs)]

    def estimate_duration(self, x):
        """
        Estimate the duration dynamically based on the input waveform

        Parameters
        ----------
        x : np.ndarray
            Audio waveform

        Returns
        -------
        int
            Estimated duration in samples
        """
        duration_in_seconds = len(x) / self.sample_rate
        estimated_duration = min(
            max(5, duration_in_seconds // 2), 7
        )  # Clamp between 5 and 7 seconds
        return int(estimated_duration * self.sample_rate)

    def itertracks(
        self, wav: Union[str, np.ndarray], onset: float = 0.5, offset: float = 0.5
    ):
        """
        Perform speaker diarization

        Parameters
        ----------
        wav : str or np.ndarray
            Audio waveform
        onset : float
            Onset threshold, by default 0.5
        offset : float
            Offset threshold, by default 0.5

        Yields
        ------
        Dict[str, Union[int, float]]
            Speaker tag, start second, end second
        """
        if not isinstance(wav, np.ndarray):
            wav, _ = librosa.load(wav, sr=self.sample_rate, mono=True)

        current_samples = INITIAL_SAMPLE_OFFSET  # Start with the initial offset

        is_active = [False] * (self.num_speakers)
        start = [0] * (self.num_speakers)

        # Iterate over the speaker probabilities
        for speech_probs in self(wav):
            current_samples += FRAME_STEP_SIZE  # Use FRAME_STEP_SIZE for incrementing
            for idx, prob in enumerate(speech_probs[: self.num_speakers]):

                if is_active[idx]:
                    if prob < offset:
                        yield {  # noqa: WPS220
                            "speaker_tag": idx,
                            "start_sec": round(start[idx] / self.sample_rate, 3),
                            "end_sec": round(current_samples / self.sample_rate, 3),
                        }
                        is_active[idx] = False  # noqa: WPS220
                else:
                    if prob > onset:  # noqa: WPS513
                        start[idx] = current_samples  # noqa: WPS220
                        is_active[idx] = True  # noqa: WPS220

        for idx in range(self.num_speakers):  # noqa: WPS440
            if is_active[idx]:
                yield {  # noqa: WPS220
                    "speaker_tag": idx,
                    "start_sec": round(start[idx] / self.sample_rate, 3),
                    "end_sec": round(current_samples / self.sample_rate, 3),
                }


def diarize_audio(
    audio_path: str,
    sample_rate: int = 16000,
    onset_threshold: float = 0.01,
    offset_threshold: float = 0.01,
    path_to_onnx_model: str = "segmentation-3.0.onnx",
):
    """
    Perform speaker diarization using PyannoteONNX and optionally plot VAD probabilities.

    Parameters
    ----------
    audio_path : str
        Path to the input audio file.
    sample_rate : int
        The sample rate to load the audio with, matching the model's expected rate.
    path_to_onnx_model : str
        Path to the ONNX model file.

    Returns
    -------
    None
    """
    # Initialize the PyannoteONNX model
    pyannote = PyannoteONNX(
        sample_rate,
        path_to_onnx_model,
    )
    output = []
    print("Model loaded with PyannoteONNX.")

    # Load the audio file as a waveform
    wav, sr = librosa.load(audio_path, sr=sample_rate)
    print(f"Audio loaded with sample rate: {sr}")

    # Perform diarization and print each detected segment
    print("Performing diarization...")
    for turn in pyannote.itertracks(
        wav, onset=onset_threshold, offset=offset_threshold
    ):
        output.append(turn)

    return output
