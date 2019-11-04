import tkinter as tk
import requests
from googletrans import Translator

translator = Translator()
def do_translation(translate_this):
    translate_to = ["en","fr","es","it"]
    out = ""
    for i in translate_to:
        out=out+i + ": " + translator.translate(translate_this, dest=i).text+"\n"

    label['text'] = out
    #print(out)

HEIGHT = 500
WIDTH = 600

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='ny.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


frame = tk.Frame(root, bg='#AA8C03', bd=2)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

#button = tk.Button(frame, text="Uebersetzen", font=40, command = do_translation(entry.get()))
button = tk.Button(frame, text="Uebersetzen", font=40, command=lambda: do_translation(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#AA8C03', bd=3)
lower_frame.place(relx=0.5, rely=0.55, relwidth=0.75, relheight=0.3, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()
