import tkinter as tk
from functions import yes_button_clicked
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
popup.geometry('400x100')
popup.eval('tk::PlaceWindow . center')
popup.title("Mozzeno")

# Creating a button widget
button_no = tk.Button(popup, text=no, command=popup.destroy).place(x=200, y=30)
button_yes = tk.Button(popup, text=yes, command=yes_button_clicked).place(x=150, y=30)
button_close = tk.Button(popup, text=close, command=popup.destroy).place(x=165, y=60)
label_text = tk.Label(popup, text=label)
label_text.pack()

popup.mainloop()
