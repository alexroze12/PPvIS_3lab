from pygame_functions import *


def enter_name():
    screenSize(1020, 750)
    wordBox = makeTextBox(10, 80, 300, 0, 'Enter name, please', 0, 24)
    showTextBox(wordBox)
    entry = textBoxInput(wordBox)
    return entry
