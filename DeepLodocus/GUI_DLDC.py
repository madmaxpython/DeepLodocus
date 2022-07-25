#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:39:14 2022

@author: maximeteixeira
"""

import os
import json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = str(Path(__file__).parent)
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

with open("config.txt", "r") as config:
    config = json.loads(config.read())

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def run():
    os.system('python '+ OUTPUT_PATH+'/main.py')

def selectzone():
    os.system('python '+ OUTPUT_PATH+'/calibvideo.py')
    
    
def save():
    global config
    
    entre = entry_1.get()
    config['zone_name']= list(entre.split(" "))
    strconfig=json.dumps(config)
    print(strconfig)
    
    # Write the file out again
    with open(OUTPUT_PATH+'/config.txt', 'w') as file:
        file.write(strconfig)
        
    with open(OUTPUT_PATH+'/config.txt', "r") as config:
        config = json.loads(config.read())
    
    print(config)
    
    
def MakeTrue(val,button ):
    global config
    if config[val]==True:
        config[val]=False
        button.config(image=off)
    elif config[val]==False:
        config[val]=True
        button.config(image=on)

window = Tk()

window.geometry("1178x769")
window.configure(bg = "#FFFFFF")
window.title("DeepLodocus - Deep Localization Document's User")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 769,
    width = 1178,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1178.0,
    126.0,
    fill="#6EAAF2",
    outline="")

off=PhotoImage(file=relative_to_assets("button_off.png"))
on=PhotoImage(file=relative_to_assets("button_on.png"))

button_image_1 = PhotoImage(
    file=relative_to_assets("button_save.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: save(),
    relief="flat"
)
button_1.place(
    x=161.0,
    y=620.0,
    width=165.0,
    height=61.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_calibrate.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("useless button"),
    relief="flat"
)
button_2.place(
    x=663.0,
    y=627.0,
    width=202.0,
    height=47.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_selectzone.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=selectzone,
    relief="flat"
)
button_3.place(
    x=245.0,
    y=408.0,
    width=163.0,
    height=51.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_run.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=run,
    relief="flat"
)
button_4.place(
    x=925.0,
    y=627.0,
    width=202.0,
    height=47.0
)
button_image_zone = PhotoImage(
    file=relative_to_assets("button_on.png"))
button_zone = Button(
    image=button_image_zone,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:MakeTrue('analyse_zone', button_zone),
    relief="flat"
)
button_zone.place(
    x=259.0,
    y=322.0,
    width=149.0,
    height=51.0
)

button_image_distance = PhotoImage(
    file=relative_to_assets("button_on.png"))
button_distance = Button(
    image=button_image_distance,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeTrue('analyse_distance', button_distance),
    relief="flat"
)
button_distance.place(
    x=258.0,
    y=236.0,
    width=149.0,
    height=51.0
)

button_image_entries = PhotoImage(
    file=relative_to_assets("button_on.png"))
button_entries = Button(
    image=button_image_entries,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeTrue('analyse_entries', button_entries),
    relief="flat"
)
button_entries.place(
    x=259.0,
    y=510.0,
    width=149.0,
    height=51.0
)
canvas.create_text(
    47.0,
    162.0,
    anchor="nw",
    text="Measures to extracts",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

canvas.create_text(
    720.0,
    162.0,
    anchor="nw",
    text="Parameters",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

canvas.create_text(
    69.0,
    251.0,
    anchor="nw",
    text="Distance ",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

canvas.create_text(
    69.0,
    330.0,
    anchor="nw",
    text="Time in zone",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

canvas.create_text(
    69.0,
    524.0,
    anchor="nw",
    text="Entries in zone",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    137.0,
    432.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=47.0,
    y=399.0,
    width=180.0,
    height=64.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    994.0,
    294.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F0EDED",
    highlightthickness=0
)
entry_2.place(
    x=947.0,
    y=274.0,
    width=94.0,
    height=39.0
)

canvas.create_text(
    743.0,
    282.0,
    anchor="nw",
    text="Camera FPS",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    994.0,
    355.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#F0EDED",
    highlightthickness=0
)
entry_3.place(
    x=947.0,
    y=335.0,
    width=94.0,
    height=39.0
)

canvas.create_text(
    743.0,
    343.0,
    anchor="nw",
    text="Number of animals",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    994.0,
    419.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#F0EDED",
    highlightthickness=0
)
entry_4.place(
    x=947.0,
    y=399.0,
    width=94.0,
    height=39.0
)

canvas.create_text(
    743.0,
    407.0,
    anchor="nw",
    text="Pixel size",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)



image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1051.0,
    63.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    271.0,
    62.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()
