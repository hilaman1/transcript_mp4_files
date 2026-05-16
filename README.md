# Video Transcription Tool

This tool transcribes audio from MP4, M4A, or WAV files into text using OpenAI's Whisper model. It optionally enhances audio quality before transcription using signal processing (high-pass/low-pass filtering, normalization, and compression).

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `openai-whisper`
  - `moviepy`
  - `numpy`
  - `scipy`
  - `soundfile`

Install with:
```sh
pip install -r requirements.txt
```

## Usage

```sh
python transcript_mp4_files.py <file_path> [--model MODEL] [--language LANGUAGE] [--delete-enhanced]
```

### Arguments

| Argument | Description |
|---|---|
| `file_path` | Path to the input MP4, M4A, or WAV file |
| `--model` | Whisper model to use (default: `base`). Options: `tiny`, `base`, `small`, `medium`, `large`, `large-v1`, `large-v2`, etc. |
| `--language` | Language code for transcription (e.g. `en`, `he`). Omit for auto-detect. |
| `--delete-enhanced` | Delete the intermediate enhanced WAV file after transcription |

### Examples

Transcribe an M4A file using the `large-v1` model in English:
```sh
python transcript_mp4_files.py "C:\Users\<User>\Videos\lecture_4.m4a" --model large-v1 --language en
```

Transcribe an MP4 file and clean up the enhanced audio afterward:
```sh
python transcript_mp4_files.py "C:\Users\<User>\Videos\lecture.mp4" --model medium --language en --delete-enhanced
```

Transcribe with auto language detection using the base model:
```sh
python transcript_mp4_files.py "C:\Users\<User>\Videos\lecture.wav"
```

> **Note:** Paths containing spaces must be quoted.

## Output

- The transcript is saved as `<input_filename>_transcript.txt` in the same directory as the input file.
- For non-WAV inputs, an intermediate `<input_filename>.mp3` and `<input_filename>_enhanced.wav` are created. Use `--delete-enhanced` to remove the enhanced WAV automatically.