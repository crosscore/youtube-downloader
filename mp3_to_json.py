import json
import torch
from transformers import pipeline, WhisperForConditionalGeneration, WhisperProcessor, GenerationConfig
import os
from pathlib import Path
from tqdm import tqdm
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioTranscriber:
    def __init__(self, model_id: str = "openai/whisper-medium"):
        self.model_id = model_id
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.pipe = None
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"Torch dtype: {self.torch_dtype}")

    def load_model(self, model_dir: str = "model") -> None:
        """Load or download the model"""
        try:
            model_path = Path(model_dir) / self.model_id.replace("/", "_")
            model_path.parent.mkdir(exist_ok=True)

            if model_path.exists() and (model_path / "model.safetensors").exists():
                logger.info(f"Loading model from local cache: {model_path}")
                model = WhisperForConditionalGeneration.from_pretrained(
                    model_path,
                    torch_dtype=self.torch_dtype
                )
                processor = WhisperProcessor.from_pretrained(model_path)
            else:
                logger.info(f"Downloading model {self.model_id}...")
                model = WhisperForConditionalGeneration.from_pretrained(
                    self.model_id,
                    torch_dtype=self.torch_dtype
                )
                processor = WhisperProcessor.from_pretrained(self.model_id)
                
                # Save model and processor
                model.save_pretrained(model_path)
                processor.save_pretrained(model_path)
                logger.info(f"Model saved to {model_path}")

            # Configure generation settings
            generation_config = GenerationConfig.from_pretrained(self.model_id)
            generation_config.no_timestamps_token_id = processor.tokenizer.convert_tokens_to_ids("<|notimestamps|>")
            model.generation_config = generation_config

            # Move model to appropriate device
            model = model.to(self.device)

            # Create pipeline with Japanese settings
            forced_decoder_ids = processor.get_decoder_prompt_ids(language="ja", task="transcribe")
            
            self.pipe = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                torch_dtype=self.torch_dtype,
                device=self.device,
                model_kwargs={"forced_decoder_ids": forced_decoder_ids},
                generate_kwargs={
                    "max_new_tokens": 400,  # Reduced from 448
                    "language": "ja"
                }
            )

            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def transcribe(
        self,
        mp3_path: str,
        output_path: str,
        chunk_length_s: int = 30
    ) -> None:
        """Transcribe audio file and save result as JSON"""
        try:
            if self.pipe is None:
                self.load_model()

            if not os.path.exists(mp3_path):
                raise FileNotFoundError(f"Audio file not found: {mp3_path}")

            logger.info(f"Processing {mp3_path}")
            
            # Try transcription with basic settings
            try:
                result = self.pipe(
                    mp3_path,
                    chunk_length_s=chunk_length_s,
                    return_timestamps=False  # Disable timestamps for now
                )
            except ValueError as e:
                logger.warning(f"Error during transcription: {e}")
                # Try with even more conservative settings
                result = self.pipe(
                    mp3_path,
                    chunk_length_s=chunk_length_s,
                    batch_size=1
                )

            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Transcription saved to {output_path}")

        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            raise

def main():
    # Configuration
    mp3_folder = Path('mp3')
    output_folder = Path('json')
    output_folder.mkdir(exist_ok=True)

    try:
        transcriber = AudioTranscriber()
        
        mp3_files = list(mp3_folder.glob("*.mp3"))
        if not mp3_files:
            logger.warning(f"No MP3 files found in {mp3_folder}")
            return

        for mp3_file in tqdm(mp3_files, desc="Processing audio files"):
            output_path = output_folder / f"{mp3_file.stem}.json"
            transcriber.transcribe(
                str(mp3_file),
                str(output_path)
            )

    except Exception as e:
        logger.error(f"Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()