import json
import torch
from transformers import pipeline
import os

def load_or_download_model(model_id, model_dir="model"):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, model_id.replace("/", "_"))

    if not os.path.exists(model_path):
        print(f"Downloading model {model_id}...")
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            model_kwargs={"attn_implementation": "sdpa"} if torch.cuda.is_available() else {},
            batch_size=8,
            trust_remote_code=True,
        )
        pipe.model.save_pretrained(model_path)
        print(f"Model saved to {model_path}")
    else:
        print(f"Loading model from {model_path}")
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            model_kwargs={"attn_implementation": "sdpa"} if torch.cuda.is_available() else {},
            batch_size=8,
            trust_remote_code=True,
        )

    return pipe

def transcribe_audio_with_diarization(mp3_path, output_json_path, num_speakers=None, add_punctuation=False):
    model_id = "kotoba-tech/kotoba-whisper-v2.2"
    pipe = load_or_download_model(model_id)

    result = pipe(mp3_path, chunk_length_s=15, num_speakers=num_speakers, add_punctuation=add_punctuation)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def main():
    mp3_folder = 'mp3'
    output_folder = 'output_json'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(mp3_folder):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(mp3_folder, filename)
            output_json_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.json')
            transcribe_audio_with_diarization(mp3_path, output_json_path, num_speakers=2, add_punctuation=True)

if __name__ == "__main__":
    main()