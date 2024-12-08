from pathlib import Path
from utils.logging_utils import setup_logging
import shutil

class ravdess_parser:
    def __init__(self):
        self.emotion_map = {
            '01': 'neutral',
            '02': 'neutral',
            '03': 'happy',
            '04': 'sad',
            '05': 'angry',
            '06': 'fearful',
            '07': 'disgust'
        }

        self.logger = setup_logging()

    def process_files(self, input_path: str, output_path: str = "./standardised_datasets/RAVDESS"):
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Processing RAVDESS files from: {input_path}")
        processed_count = 0
        skipped_count = 0
        
        for actor_folder in input_path.iterdir():
            if not actor_folder.is_dir() or not actor_folder.name.startswith('Actor_'):
                continue
                
            self.logger.info(f"Processing actor folder: {actor_folder.name}")
            
            for file_path in actor_folder.glob('*.wav'):
                try:
                    # Skip files with emotion code '08' (surprised)
                    emotion_code = file_path.name.split('-')[2]
                    if emotion_code == '08':
                        skipped_count += 1
                        continue
                        
                    new_filename = self._create_standardised_name(file_path.name, actor_folder.name)
                    if new_filename:
                        new_path = output_path / new_filename
                        shutil.copy2(file_path, new_path)
                        processed_count += 1
                        self.logger.info(f"Processed: {file_path.name} -> {new_filename}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing {file_path.name}: {str(e)}")
                    continue
        
        self.logger.info(f"Processing complete. Processed: {processed_count}, Skipped: {skipped_count}")

    def _create_standardised_name(self, filename: str, actor_folder: str) -> str:
        '''
        Create standardised filename from RAVDESS format
        IN: 03-01-03-02-02-01-06.wav
        OUT: 03_02_F_ravdess_06_0201.wav
        (emotion_intensity_gender_dataset_statement+repetiion)
        '''
        parts = filename.replace('.wav', '').split('-')
        
        # Exctracting info
        actor_id = int(parts[6])
        emotion_code = parts[2]
        
        # Skipping non-mapped emotions
        if emotion_code not in self.emotion_map:
            return None
        
        # Change 'calm' to 'neutral'
        if emotion_code == '02':
            emotion_code = '01'
            
        intensity_code = parts[3]
        gender = 'M' if actor_id % 2 != 0 else 'F'  # odd=male, even=female
        statement_rep = f"{parts[4]}{parts[5]}"  # combine statement and repetition
        
        # Create new filename
        return f"{emotion_code}_{intensity_code}_{gender}_ravdess_{actor_id:02d}_{statement_rep}.wav"