import tkinter as tk
from functions import yes_button_clicked
from fixed_values import language_moz

if language_moz == 'NL':
    yes = 'Ja'
    no = 'Nee'
    label = 'Nu het Mozzeno-script laten lopen?'
else:
    yes = 'Oui'
    no = 'Non'
    label = 'Exécutez le script Mozzeno maintenant?'

popup = tk.Tk()
popup.geometry('400x100')
popup.eval('tk::PlaceWindow . center')
popup.title("Mozzeno")

label_text = tk.Label(popup, text=label)
label_text.pack(pady=5)

button_frame = tk.Frame(popup)
button_frame.pack(pady=10)
button_yes = tk.Button(button_frame, text=yes, command=lambda: yes_button_clicked(popup)) # lambda needed to use arguments
button_no = tk.Button(button_frame, text=no, command=popup.destroy)
button_yes.grid(row=0, column=0, padx=10)
button_no.grid(row=0, column=1, padx=10)

popup.mainloop()
