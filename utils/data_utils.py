import pandas as pd
from pathlib import Path

def create_audio_dataframe(standardised_dir):
   # List to store file information
   data = []
   
   # Process each dataset folder
   for dataset_folder in Path(standardised_dir).iterdir():
       if not dataset_folder.is_dir():
           continue
           
       dataset_name = dataset_folder.name
       print(f"Processing {dataset_name}...")
       
       # Process each wav file in the dataset folder
       for file_path in dataset_folder.glob("*.wav"):
           parts = file_path.name.split('_')
           
           # Extract common information (first 4 parts are same for all)
           emotion_code = parts[0]
           intensity_code = parts[1]
           gender = parts[2]
           dataset = parts[3]
           
           # Extract dataset-specific information
           if dataset == 'ravdess':
               actor_id = parts[4]
               statement_rep = parts[5].replace('.wav', '')
               extra_info = statement_rep
           elif dataset == 'crema':
               actor_id = parts[4]
               sentence_code = parts[5].replace('.wav', '')
               extra_info = sentence_code
           elif dataset == 'savee':
               speaker = parts[4]
               sentence = parts[5].replace('.wav', '')
               extra_info = f"{speaker}_{sentence}"
           elif dataset == 'tess':
               actor = parts[4]
               word = parts[5].replace('.wav', '')
               extra_info = f"{actor}_{word}"
           
           # Map emotion codes to names
           emotion_map = {
               '01': 'neutral',
               '03': 'happy',
               '04': 'sad',
               '05': 'angry',
               '06': 'fear',
               '07': 'disgust'
           }
           
           # Map intensity codes
           intensity_map = {
               '01': 'normal',
               '02': 'strong',
               '03': 'unspecified'
           }
           
           data.append({
               'path': str(file_path),
               'emotion': emotion_map[emotion_code],
               'intensity': intensity_map[intensity_code],
               'gender': gender,
               'dataset': dataset,
               'extra_info': extra_info
           })
   
   # Create DataFrame
   df = pd.DataFrame(data)
   
   return df

# Create and display DataFrame
df = create_audio_dataframe("./standardised_datasets")

# Display information about the dataset
print("\nFirst few rows:")
print(df.head())

print("\nDataset info:")
print(df.info())

print("\nSample counts per dataset:")
print(df['dataset'].value_counts())

print("\nEmotion distribution:")
print(df['emotion'].value_counts())

print("\nGender distribution:")
print(df['gender'].value_counts())

# Save to CSV if needed
df.to_csv("audio_dataset_info.csv", index=False)