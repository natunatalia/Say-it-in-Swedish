# Say-it-in-Swedish

A prototype of a simple tool that allows students of Swedish to practice their pronunciation by listening to sentences and recording their own versions of them. 

## Table of contents  
1. Introduction
2. Installation
3. Usage
4. Limitations
5. Acknowledgments
8. Questions to Wojtek :)

### 1. Introduction
This is a school project whose aim is to give students of Swedish a simple tool to practice their pronunciation.
The tool can be used in two ways:
1. The student uploads a text file and then listens to it. After that, the student can choose the sentece/-s they want to practice pronouncing and they write it in the writing space. They can listen to the individual sentence and then record their version of it. After that, they get simple feedback: "Perfect!", "Good!", or "Try recording the sentence again.".
2. The student skips the part with the text and writes a chosen sentence in the writing space. They can listen to the individual sentence and then record their version of it. After that, they get simple feedback: "Perfect!", "Good!", or "Try recording the sentence again.".
   
### 2. Installation
Create an environment(do I have to explain how to do it?) in the tool you use and install the following modules and libraries in your terminal:  
pip install gTTS  
pip install librosa  
pip install playsound  
pip install dtw  
pip install numpy  
pip install tk  
pip install pydub
pip install pyaudio
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" (for mac)
brew install ffmpeg (mac)


Import all the libraries, see the file UploadTextFile.py

### 3. Usage
The code has many parts that can be used for other projects if needed.  

#### Converting text to audio
For this part of the project, we decided to use the Google text-to-speech module and Playsound library. We created a function and definied all the specified type of entry, language, and the name of the created audio file and made it possible to play it. 
```python
def generate_and_play_mening():
#insert text you wanna convert to audio
    result= entry2.get() 
    language = "sv" 
    myobj = gTTS(text=result, lang=language, slow=False)
    myobj.save("upplastmening.mp3")
    playsound.playsound("upplastmening.mp3", True) 
```

#### Comparison of the files
We have decided to compare the audio files by creating vectors of each file and use the cosine similarity to asses the distance between the vectors. 
```python
#uploading audio files for comparison
    y1, sr1 = librosa.load("Projekt_programmering/upplastmening.mp3")
    y2, sr2 = librosa.load("Projekt_programmering/elevinspelning.wav") #OBS! rename the file in the recording script

#computing the MFSS audio signal
    features1 = librosa.feature.mfcc(y=y1, sr=sr1)
    features2 = librosa.feature.mfcc(y=y2, sr=sr2)

#computing distance DTW, with cosine similarity
    result = dtw(x=features1.T, y=features2.T, dist_method="cosine")
    dist = result.distance
