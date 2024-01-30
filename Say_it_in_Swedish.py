#import the libraries to analyze sounds & for the interface
from gtts import gTTS
import os
import librosa
import playsound
import pyaudio
from pydub import AudioSegment
import scipy.io.wavfile as wf
from scipy.spatial.distance import cdist
from dtw import dtw
import numpy as np 
import tkinter as tk
from tkinter import Entry, Button, Label, LabelFrame, StringVar, filedialog
from tkinter import ttk

#Defining parameters for recording
chunk = 1024
format = pyaudio.paFloat32 
channel = 2
rate = 44100
p = pyaudio.PyAudio()

#defining relative directory for the gtts-read sentence
relative_directory = os.path.dirname(os.path.abspath(__file__))

#Global recorder to track recording of the audio
recording_in_progress = False

#Function for acessing the user's directory and displaying the text on the screen
def choose_file():
    initial_dir = os.path.expanduser("~")  
    file_path = filedialog.askopenfilename(initialdir=initial_dir)


    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        file_content_label.config(text=f"{file_content}")

#Function for text-to-speech coversion - the uploaded text
def generate_and_play_textfile():
    language = "sv"
    file_content = file_content_label.cget("text")
    myobj = gTTS(text=file_content, lang=language, slow=False)
    myobj.save("uppladad_text.mp3")
    playsound.playsound("uppladad_text.mp3", True) 

#Function for text-to-speech conversion - sentence
def generate_and_play_mening():
    global relative_directory
    result= entry2.get() 
    language = "sv" 
    output_filename = "upplastmening.mp3"

    #defining directory for the output file
    output_path = os.path.join(relative_directory, output_filename)

    myobj = gTTS(text=result, lang=language, slow=False)
    myobj.save(output_path)
    playsound.playsound(output_path, True) 


#The recorder
def start_recording(event=None):
    global recording_in_progress

    if not recording_in_progress:
        recording_in_progress = True

        #Change the button text while recording
        record_button.config(text="Spelar in...", bg= "grey", fg="red")
        root.update() 

        stream = p.open(format=format,
                channels=channel,
                rate=rate,
                input=True,
                frames_per_buffer=chunk,
        )

        frames = np.zeros((channel, 0), dtype=np.float32)
        seconds = 5

    
        #Loop for capturing the audio data and append it to the frame list
        for i in range (0, int(rate / chunk * seconds)):
            data = stream.read(chunk)
            decoded = np.frombuffer(data, np.float32)
            decodedSplit = np.stack((decoded[::2], decoded[1::2]), axis=0)  
            frames = np.append(frames, decodedSplit, axis=1)


        stream.stop_stream()
        stream.close()
        p.terminate()

        #Changing the recording button to normal
        record_button.config(text="Spela in din mening", bg= "grey", fg="black")
        recording_in_progress = False
        root.update()
        
        #Storing the recording as a wav-file
        wave_file_path = f"elevinspelning.wav"
        wf.write(wave_file_path, 44100, frames.T)

        #Calling the compare and feedback function that displays the feedback when the recording ended
        compare_and_feedback()
        

#Converting mp3 to wav for better comparison
def convert_mp3_to_wav():
    global relative_directory
    input_mp3_path = os.path.join(relative_directory,"upplastmening.mp3")
    output_wav_path = os.path.join(relative_directory, "upplastmening_converted.wav")
    audio = AudioSegment.from_mp3(input_mp3_path)
    audio.export(output_wav_path, format="wav")

#calling the function
convert_mp3_to_wav()

#Function for comparison
def compare_and_feedback():
    global relative_directory

    #Uploading audio files for comparison
    output_wav_path = os.path.join(relative_directory, "upplastmening_converted.wav")
    y1, sr1 = librosa.load(output_wav_path)
    y2, sr2 = librosa.load("elevinspelning.wav")

#Specifing audio vector features for more accurate comparison
    n_mfcc = 40
    n_fft = 2048
    features1 = np.vstack((
        librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=n_mfcc, n_fft=n_fft),
        librosa.feature.chroma_stft(y=y1, sr=sr1),
        librosa.feature.spectral_contrast(y=y1, sr=sr1),
    ))

    features2 = np.vstack((
        librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=n_mfcc, n_fft=n_fft),
        librosa.feature.chroma_stft(y=y2, sr=sr2),
        librosa.feature.spectral_contrast(y=y2, sr=sr2),
    ))
    
    
    #Normalizing features
    mean1, std1 = np.mean(features1, axis=1, keepdims=True), np.std(features1, axis=1, keepdims=True)
    mean2, std2 = np.mean(features2, axis=1, keepdims=True), np.std(features2, axis=1, keepdims=True)

    features1_normalized = (features1 - mean1) / std1
    features2_normalized = (features2 - mean2) / std2
    result = cdist(features1_normalized.T, features2_normalized.T, metric='cosine')
    dist = np.mean(result)

#Definig ranges for the assesment of the student recording (elevinspelning)
    threshold_excellent = (0.9)
    threshold_good = (0.65)
    threshold_again = (0.64)


#Giving feeback based on the distance and previously set thresholds
    if dist >= threshold_excellent:
        feedback = "perfekt!"   
    elif dist >= threshold_good:
        feedback = "bra!" 
    elif dist <= threshold_again:
        feedback = "ok. Försök att uttala meningen igen!"

    #The label for the feedback
    feedback_label.config(text=f"Du uttalar meningen {feedback}")

# Print feedback
    print("Du uttalar meningen ", feedback)

#Interface
root = tk.Tk()
root.title("Säg det på svenska")
# Main window interface

#label for the instruction
instruction = Label(text="I det här programmet kan du ladda upp en text och få den uppläst.\nDu kan också träna på uttal av olika meningar,\nantingen från den uppladade texten eller skriva in andra meningar.\n\n", font =("Helvetica", 16), justify = "left")
instruction.grid(row=0, column=0, columnspan=2, padx =(10), pady=(10,0), sticky ="w")

#Label for the button instruction
label = Label(root, text="Klicka på knappen och ladda upp din text.", font =("Helvetica", 16))
label.grid(row=1, column=0, columnspan=2, padx=(20,0), pady=20, sticky="w")
label.grid(row=1, column=0, padx=(5,0), pady=5, sticky="w")


#Button to upload the file
button_file1 = Button(root, text="Bläddra", command=choose_file)
button_file1.grid(row=2, column=0, padx=(20,0), pady=12, sticky="e")
button_file1.grid(row=2, column=0, sticky="w")

#label for the uploaded text
file_content_label = Label(root, text="", justify="left", wraplength=450, font =("Helvetica", 16))
file_content_label.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=50, sticky="w")


#Label for writing a sentence
label = Label(root, text="Skriv din mening här: ", font =("Helvetica", 16))
label.grid(row=4, column=0, columnspan=2, padx=(20,0), pady=20, sticky="w")
label.grid(row=5, column=0, padx=(5,0), pady=5, sticky="w")

#The field for writing a sentence
entry2 = Entry(root, width=50)
entry2.grid(row=5, column=0, padx=(20, 0), pady=10, sticky= "w")
entry2.grid(row=6, column=0, padx=(5,0), pady=5, sticky= "w")

#Button for generating and playing the uploaded text
generate_button = Button(root, text="Lyssna på texten", command=generate_and_play_textfile)
generate_button.grid(row=4, column=0, padx=10, pady=20, sticky = "w")

#Button for generating and playing the sentence
play_button = Button(root, text="Lysna på din mening", command=generate_and_play_mening)
play_button.grid(row=6, column=1, padx=(5, 0), pady=5,  sticky="w")

#Instruction for the recording
label = Label(root, text = "Klicka på knappen nedan och säg din mening en gång. Det kan ta en stund innan du får respons.", font=("Helvetica", 16), justify = "left")
label.grid(row= 7, column=0, columnspan = 2,padx=(20,0), pady=20, sticky="w") 

#Button to record the sentence
record_button = Button(root, text="Spela in din mening", command=start_recording)
record_button.grid(row=8, column=0, padx=(5, 0), pady=5, sticky ="w")

#Label with the feedback
feedback_label = Label(root, text="", font=("Helvetica", 18), justify="left")
feedback_label.grid(row=9, column=0, padx=(5, 0), pady=5,)

root.geometry("700x700")

# Start window
root.mainloop()