import PySimpleGUI as sg


class geneal_error:
    def __init__(self, text):
        design = [[text, "", "Arial 14", "black", "white", (50, 3), 0, "c", True, ""],
                  ["PayOff", "layout", (800, 600), True, "c"]]
        layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3],
                           background_color=design[0][4], size=design[0][5], pad=design[0][6],
                           justification=design[0][7], visible=design[0][8], tooltip=design[0][9])]]

        window = sg.Window(title=design[1][0], layout=layout, size=design[1][2], modal=design[1][3],
                           element_justification=design[1][4])

        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WINDOW_CLOSED:
                break
        window.close()

