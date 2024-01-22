# Say-it-in-Swedish

A prototype of a simple tool that allows students of Swedish to practice their pronunciation by listening to sentences and recording their own versions of them. 

## Table of contents  
1. Introduction
2. Installation
3. Usage
5. Acknowledgments


### 1. Introduction
This is a school project whose aim is to give students of Swedish a simple tool to practice their pronunciation.
The tool can be used in two ways:
1. The student uploads a text file and then listens to it. After that, the student can choose the sentece/-s they want to practice pronouncing and they write it in the writing space. They can listen to the individual sentence and then record their version of it. After that, they get simple feedback: "Perfect!", "Good!", or "Ok. Try recording the sentence again.".
2. The student skips the part with the text and writes a chosen sentence in the writing space. They can listen to the individual sentence and then record their version of it. After that, they get simple feedback: "Perfect!", "Good!", or "Ok. Try recording the sentence again.".
   
### 2. Installation
Create an environment in the programming tool you use and install the following modules and libraries in your terminal:  
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

### Getting a file from a home directory and displaying it on the screen
This function @@choose_file@@ allows the user to choose a text file from their home directory and if a file is chosen, the text will be displayed on the screen. 

#### Converting text to audio
For this part of the project, we decided to use the Google text-to-speech module and Playsound library. We created a function and defined different parameters within it, like entry, language, and the name of the created audio file, and made it possible to play it. The language can be easily changed. We used the function both for the text input (**generate_and_play_textfile**) and the sentence input (**generate_and_play_mening**). The audio file is stored in mp3 format. 

### The recorder
**Start_recording** function makes it possible for the user to record their version of a chosen sentence. Within the function, the parameters for the stream are defined. The .wav file is created and stored for further comparison. 

### Converting the files
**convert_mp3_to_wav** is used to convert the mp3 audio file (generated by the text-to-speech function) to the wav audio file. This is for more reliable comparison results.

#### Comparison of the files and feedback
We have decided to compare the audio files by creating vectors of each file (**compare_and_feedback**) and using the cosine similarity (**cosine_similarity**) to assess the distance between the vectors. Even though we specified the features of each vector, using **mfcc**, **chroma_stft** and **spectral_contrast** and normalized the vectors, we still get results that are far from perfect. 
This method is not the best for comparing audio recordings and it has to be improved. 



