from parsers.RAVDESS_parser import ravdess_parser
from parsers.TESS_parser import tess_parser
from parsers.CREMA_parser import crema_parser
from parsers.SAVEE_parser import savee_parser

def process_datasets():
    ravdess = ravdess_parser()
    tess = tess_parser()
    crema = crema_parser()
    savee = savee_parser()
    
    # Define paths
    ravdess_path = './datasets/Ravdess/audio_speech_actors_01-24'
    tess_path = './datasets/Tess'
    crema_path = './datasets/Crema'
    savee_path = './datasets/Savee'
    
    try:
        # Process RAVDESS
        print("Processing RAVDESS dataset...")
        ravdess.process_files(ravdess_path)
        print("RAVDESS processing complete")
        
        # Process TESS
        print("Processing TESS dataset...")
        tess.process_files(tess_path)
        print("TESS processing complete")

        # Process CREMA
        print("Processing CREMA dataset...")
        crema.process_files(crema_path)
        print("CREMA processing complete")
        
        # Process SAVEE
        print("Processing SAVEE dataset...")
        savee.process_files(savee_path)
        print("SAVEE processing complete")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    process_datasets()