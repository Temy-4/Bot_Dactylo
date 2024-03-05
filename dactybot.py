##Specifically designed for dactylo.djopa.fr
##will be updated
##Don't forget to put the focus on the type zone
from PIL import Image,ImageTk
from tkinter import *
import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import PIL.Image
import pyautogui
import sys
import threading


myconfig = r"--psm 8 --oem 3 -c tessedit_char_blacklist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --dpi 1000"
write = False

def bot_de_saisie(texte):
    # Saisie du texte avec un délai très court pour maximiser la vitesse
    pyautogui.write(texte, interval=0.02)
    
def clean_text(text):
    # Supprimer les caractères indésirables, par exemple, ici, nous supprimons les espaces et les caractères non alphabétiques
    cleaned_text = ''.join(char for char in text if char.isalpha() or char.isspace())
    return cleaned_text.strip()

def dactybot():
    global write
    
    while write:
    
        #capturer la zone de la fenêtre correspondant au mot 
        cap = ImageGrab.grab(bbox=(450, 522, 1300, 730))
        cap_arr = np.array(cap)
        #mise de l'image en deux dimensions et en noir sur blanc,c'est plus facile
        cap_arr = cv2.cvtColor(cap_arr, cv2.COLOR_BGR2GRAY)
        #application d'un masque pour l'image
        #tous les pixels sombres deviennent noirs
        cap_arr[cap_arr<100]=0
        #tous les pixels clairs deviennent blancs
        cap_arr[cap_arr>185]=255
        #👇🏾retirer le commentaire pour visualiser l'image capturée
        #cv2.imshow("Capture d'écran", cap_arr)
        #conversion de l'image en texte
        text = pytesseract.image_to_string(PIL.Image.fromarray(cap_arr), config=myconfig)
        # nettoyer le texte des caractères indésirables
        cleaned_text = clean_text(text)
        #saisie du texte lu et nettoyé
        bot_de_saisie(cleaned_text)
        #print(text)
        #print(cleaned_text)
        if not write:
            print("Thread dactybot stopping")
            break
        
        
def switch():
    global write
    #assure le switch visuel entre le mode on et off du bouton
    if button['text'] == 'Start DactyBot ':
        button.config(image=on)
        button.config(text='Stop DactyBot ')
        button.config(bg='#149181')
        button.config(fg='#f0ebef')
        write = True
        threading.Thread(target=dactybot).start()  # Démarre dactybot dans un thread séparé
    else:
        button.config(image=off)
        button.config(text='Start DactyBot ')
        button.config(bg='#f0ebef')
        button.config(fg='#0d0d0d')
        write = False
        
# Fonction pour arrêter proprement le programme
def stop_program():
    global write
    write = False  # Indique au thread de se terminer
    window.quit()  # Ferme la fenêtre Tkinter
    window.destroy()  # Assure la destruction complète de tous les widgets
    sys.exit()  # Quitte Python


    
window = Tk()
button = Button(window,text='Start DactyBot ')
button.pack()
button.config(font=('plus jakarta sans',15))
button.config(bg='#f0ebef')
button.config(activebackground='#0d0d0d')
button.config(activeforeground='#0d0d0d')
off = PhotoImage(file='robot.png')
on = PhotoImage(file='robot(1).png')
on = on.subsample(15, 15)
off = off.subsample(15, 15)
button.config(image=off)
button.config(compound='right')
button.config(command=switch)
exit = Button(window,text='Exit')
exit.pack()
exit.config(font=('plus jakarta sans',15))
exit.config(compound='bottom')
exit.config(bg='#911425')
# Ajout de l'action d'arrêt au bouton Exit
exit.config(command=stop_program)

window.mainloop()





















