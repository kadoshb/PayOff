import PySimpleGUI as sg
import time
import general_error


class export_file:
    def __init__(self, file_name):  # string of full address of the export file

        # file name preparation - from full file address gets the file name
        file_name = file_name[::-1]  # turn over to isolate the name of the file
        file_name = file_name[0:file_name.index("/")]  # according to windows address structure
        file_name = file_name[::-1]  # turns over again - to right order

        # date (month and year) preparation - from file name gets month and year
        len_error = 0
        character_error = 0
        structure_error = 0

        # input check: len error, length of file name assuming - 01.2022 or 11.2021
        if len(file_name) < 7:
            len_error = 1

        # input check: character error
        for i in file_name:
            if i == "_" or not ord(i) >= 48 and not ord(i) <= 57 or not ord(i) >= 65 and not ord(i) <= 90 or not ord(i) >= 97 and not ord(i) <= 122:
                character_error = 1

        #  input check: structure error
        struc_num = 0
        for i in file_name:
            if i == "_":
                struc_num += 1
        if not struc_num == 2:
            structure_error = 1


    def check_data(self, fila_name):



    def main(self, file_name):

        cur_year = time.localtime()[0]  # int
        cur_month = time.localtime()[1]  # int
        cur_day = time.localtime()[2]  # int
        cur_hour = time.localtime()[3]  # int
        cur_min = time.localtime()[4]  # int

        # case1: export file name is ok, month and year are recognized
        if len_error == 0 and character_error == 0 and structure_error == 0:
            month = ""
            year = ""
            for i in file_name:
                if i == "_" and file_name[file_name.index("_") + 3] == "_":  # months: 10, 11, 12
                    month = int(file_name[file_name.index("_") + 1:file_name.index("_") + 3])
                    year = int(file_name[file_name.index("_") + 4:file_name.index("_") + 8])
                    break
                elif i == "_" and file_name[file_name.index("_") + 2] == "_":  # months: 1-9 or 01-09
                    month = int(file_name[file_name.index("_") + 1:file_name.index("_") + 2])
                    year = int(file_name[file_name.index("_") + 3:file_name.index("_") + 7])
                    break

        # case2: otherwise
        else:
            design = [[":מצטערים לא הצלחנו לזהות את תאריך החודש, אנא הכנס/י ידנית", "", "Arial 14", "black", "white", (50, 3), 5, "c", True, ""],  # text1: headline
                      ["", "month", "Arial 12", "black", "white", (10, 3), 5, "c", True, False, ""],  # input1: month
                      [":חודש", "", "Arial 12", "black", "white", (10, 3), 5, "c", True, ""],  # text2: month
                      ["", "year", "Arial 12", "black", "white", (10, 3), 5, "c", True, False, ""],  # input2: year
                      [":שנה", "", "Arial 12", "black", "white", (10, 3), 5, "c", True, ""],  # text2: year
                      ["פתח/י קובץ", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י כדי לפתוח את קובץ החיוב"],  # button1: open file
                      ["ביטול", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י לביטול"],  # button2: cancel
                      ["PayOff", "layout", (600, 600), True, "c"]]  # window

            error_layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3],
                                     background_color=design[0][4], size=design[0][5], pad=design[0][6],
                                     justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
                            [sg.Input(default_text=design[1][0], key=design[1][1], font=design[1][2],
                                      text_color=design[1][3], background_color=design[1][4], size=design[1][5],
                                      pad=design[1][6], justification=design[1][7], visible=design[1][8],
                                      disabled=design[1][9], tooltip=design[1][10]),
                             sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3],
                                     background_color=design[2][4], size=design[2][5], pad=design[2][6],
                                     justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
                            [sg.Input(default_text=design[3][0], key=design[3][1], font=design[3][2],
                                      text_color=design[3][3], background_color=design[3][4], size=design[3][5],
                                      pad=design[3][6], justification=design[3][7], visible=design[3][8],
                                      disabled=design[3][9], tooltip=design[3][10]),
                             sg.Text(design[0][0], key=design[4][1], font=design[4][2], text_color=design[4][3],
                                     background_color=design[4][4], size=design[4][5], pad=design[4][6],
                                     justification=design[4][7], visible=design[4][8], tooltip=design[4][9])],
                            [sg.Button(design[5][0], key=design[5][1], font=design[5][2], button_color=design[5][3],
                                       size=design[5][4], pad=design[5][5], visible=design[5][6], disabled=design[5][7],
                                       tooltip=design[5][8]),
                             sg.Button(design[6][0], key=design[6][1], font=design[6][2], button_color=design[6][3],
                                       size=design[6][4], pad=design[6][5], visible=design[6][6], disabled=design[6][7],
                                       tooltip=design[6][8])]]

            window = sg.Window(title=design[7][0], layout=error_layout, size=design[7][2], modal=design[7][3],
                               element_justification=design[7][4])

            year = ""
            month = ""
            error = 1
            mon = 0
            while error == 1:
                event, values = window.read()
                if event == "ביטול" or event == sg.WINDOW_CLOSED:
                    break
                elif values['month'] == "" or values['year'] == "" or\
                        len(values['month']) > 2 or not len(values['year']) == 4 or\
                        int(values['year']) > cur_year or\
                        (int(values['month']) > cur_month and
                         int(values['year']) == cur_year):
                    general_error("!יש להכניס ערכים תקינים")
                elif event == "פתח/י קובץ":
                    month = values['year']
                    year = values['month']

                    if len(month) == 1 and len(year) == 4:
                        month = "0" + month
                        error = 0
                        break
                    elif len(month) == 2 and len(year) == 4:
                        error = 0
                        break
            window.close()




file = "C:/Users/97250/Desktop/PayOff/Export_12_2020.xls"
