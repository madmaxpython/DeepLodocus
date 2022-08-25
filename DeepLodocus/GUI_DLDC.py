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
from utils import tkAskString

OUTPUT_PATH = str(Path(__file__).parent)
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

with open(OUTPUT_PATH + "/config.txt", "r") as config:
    config = json.loads(config.read())


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def run():
    save()
    FILE_NAME = str(tkAskString('Save your file', 'Output File Name'))
    os.system('python ' + OUTPUT_PATH + '/main.py ' + FILE_NAME)


def selectzone():
    global config
    save()
    os.system('python ' + OUTPUT_PATH + '/calibvideo.py')


def save():
    global config

    ZoneName = entry_1.get()
    if ZoneName != '':
        config['zone_name'] = list(ZoneName.split(" "))

    strconfig = json.dumps(config)

    # Write the file out again
    with open(OUTPUT_PATH + '/config.txt', 'w') as file:
        file.write(strconfig)

    with open(OUTPUT_PATH + '/config.txt', "r") as config:
        config = json.loads(config.read())


def MakeTrue(val, button):
    global config
    if config[val] == True:
        config[val] = False
        button.config(image=off)
    elif config[val] == False:
        config[val] = True
        button.config(image=on)


window = Tk()

window.geometry("1200x840")
window.configure(bg="#6EABF2")
window.title("DeepLodocus - Deep Localization Document's User")

off = PhotoImage(file=relative_to_assets("button_off.png"))
on = PhotoImage(file=relative_to_assets("button_on.png"))

canvas = Canvas(
    window,
    bg="#6EABF2",
    height=840,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    924.0,
    319.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    924.0,
    644.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    342.0,
    488.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    311.0,
    107.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    1029.0,
    114.0,
    image=image_image_5
)

canvas.create_text(
    108.0,
    218.0,
    anchor="nw",
    text="Measures to extracts",
    fill="#000000",
    font=("Inter Bold", 28 * -1)
)

canvas.create_text(
    758.0,
    219.0,
    anchor="nw",
    text="Video editing",
    fill="#000000",
    font=("Inter Bold", 28 * -1)
)

canvas.create_text(
    757.0,
    525.0,
    anchor="nw",
    text="Ready to go ?",
    fill="#000000",
    font=("Inter Bold", 28 * -1)
)

canvas.create_text(
    211.0,
    313.0,
    anchor="nw",
    text="Distance ",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

canvas.create_text(
    211.0,
    392.0,
    anchor="nw",
    text="Time in zone",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

canvas.create_text(
    211.0,
    555.0,
    anchor="nw",
    text="Entries in zone",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

canvas.create_text(
    211.0,
    633.0,
    anchor="nw",
    text="Average speed",
    fill="#000000",
    font=("Inter Regular", 24 * -1)
)

button_save_image = PhotoImage(
    file=relative_to_assets("button_save.png"))
button_save = Button(
    image=button_save_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: save(),
    relief="flat"
)
button_save.place(
    x=447.0,
    y=715.0,
    width=165.0,
    height=60.0
)

button_crop_image = PhotoImage(
    file=relative_to_assets("button_crop.png"))
button_crop = Button(
    image=button_crop_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: os.system('python ' + OUTPUT_PATH + '/videoCrop.py'),
    relief="flat"
)
button_crop.place(
    x=874.0,
    y=279.0,
    width=180.0,
    height=59.0
)

button_convert_image = PhotoImage(
    file=relative_to_assets("button_convert.png"))
button_3 = Button(
    image=button_convert_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("To Be Attribute"),
    relief="flat"
)
button_3.place(
    x=874.0,
    y=369.0,
    width=180.0,
    height=60.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    262.0,
    483.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=172.0,
    y=458.0,
    width=180.0,
    height=48.0
)

button_zone_image = PhotoImage(
    file=relative_to_assets("button_zone.png"))
button_zone = Button(
    image=button_zone_image,
    borderwidth=0,
    highlightthickness=0,
    command=selectzone,
    relief="flat"
)
button_zone.place(
    x=405.0,
    y=457.0,
    width=163.0,
    height=51.0
)

if config['analyse_distance']:
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_on.png"))
elif not config['analyse_distance']:
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_off.png"))
button_select_distance = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeTrue('analyse_distance', button_select_distance),
    relief="flat"
)
button_select_distance.place(
    x=405.0,
    y=305.0,
    width=92.0,
    height=44.0
)

if config['analyse_zone']:
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_on.png"))
elif not config['analyse_zone']:
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_off.png"))

button_select_zone = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeTrue('analyse_zone', button_select_zone),
    relief="flat"
)
button_select_zone.place(
    x=406.0,
    y=384.0,
    width=92.0,
    height=44.0
)

if config['analyse_entries']:
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_on.png"))
elif not config['analyse_entries']:
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_off.png"))
button_select_entries = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeTrue('analyse_entries', button_select_entries),
    relief="flat"
)
button_select_entries.place(
    x=398.0,
    y=552.0,
    width=92.0,
    height=44.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_on.png"))
button_select_velocity = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_select_velocity.place(
    x=398.0,
    y=633.0,
    width=92.0,
    height=44.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    149.0,
    573.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    149.0,
    654.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    143.0,
    406.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    142.0,
    327.0,
    image=image_image_9
)

button_run_image = PhotoImage(
    file=relative_to_assets("button_run.png"))
button_run = Button(
    image=button_run_image,
    borderwidth=0,
    highlightthickness=0,
    command=run,
    relief="flat"
)
button_run.place(
    x=870.0,
    y=705.0,
    width=203.0,
    height=60.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=871.0,
    y=594.0,
    width=203.0,
    height=60.0
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    803.0,
    309.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    810.0,
    401.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    807.0,
    624.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    805.0,
    735.0,
    image=image_image_13
)
window.resizable(False, False)
window.mainloop()
