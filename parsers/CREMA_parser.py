# 6076/7442 is unspecified

from pathlib import Path
from utils.logging_utils import setup_logging
import shutil
import pandas as pd

class crema_parser:
    def __init__(self) -> None:
        self.emotion_map = {
            'NEU': '01',
            'HAP': '03',
            'SAD': '04',
            'ANG': '05',
            'FEA': '06',
            'DIS': '07'
        }

        self.intensity_map = {
            'XX': '03',
            'LO': '01',
            'MD': '01',
            'HI': '02'
        }

        self.logger = setup_logging()

        demographics_path = Path(__file__).parent.parent / 'misc' / 'CremaDemographics.csv'
        self.demographics = pd.read_csv(demographics_path)
        self.gender_map = self.demographics.set_index('ActorID')['Sex'].to_dict()
    
    def process_files(self, input_path: str, output_path: str = "./standardised_datasets/CREMA"):
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Processing CREMA files from {input_path}")
        processed_count = 0
        skipped_count = 0

        for file_path in input_path.glob('*.wav'):
            try:
                new_filename = self._create_standardised_name(file_path.name)
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
        
        self.logger.info(f"Processing complete. Processed: {processed_count}, Skipped: {skipped_count}")


    def _create_standardised_name(self, filename: str) -> str:
        '''
        Convert CREMA to standardised
        IN: 1005_IWW_DIS_XX.wav
        OUT: emotion_intensity_gender_dataset_actorID_sentenceCode
        '''

        parts = filename.replace('.wav', '').split('_')
        actor_id = parts[0]
        sentence = parts[1]
        emotion = parts[2]
        intensity = parts[3]


        if emotion not in self.emotion_map:
            self.logger.debug(f"Skipped emotion: {emotion} in file {filename}")
            return None
        
        gender = 'M' if self.gender_map[int(actor_id)] == 'Male' else 'F'
        emotion_code = self.emotion_map[emotion]
        intensity_code = self.intensity_map[intensity]

        return f"{emotion_code}_{intensity_code}_{gender}_crema_{actor_id}_{sentence}.wav"
