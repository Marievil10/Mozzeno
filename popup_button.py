import tkinter as tk
from tkinter import *
from functions import yes_button_clicked, no_button_clicked
from fixed_values import language_moz

if language_moz == 'NL':
    yes = 'Ja'
    no = 'Nee'
    close = 'Sluiten'
    label = 'Nu het Mozzeno-script laten lopen?'
else:
    yes = 'Oui'
    no = 'Non'
    close = 'Fermer'
    label = 'Exécutez le script Mozzeno maintenant?'

popup = tk.Tk()
popup.eval('tk::PlaceWindow . center')
popup.title("Mozzeno")

# Creating a button widget
button_yes = tk.Button(popup, text=yes, command=yes_button_clicked).pack(side=LEFT)
button_no = tk.Button(popup, text=no, command=no_button_clicked).pack(side=RIGHT)
button_close = tk.Button(popup, text=close, command=popup.destroy).pack(side=BOTTOM)
label_text = tk.Label(popup, text=label)
label_text.pack()

popup.mainloop()
