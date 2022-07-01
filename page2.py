from tkinter import *
from typing import Counter

counter = 60
def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1000x600")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background_1.png")
background = canvas.create_image(
    506.5, 239.0,
    image=background_img)

canvas.create_text(
    360.0, 112.5,
    text = "YOUR AGILITY SCORE :",
    fill = "#000000",
    font = ("RalewayRoman-ExtraBold", int(35.0)))

canvas.create_text(
    680, 109.5,
    text = "{}".format(counter),
    fill = "#fa2121",
    font = ("RalewayRoman-Regular", int(40.0)))

canvas.create_text(
    600, 191.5,
    text = "22",
    fill = "#fa2121",
    font = ("RalewayRoman-Regular", int(40.0)))

canvas.create_text(
    320.0, 194.5,
    text = "EXPECTED SCORE :",
    fill = "#000000",
    font = ("RalewayRoman-ExtraBold", int(35.0)))

canvas.create_text(
    164, 276.5,
    text = "DIET : ",
    fill = "#fa2121",
    font = ("RalewayRoman-ExtraBold", int(35.0)))

canvas.create_text(
    184, 322.0,
    text = "THIS IS YOUR DIET",
    fill = "#000000",
    font = ("OpenSansRoman-Light", int(15.0)))

img0 = PhotoImage(file = f"img0_1.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 403, y = 466,
    width = 194,
    height = 57)

window.resizable(False, False)
window.mainloop()
