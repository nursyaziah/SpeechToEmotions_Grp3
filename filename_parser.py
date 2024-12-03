import os
import shutil
from typing import List, Dict, Tuple

def create_standardized_name(original_file: str, actor_folder: str) -> Tuple[str, dict]:
    """
    Convert RAVDESS filename to standardized format with unique identifiers
    Output: (emotion_intensity_gender_dataset_actor_statement-repetition)
    """
    parts = original_file.replace('.wav', '').split('-')
    
    # Get actor number and determine gender code
    actor_id = int(parts[6])
    gender_code = '01' if actor_id % 2 != 0 else '02'  # 01=male, 02=female
    
    # Get emotion and intensity codes
    emotion_code = parts[2]
    intensity_code = parts[3]
    
    # Create unique identifier from statement and repetition
    statement_code = parts[4]
    repetition_code = parts[5]
    unique_id = f"{statement_code}{repetition_code}"
    
    # Create new standardized filename
    new_filename = f"{emotion_code}_{intensity_code}_{gender_code}_ravdess_{actor_id:02d}_{unique_id}.wav"
    
    metadata = {
        'original_filename': original_file,
        'emotion_code': emotion_code,
        'intensity_code': intensity_code,
        'gender_code': gender_code,
        'actor_id': actor_id,
        'statement_code': statement_code,
        'repetition_code': repetition_code
    }
    
    return new_filename, metadata


def standardize_ravdess(input_path: str, output_base: str = "./standardised_datasets") -> List[Dict]:
    """
    Copy and rename RAVDESS files to standardised format and location
    """
    # Create output directory for RAVDESS
    output_dir = os.path.join(output_base, "RAVDESS")
    os.makedirs(output_dir, exist_ok=True)
    
    processed_files = []
    total_actors = 0
    total_files = 0

    print(f"Reading from: {input_path}")
    
    # Process each actor folder
    for actor_folder in os.listdir(input_path):
        actor_path = os.path.join(input_path, actor_folder)
        
        if not os.path.isdir(actor_path) or not actor_folder.startswith('Actor_'):
            continue
            
        total_actors += 1
        actor_file_count = 0
        
        # Process each wav file
        for file in os.listdir(actor_path):
            if file.endswith('.wav'):
                try:
                    # Generate new filename
                    new_filename, metadata = create_standardized_name(file, actor_folder)
                    original_path = os.path.join(actor_path, file)
                    new_path = os.path.join(output_dir, new_filename)
                    
                    # Copy file with new name
                    shutil.copy2(original_path, new_path)
                    
                    actor_file_count += 1
                    total_files += 1
                    
                    # Store the mapping
                    processed_files.append({
                        'original_path': original_path,
                        'new_path': new_path,
                        'original_filename': file,
                        'new_filename': new_filename,
                        'metadata': metadata
                    })
                    
                except Exception as e:
                    print(f"Error processing file {file}: {str(e)}")
                    continue
        
        print(f"Processed Actor {actor_folder}: {actor_file_count} files")
    
    print(f"\nTotal actors processed: {total_actors}")
    print(f"Total files found: {total_files}")
    return processed_files

    
if __name__ == '__main__':
    ravdess_path = "./datasets/Ravdess/audio_speech_actors_01-24"
    
    # Process files
    processed_files = standardize_ravdess(ravdess_path)
    
    # Print summary
    print(f"\nTotal files processed: {len(processed_files)}")
    
    # Print some examples
    print("\nExample of processed files:")
    for entry in processed_files[:3]:
        print(f"\nOriginal: {entry['original_filename']}")
        print(f"New: {entry['new_filename']}")
        print(f"New path: {entry['new_path']}")

