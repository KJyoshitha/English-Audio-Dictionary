# Digital English Dictionary
from tkinter import *
import customtkinter as ctk
import json
from nltk.corpus import wordnet
import nltk
import pyttsx3
from difflib import get_close_matches
from CTkMessagebox import CTkMessagebox

nltk.download("wordnet")
nltk.download("omw-1.4")


ctk.set_appearance_mode("dark")

# window
app = ctk.CTk()
app.title("Digital English Dictionary")
app.geometry("1200x700+10+20")
app.resizable(None, None)

# Audio - pyttsx3
engine = pyttsx3.init()

voice = engine.getProperty('voices')
engine.setProperty('voices', voice[0].id)


# Functionalities

def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            s = lemma.name().replace("_", " ")
            if s.lower() != word.lower():
                synonyms.add(s)
    return sorted(synonyms)


def get_antonyms(word):
    antonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            for ant in lemma.antonyms():
                antonyms.add(ant.name().replace("_", " "))
    return sorted(antonyms)


def search():
    # clear text
    # txt1.delete(0.0, "end")
    txt2.delete(0.0, "end")
    txt3.delete(0.0, "end")

    data = json.load(open('data.json'))
    word = entry.get()
    word = word.lower()

    if word in data:
        meaning = data[word]
        txt1.delete(0.0, "end")
        for item in meaning:
            txt1.insert("end", '- ' + item + '\n\n')

    elif len(get_close_matches(word, data.keys())) > 0:
        suggest = get_close_matches(word, data.keys())[0]
        confirm = CTkMessagebox(title="Confirm", message=f'Did you mean {suggest} instead?',
                                option_1="Yes", option_2="No")
        if confirm.get() == "Yes":
            entry.delete(0, END)
            entry.insert(END, suggest)
            meaning = data[suggest]
            txt1.delete(0.0, "end")

            for item in meaning:
                txt1.insert("end", '- ' + item + '\n\n')
        else:
            CTkMessagebox(title="Error", icon="warning", message="The word does not exist. Try searching the web.")
            entry.delete(0, END)
            txt1.delete(0.0, "end")

    else:
        CTkMessagebox(title="Info", message="Word does not exist.")
        entry.delete(0, END)
        txt1.delete(0.0, "end")

    # Synonyms
    synonym_results = get_synonyms(word)
    if synonym_results:
        for i in synonym_results:
            txt2.insert("end", "- " + i + "\n\n")
    else:
        txt2.insert("end", "No synonyms found.")

    # Antonyms
    antonym_results = get_antonyms(word)
    if antonym_results:
        for i in antonym_results:
            txt3.insert("end", "- " + i + "\n\n")
    else:
        txt3.insert("end", "No antonyms found.")


# Entry Audio
def entry_audio():
    engine.setProperty('rate', 125)
    engine.say(entry.get())
    engine.runAndWait()


def meaning_audio():
    engine.say(txt1.get(1.0, 'end'))
    engine.runAndWait()


def clear():
    entry.delete(0, END)
    txt1.delete(0.0, 'end')
    txt2.delete(0.0, 'end')
    txt3.delete(0.0, 'end')


def enter_event(event):
    mag.invoke()


# left frame
frame1 = ctk.CTkFrame(app, width=550, height=800, fg_color="#3AAFA9", corner_radius=0)
frame1.place(x=0, y=0)

label1 = ctk.CTkLabel(app, text="ENGLISH", font=("helvetica", 60, "bold"), fg_color="#3AAFA9")
label2 = ctk.CTkLabel(app, text="DICTIONARY", font=("helvetica", 60, "bold"), fg_color="#3AAFA9")
label1.place(x=140, y=250)
label2.place(x=100, y=340)

entry = ctk.CTkEntry(app, height=40, width=210, font=('roboto', 15),
                     placeholder_text="Type here", placeholder_text_color="white")
entry.place(x=650, y=100)
# audio
mic = ctk.CTkButton(app, width=50, height=40, corner_radius=5, text="Audio", fg_color="#2B7A78", command=entry_audio)
mic.place(x=950, y=100)
# search button
mag = ctk.CTkButton(app, width=50, height=40, corner_radius=5, text="Search", fg_color="#2B7A78", command=search)
mag.place(x=880, y=100)
clear = ctk.CTkButton(app, width=50, height=40, corner_radius=5, text="Clear", fg_color="#2B7A78", command=clear)
clear.place(x=1020, y=100)

# create tabview
tab = ctk.CTkTabview(app, width=600, height=450, anchor="w")
tab.place(x=575, y=200)

# create tabs
tab_1 = tab.add("Meaning")
tab_2 = tab.add("Synonyms")
tab_3 = tab.add("Antonyms")

# add to tabs
# tab1
txt1 = ctk.CTkTextbox(tab_1, width=560, height=350, wrap='word', font=('roboto', 17))
txt1.place(x=10, y=45)
mic = ctk.CTkButton(tab_1, width=40, height=30, corner_radius=5, text="Audio", fg_color="#2B7A78",
                    command=meaning_audio)
mic.place(x=30, y=5)

# tab2
txt2 = ctk.CTkTextbox(tab_2, width=560, height=350, font=('roboto', 17))
txt2.place(x=10, y=45)
mic = ctk.CTkButton(tab_2, width=40, height=30, corner_radius=5, text="Audio", fg_color="#2B7A78")
mic.place(x=30, y=5)

# tab3
txt3 = ctk.CTkTextbox(tab_3, width=560, height=350, font=('roboto', 17))
txt3.place(x=10, y=45)
mic = ctk.CTkButton(tab_3, width=40, height=30, corner_radius=5, text="Audio", fg_color="#2B7A78")
mic.place(x=30, y=5)

app.bind('<Return>', enter_event)

app.mainloop()
