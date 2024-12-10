Data Standardisation:

    - make sure to create a virtual environment

    - type these into your terminal:

        python3 -m venv .venv

        .venv/bin/pip install -r requirements.txt


    -   To process data (make sure your working directory is the root project directory):

        .venv/bin/python3 process_files.py

FORMATS:

CREMA:
    IN: 
    1005_IWW_DIS_XX.wav
    OUT: emotion_intensity_gender_dataset_actorID_sentenceCode

RAVDESS:
    IN: 
    03-01-03-02-02-01-06.wav
    OUT: 
    03_02_F_ravdess_06_0201.wav
    (emotion_intensity_gender_dataset_statement+repetiion)

SAVEE:
    IN: 
    speaker_emotion_sentencenumber
    OUT: 
    05_01_M_savee_DC_01.wav (emotion_intensity_gender_savee_speaker_sentence)

TESS:
    IN: 
    OAF_bark_angry.wav
    OUT: 
    05_01_F_tess_OAF_bark.wav 
    (emotion_intensity_gender_dataset_actor_word)