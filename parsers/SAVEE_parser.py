# The SAVEE database was recorded from four native English male speakers (identified as DC, JE, JK, KL)

from pathlib import Path
from utils.logging_utils import setup_logging
import shutil

class savee_parser:
    def __init__(self) -> None:
        self.emotion_map = {
            'n': '01',
            'h': '03',
            'sa': '04',
            'a': '05',
            'f': '06',
            'd': '07'
        }

        self.logger = setup_logging()

    def process_files(self, input_path: str, output_path: str = './standardised_datasets/SAVEE'):
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

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

        self.logger.info(f"Processing complete. Processed: {processed_count}, Skipped: {skipped_count}")
    
    def _create_standardised_name(self, filename: str) -> str:
        """
        Convert SAVEE filename to standardized format
        IN: speaker_emotion_sentencenumber
        Output: 05_01_M_savee_DC_01.wav (emotion_intensity_gender_savee_speaker_sentence)
        """
        parts = filename.split('_')
        speaker = parts[0]
        emotion = ''.join(c for c in parts[1].replace('.wav','') if not c.isdigit())
        
        sentence = ''.join(c for c in parts[1].replace('.wav','') if c.isdigit())

        if emotion not in self.emotion_map:
            self.logger.debug(f"Skipped emotion: {emotion} in file {filename}")
            return None

        gender = 'M'
        emotion_code = self.emotion_map[emotion]
        intensity_code = '01'  

        return f"{emotion_code}_{intensity_code}_{gender}_savee_{speaker}_{sentence}.wav"