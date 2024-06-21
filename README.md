# Video Transcription Tool

This tool allows you to transcribe audio from a video file (MP4 format) into text using OpenAI's Whisper model. It converts the video to an audio file (MP3 format) and then transcribes the audio into a text file.

## Requirements

- Python 3.8
- `moviepy` library
- `ffmpeg` (for `moviepy` to work)

## Installation

1. Install Python 3.8 from [python.org](https://www.python.org/).
2. Install the required Python libraries:

    ```sh
    pip install moviepy
    ```

3. Ensure you have `ffmpeg` installed. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html) and follow the installation instructions for your operating system.

## Usage

1. Run the script:

    ```sh
    python transcript_mp4_files.py
    ```

2. Follow the prompts:

    - **Video File Path**: Enter the path to the MP4 file you want to transcribe.
    - **Model Selection**: Choose a Whisper model from the list of available models.
    - **Language Selection**: Select the language code for the transcription. Press Enter without typing anything for English (default).

3. The script will:

    - Convert the MP4 file to an MP3 file if it doesn't already exist.
    - Load the selected Whisper model.
    - Transcribe the audio to a text file.

4. The transcript will be saved as a text file in the same directory as the input video file, with a `_transcript.txt` suffix.
