import logging
from osgeo import gdal, gdal_array
import os

import PySimpleGUI as sg
from matplotlib import pyplot as plt

from tools.config import read_config
from tools import window_tools

#logger = logging.


config = read_config("config.json")

# Read in Datasets
datasets = {}

for item in config["Datasets"].items():
    print(item[0], item[1])
    
    if os.path.isfile(item[1]):
        datasets[item[0]] = {"dataset": gdal.Open(item[1], gdal.GA_ReadOnly),
                             "raster": gdal_array.LoadFile(item[1])}
    else:
        print("Error! {} is not a file!".format(item[1]))

# layout = [
#     [sg.Text("Plot test")],
#     [sg.Canvas(key="-CANVAS-")],
#     [sg.Button("Ok")],
# ]

# Taken from https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py
layout = [
    [sg.T('Display')],
    [sg.B('Plot'), sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.B('Alive?')]

]

# Create the form and show it without the plot
window = sg.Window(
    "Mars Habitability Explorer",
    layout,
    location=(0, 0),
    # finalize=True,
    # element_justification="center",
    font="Helvetica 18",
)


while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    elif event == 'Plot':
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------
        plt.imshow(datasets["MOLA"]["raster"])
        plt.title('MOLA')

        # ------------------------------- Instead of plt.show()
        window_tools.draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()

# Add the plot to the window
# window_tools.draw_figure(window["-CANVAS-"].TKCanvas, fig)
#
# event, values = window.read()
#
# window.close()


































