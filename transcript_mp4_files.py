import whisper
import moviepy.editor as mp
import os
import time
from whisper.tokenizer import TO_LANGUAGE_CODE


# ask user to choose a video file
mp4_file_path = input("Type the path to the mp4 file you want to transcribe, and press Enter: ")
mp3_file_path = mp4_file_path[:-4] + ".mp3"
mp3_file_path = fr"{mp3_file_path}"
# convert mp4 file to mp3 if needed
if not os.path.exists(mp3_file_path):
    print("Converting mp4 file to mp3...")
    clip = mp.VideoFileClip(mp4_file_path)
    clip.audio.write_audiofile(mp3_file_path)

# ask user to choose a model
print("Available models:")
print(whisper.available_models())
model_name = input("Type the name of the model you want to use for transcription, and press Enter: ")
model = whisper.load_model(model_name, in_memory=True)
text_file_path = mp3_file_path[:-4] + "_transcript"+".txt"
if os.path.exists(text_file_path):
    os.remove(text_file_path)
# ask user to choose a language
# for key,value in TO_LANGUAGE_CODE print the language name (key) and the language code (value). e.g.: 'English' -> 'en'
for k,v in sorted(TO_LANGUAGE_CODE.items()):
    print(f"{v} -> {k}")
print("\n")

language_code = input("Type the language code you want to use for transcription from the options above, and press "
                      "Enter. \nFor English (which is the default), press Enter without typing anything: ")
if language_code == "":
    language_code = None
print("\nTranscribing...")
start = time.time()
result = model.transcribe(mp3_file_path, text_file_path=text_file_path, language=language_code)
end = time.time()
print(f"Transcription took {end-start} seconds")


