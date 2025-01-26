import glob
import os
from reazonspeech.k2.asr import load_model, transcribe, audio_from_path

mp3_dir = 'mp3'
txt_base_dir = 'output/txt'

model = load_model(device='cpu')

mp3_files = glob.glob(f'{mp3_dir}/*.mp3')

for mp3_file in mp3_files:
    audio = audio_from_path(mp3_file)
    full_text = []
    
    # prepare sub directory
    base_name = os.path.splitext(os.path.basename(mp3_file))[0]
    txt_sub_dir = os.path.join(txt_base_dir, base_name)
    os.makedirs(txt_sub_dir, exist_ok=True)
    
    chunk_length = 60
    for i in range(0, len(audio.waveform), chunk_length * audio.samplerate):
        chunk = audio.waveform[i:i + chunk_length * audio.samplerate]
        chunk_audio = type(audio)(waveform=chunk, samplerate=audio.samplerate)
        
        result = transcribe(model, chunk_audio)
        text_content = result.text.strip()
        print(text_content)

        chunk_filename = f'{base_name}_chunk_{i//(chunk_length * audio.samplerate)}.txt'
        chunk_path = os.path.join(txt_sub_dir, chunk_filename)
        with open(chunk_path, 'w') as f:
            f.write(text_content)
        
        full_text.append(text_content)
    
    # save combined text
    if full_text:
        combined_filename = f'{base_name}.txt'
        combined_path = os.path.join(txt_sub_dir, combined_filename)
        with open(combined_path, 'w') as f:
            f.write('\n'.join(full_text))