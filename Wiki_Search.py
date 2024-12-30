#-------------------------------LES IMPORTATIONS------------------------------------------------------------
from tkinter import *
import customtkinter as ctk
from CTkSpinbox import *
import pyttsx4
from wikipedia import *
import threading
from PIL import Image, ImageTk, ImageSequence
import time

#---------------------------------configureURATION DE LA FENETRE---------------------------------------------------
ctk.set_appearance_mode("light")
fen = ctk.CTk()
fen.title("Wiki_Search")
fen.geometry("450x550")
fen.resizable(False,False)
fen.iconbitmap('C:\\Users\\HP\\Desktop\\BUREAU\\mes projets\\python fill\\assistant vocale\\WS_icon.ico')

#--------------------------------C'EST LA PARTIE DES VARIABLES---------------------------------------------------

off = PhotoImage(file="C:\\Users\\HP\\Desktop\\BUREAU\\mes projets\\python fill\\assistant vocale\\off.png")
on = PhotoImage(file="C:\\Users\\HP\\Desktop\\BUREAU\\mes projets\\python fill\\assistant vocale\\on.png")
reglage_icon = PhotoImage(file="C:\\Users\\HP\\Desktop\\BUREAU\\mes projets\\python fill\\assistant vocale\\pg1.png")
search1 = PhotoImage(file = "C:\\Users\\HP\\Desktop\\BUREAU\\mes projets\\python fill\\assistant vocale\\search.png")
lang = StringVar()
is_on = False
reponse = StringVar()
result = StringVar()
nbr_phrase = IntVar()
#=================================INITIALISATION DE PYTTSX4========================================================
engine=pyttsx4.init()
voices=engine.getProperty('voices')
#engine.setProperty('voice',voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-15)

wikipedia.set_lang("fr")
#=================================LA PARTIE DE L'ENSEMBLE DES FONCTIONS===========================================

def select():
    lang = fr_en.get()
    if lang == "Francais":
        wikipedia.set_lang("fr")
        engine.setProperty('voice',voices[0].id)
    elif lang == "Anglais":
        wikipedia.set_lang("en")
        engine.setProperty('voice',voices[1].id)

#--------------------------------LA PARTIE QUI GERE LE CHARGEMENT (SPIN LOADER)-----------------------------------
# Fonction pour démarrer l'animation dans un thread
def start_animation():
    threading.Thread(target=run_animation, daemon=True).start()

# Fonction pour afficher le GIF dans un thread
def run_animation():
    global gif_label
    gif = Image.open(r"C:\Users\HP\Desktop\BUREAU\mes projets\python fill\assistant vocale\loader.gif")
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

    gif_label = ctk.CTkLabel(fen,text="",bg_color="white"
                            #,fg_color="white"
                            )
    gif_label.place(x = 210,y = 250)

    def update_gif(frame_index):
        if gif_label.winfo_exists():  # Si le label existe encore
            gif_label.configure(image=frames[frame_index])
            fen.after(100, update_gif, (frame_index + 1) % len(frames))

    update_gif(0)  # Démarrer l'animation
    
    # Détruire l'animation après 3 secondes
    time.sleep(2)
    if gif_label.winfo_exists():
        gif_label.destroy()
    rechercher()
#-----------------------------------------------------------------------------------------------------------------

def rechercher():
    global result
    select()
    effacer()
    try:
        nbr_phrase = phrase_entry.get()
        entrer = reponse.get()
        result = wikipedia.summary(entrer, sentences = nbr_phrase)
        resultat.configure(border_color='#007FFF')
        resultat.insert(END, result)
    except requests.exceptions.ConnectionError as e:
        resultat.insert(END, "OUPS!!!😬 Probléme de Connexion!!!\nVerifier votre Connexion Internet et Réessayer.")
        resultat.configure(border_color='red')
    except Exception as e:
        resultat.insert(END, "Aie😬!!! Pas de Resultat !!!\nEssayer d'une autre Maniére.")
        resultat.configure(border_color='red')

def effacer():
    resultat.delete(1.0,END)

def switch():
    global is_on
    if (is_on == True):
        sound.configure(image=off)
        is_on = False
    else:
        sound.configure(image = on)
        is_on = True
        #thread_lecture = threading.Thread(target=lecture)
        #thread_lecture.start()

def lecture():
    engine.say(result)
    engine.runAndWait()


#=================================CRÉATION DES CANVAS=================================================================
monCanvas = ctk.CTkCanvas(fen, width=673, height=823)
monCanvas.place(x=0,y=0)
monCanvas.create_rectangle(-1,0,673,823, width=0, fill="#22c7ff") #bleu cyan
#=================================LA PARTIE PRÉSENTATION================================================================
bienvenue1 = ctk.CTkLabel(fen,text = "Bienvenu sur Wiki_Search",image= search1,compound='right',
                font=("Helvetica", 20, "bold"),
                bg_color = "#22c7ff",
                text_color="white",
                ).pack(pady=5)
presentation = ctk.CTkLabel(fen,text = "Wiki_Search est une plateforme qui vous facilite la recherche sur WIKIPEDIA",
                bg_color = "#22c7ff",
                font= ("hevetica",12,'bold')
                ).pack()

#================================LA PARTIE OU ON MET LE RÉSULAT DE RECHERCHE==============================================
resultat = ctk.CTkTextbox(fen,
                bg_color= "#22c7ff", 
                font=('hevetica',12),
                text_color="black",
                border_width=2,
                border_color="#007FFF",
                wrap="word",
                width=325,
                height=200,
                state= "normal"
                )
resultat.place(x=60,y=160)

#===============================LA PARTIE OU ON MET LA QUESTION ET LE BOUTTON ENVOIE=======================================
question_label = ctk.CTkLabel(fen,text="Veillez saisir votre question :",
                    bg_color='#22c7ff',
                    text_color="black",
                    font= ("verdana",12,"bold")
                    )
question_label.place(x=135, y = 370)

question_input = ctk.CTkEntry(fen,
                    textvariable= reponse,
                    bg_color='#22c7ff',
                    border_color="#007FFF",
                    width= 325,
                    height=60,
                    justify="left",
                    font = ("verdana",13),
                    text_color="black",
                    state='normal')
question_input.place(y=400,x=60)

boutton_envoi = ctk.CTkButton(fen, text="Rechercher",image=search1,
                        font=("Arial", 12, "bold"),
                        bg_color="#22c7ff",
                        fg_color="#000ce5",
                        compound='right',
                        height=45,
                        width=130,
                        command=start_animation
                        )
boutton_envoi.place(x = 160,y = 470)

#=================================CREATION D'UN FRAME===========================================
frame = ctk.CTkFrame(fen, width=435,height=80,
                    bg_color="#22c7ff",
                    fg_color="white")
frame.place(x =7 , y = 68)

#=============================PARTIE REGLAGE=====================================================
reglages= ctk.CTkLabel(fen,text="Réglages",image=reglage_icon, compound='right',
                    bg_color="white",
                    height=20,
                    text_color='black',
                    font= ("verdana",13,"bold")
                    ).place(x = 170,y = 70)

#==============================configureURATION DU MODE VOCAL========================================
lecture_label= ctk.CTkLabel(fen,text="Lecture",
                    bg_color='white',
                    text_color='black',
                    font= ("verdana",14)).place(x = 20,y = 90)

sound = ctk.CTkButton(fen,
                text="Mode Vocal",
                bg_color='white',
                fg_color="#007FFF",
                font=("verdana",11,"bold"),
                image = off,
                border_width = 0,
                width=35,
                height=25,
                command=switch
                )
sound.place(x = 20,y = 116)

#==============================configureURATION DE LA LANGUE==========================================
langue= ctk.CTkLabel(fen,text="Langue",
                    bg_color='white',
                    text_color='black',
                    width=20,
                    font= ("verdana",14)).place(x = 155,y = 90)

fr_en = ctk.CTkComboBox(fen, values = ["Francais","Anglais"],
                    height=27,
                    width= 85,
                    bg_color = "white",
                    text_color="black",
                    border_color="#007FFF",
                    font=("verdana",9,"bold"),
                    state= "readonly")
fr_en.place(x = 155,y = 116)
fr_en.set("Francais")

#==============================CONFIGURATION DU NOMBRE DE PHRASES====================================
phrase_label = ctk.CTkLabel(fen, text = "Nombre de Phrases",
                    bg_color='white',
                    text_color='black',
                    font=("verdana",13)).place(x = 270,y = 90)
phrase_entry = CTkSpinbox(fen,
                        width= 90,
                        height = 27,
                        border_color="#007FFF",
                        fg_color="white",
                        font=("verdana",9,"bold"),
                        start_value = 2,
                        min_value = 2,
                        max_value = 10,
                        step_value=1,
                        state= "readonly")
phrase_entry.place(x = 270,y = 116)

#==============================PARTIE POUR LE COPYRIGHT===================================================================
copyright = ctk.CTkLabel(fen,text='Copyright © 2024 NDIAW_NDIAYE ',
                    bg_color='#22c7ff',
                    text_color='blue',
                    font=('arial',10,'bold')).pack(pady = 3,anchor="s",side="bottom")

fen.mainloop()