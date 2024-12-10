from pathlib import Path
from utils.logging_utils import setup_logging
import shutil

class tess_parser:
    def __init__(self) -> None:
        self.emotion_map = {
            'neutral': '01',
            'happy': '03',
            'sad': '04',
            'angry': '05',
            'fear': '06',
            'disgust': '07'
        }


        self.logger = setup_logging()
    
    def _create_standardised_name(self, filename: str, actor: str, emotion: str) -> str:
        '''
        Create standardised filename from TESS format
        IN: OAF_bark_angry.wav
        OUT: 05_01_F_tess_OAF_bark.wav 
        (emotion_intensity_gender_dataset_actor_word)
        '''

        # Taking word from input filename
        word = filename.split('_')[1]

        # Mapping emotion to standardised code
        emotion_code = self.emotion_map[emotion]

        gender = 'F'
        intensity = '01'

        return f"{emotion_code}_{intensity}_{gender}_tess_{actor}_{word}.wav"
    
    def process_files(self, input_path: str, output_path: str = './standardised_datasets/TESS') -> None:
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Processing TESS files from: {input_path}")
        processed_count = 0
        skipped_count = 0

        # Iterating through each subfolder
        for folder in input_path.iterdir():
            if not folder.is_dir():
                continue
            
            # Parse folder name ('OAF_angry' etc)
            folder_parts = folder.name.split('_')
            if len(folder_parts) != 2:
                continue

            actor, emotion = folder_parts

            if emotion not in self.emotion_map:
                continue

            self.logger.info(f"Processing folder: {folder.name}")

            # Processing each audio file
            for file_path in folder.glob('*.wav'):
                try:
                    new_filename = self._create_standardised_name(file_path.name, actor, emotion)
                    if new_filename:
                        new_path = output_path / new_filename
                        shutil.copy2(file_path, new_path)
                        processed_count += 1
                        self.logger.info(f"Processed: {file_path.name} -> {new_filename}")
                    else:
                        skipped_count += 1
                except Exception as e:
                    self.logger.error(f"Error processing {file_path.name}: {str(e)}")
                    continue

        self.logger.info(f"Processing complete. Processed: {processed_count}, Skipped {skipped_count}")