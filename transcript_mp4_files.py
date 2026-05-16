#!/usr/bin/env python
import argparse
import whisper
import moviepy.editor as mp
import os
import time
import numpy as np
from scipy import signal
import soundfile as sf

def simple_audio_enhancement(audio_path, output_path):
    """
    Simple but effective audio enhancement for classroom recordings.
    Uses basic signal processing without complex libraries.
    """
    print("Enhancing audio quality...")
    
    # Load audio file
    y, sr = sf.read(audio_path)
    
    # Ensure mono signal for consistent processing (average across channels if needed)
    if isinstance(y, np.ndarray) and y.ndim > 1:
        y = np.mean(y, axis=1)
    
    # 1. Apply high-pass filter to remove low-frequency noise (air conditioning, etc.)
    print("  - Removing low-frequency noise...")
    # Remove frequencies below 80 Hz
    b, a = signal.butter(4, 80, btype='high', fs=sr)

    y_filtered = signal.lfilter(b, a, y)

    # 2. Apply low-pass filter to remove high-frequency hiss
    print("  - Removing high-frequency hiss...")
    # Remove frequencies above 8000 Hz
    b, a = signal.butter(4, 8000, btype='low', fs=sr)

    y_filtered = signal.lfilter(b, a, y_filtered)

    
    
    # # 3. Simple noise gate to reduce background noise during quiet parts
    # print("  - Applying noise gate...")
    # # Calculate RMS in small windows
    # window_size = min(int(0.1 * sr), len(y_filtered) // 4)  # 100ms or 1/4 of audio length
    # threshold_factor = 0.1  # 10% of max RMS
    
    # # Calculate rolling RMS
    # pad_size = min(window_size//2, len(y_filtered)//2)
    # y_padded = np.pad(y_filtered, pad_size, mode='constant')
    # rms_values = []
    # for i in range(len(y_filtered)):
    #     start_idx = max(0, i)
    #     end_idx = min(len(y_padded), i + window_size)
    #     window = y_padded[start_idx:end_idx]
    #     if len(window) > 0:
    #         rms = np.sqrt(np.mean(window**2))
    #     else:
    #         rms = 0
    #     rms_values.append(rms)
    
    # rms_values = np.array(rms_values)
    # threshold = np.max(rms_values) * threshold_factor
    
    # # Apply noise gate
    # y_gated = np.copy(y_filtered)
    # for i, rms in enumerate(rms_values):
    #     if rms < threshold:
    #         y_gated[i] *= 0.1  # Reduce by 90% instead of complete silence

    y_gated = y_filtered
    
    # 4. Normalize audio
    print("  - Normalizing audio...")
    # Normalize to -3dB to prevent clipping while maintaining good levels
    max_val = np.max(np.abs(y_gated))
    if max_val > 0:
        y_normalized = y_gated * (0.7 / max_val)
    else:
        y_normalized = y_gated
    
    # 5. Apply gentle compression
    print("  - Applying gentle compression...")
    # Simple soft knee compression
    threshold = 0.6
    ratio = 3.0
    y_compressed = np.where(
        np.abs(y_normalized) > threshold,
        np.sign(y_normalized) * (threshold + (np.abs(y_normalized) - threshold) / ratio),
        y_normalized
    )
    
    # 6. Pre-emphasis for speech clarity
    print("  - Enhancing speech clarity...")
    pre_emphasis = 0.95
    y_final = np.append(y_compressed[0], y_compressed[1:] - pre_emphasis * y_compressed[:-1])
    
    # Final clipping prevention
    y_final = np.clip(y_final, -0.95, 0.95)
    
    # Save enhanced audio
    sf.write(output_path, y_final, sr)
    print(f"  - Enhanced audio saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe mp4 or m4a files using Whisper")
    parser.add_argument("file_path", help="Path to the mp4, m4a, or wav file")
    parser.add_argument("--model", default="base",
                        help=f"Whisper model name. Available: {whisper.available_models()} (default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code for transcription (e.g. en, he). Defaults to auto-detect.")
    parser.add_argument("--delete-enhanced", action="store_true",
                        help="Delete the enhanced audio file after transcription")
    args = parser.parse_args()

    input_file_path = os.path.normpath(args.file_path)
    base_path = os.path.splitext(input_file_path)[0]
    file_ext = os.path.splitext(input_file_path)[1].lower()
    enhanced_audio_path = None

    if file_ext == ".wav":
        audio_for_transcription = input_file_path
    else:
        mp3_file_path = base_path + ".mp3"
        enhanced_audio_path = base_path + "_enhanced.wav"

        # Convert to mp3 if needed
        if not os.path.exists(mp3_file_path):
            if file_ext == ".m4a":
                print("Converting m4a file to mp3...")
                clip = mp.AudioFileClip(input_file_path)
                clip.write_audiofile(mp3_file_path)
            else:
                print("Converting mp4 file to mp3...")
                clip = mp.VideoFileClip(input_file_path)
                clip.audio.write_audiofile(mp3_file_path)

        # Enhance audio quality for better transcription
        if os.path.exists(enhanced_audio_path):
            print("Enhanced audio already exists. Using cached enhanced file.")
            audio_for_transcription = enhanced_audio_path
        else:
            try:
                simple_audio_enhancement(mp3_file_path, enhanced_audio_path)
                print("Using enhanced audio for transcription.")
                audio_for_transcription = enhanced_audio_path
            except Exception as e:
                print(f"Audio enhancement failed: {e}")
                print("Using original audio for transcription.")
                audio_for_transcription = mp3_file_path

    model = whisper.load_model(args.model, in_memory=True)

    # Set up transcript file path
    text_file_path = base_path + "_transcript.txt"
    if os.path.exists(text_file_path):
        os.remove(text_file_path)

    print("\nTranscribing...")
    start = time.time()

    result = model.transcribe(
        audio_for_transcription,
        language=args.language,
        text_file_path=text_file_path,
    )

    end = time.time()
    print(f"Transcription took {end-start:.2f} seconds")

    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    print(f"Transcript saved to: {text_file_path}")

    if args.delete_enhanced and file_ext != ".wav" and os.path.exists(enhanced_audio_path):
        os.remove(enhanced_audio_path)
        print("Enhanced audio file deleted.")

if __name__ == "__main__":
    main()