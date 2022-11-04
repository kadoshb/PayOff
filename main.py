import math
import ssl
from math import nan
import pandas as pd
import tkinter as tk
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from tkinter import filedialog
import os
import sqlite3
import PySimpleGUI as sg
import matplotlib.pyplot as plotter
import smtplib
import ssl
import socket
import time
import datetime
import pyautogui
import csv

# current date
cur_year = time.localtime()[0] # int
cur_month = time.localtime()[1] # int
cur_day = time.localtime()[2] # int
cur_hour = time.localtime()[3] # int
cur_min = time.localtime()[4] # int

time_to_change_day = 24 - cur_hour

# users screen size and ip
screen_size = pyautogui.size()
width = screen_size[0] # int
hight = screen_size[1] # int


# screen size check and error
def general_error(text):  # prints text
    design = [[text, "", "Arial 14", "black", "white", (50, 3), 0, "c", True, ""],
              ["PayOff", "layout", (800, 600), True, "c"]]
    layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])]]

    window = sg.Window(title=design[1][0], layout=layout, size=design[1][2], modal=design[1][3], element_justification=design[1][4])

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
    window.close()


if not width == 1920 and not hight == 1080:  # check screen resolution
    general_error("!שגיאה יש להפעיל את התוכנה ברזולוציה מלאה (1080*1980)")
    exit()


# directory check, create directory in desktop if needed
first_dir = 0
first_run = 0
filename = 'database.db'
directory = "PayOff"
friends_names = [['בר'], ['לירן זקס'], ['עמית אליהו'], ['מיה הראל'], ['יוסי קדוש'], ['עמוס וייס'], ['אופיר כהן'], ['דודו קדוש'], ['דודו גבאי']]

categories = [['food', 'אוכל וקניות'], ['gas', 'הוצאות רכב'], ['fun', 'בילויים'], ['food_out', 'אוכל בחוץ'], ['flat', 'חשבונות בית'], ['private', 'חשבונות פרטיים'],
              ['clothes', 'ביגוד והנעלה'], ['equipment', 'ציוד ואביזרים'], ['bit', 'העברות ביט'], ['cash', 'משיכות מזומן'], ['abroad', 'חו"ל וטיולים'], ['other', 'הוצאות אחרות']]

cats = ['food', 'gas', 'fun', 'food_out', 'flat', 'private', 'clothes', 'equipment', 'bit', 'cash', 'abroad', 'other']

parent_dir = "C:/"
dir_list = os.listdir(parent_dir)

if "Users" in dir_list:  # check for directory (folder) in english computer
    parent_dir = "C:/Users/"
    dir_list = os.listdir(parent_dir)
    for i in dir_list:
        parent_dir += i + "/" + "Desktop"
        mode = 0o666
        path = os.path.join(parent_dir, directory)

        if os.path.exists(path):
            first_dir = 1
            break

    user_address = socket.gethostbyname(socket.gethostname())
    if user_address == "192.168.3.112":
        parent_dir = "C:/Users/Bark/Documents/GitHub"
    else:
        parent_dir = "C:/Users/97250/Documents/GitHub"
    dir_list = os.listdir(parent_dir)
    for i in dir_list:
        mode = 0o666
        path = os.path.join(parent_dir, directory)

        if os.path.exists(path):
            first_dir = 1
            break

else:  # check for directory (folder) in hebrew computer
    parent_dir = "C:/משתמשים/"
    dir_list = os.listdir(parent_dir)

    for i in dir_list:
        parent_dir += i + "/" + "שולחן העבודה"
        mode = 0o666
        path = os.path.join(parent_dir, directory)

        if os.path.exists(path):
            first_dir = 1
            break

if first_dir == 0:  # first time to use program - creates folder in desktop
    text = "אנא בחר/י את שם המשתמש של המחשב, כדי שנוכל ליצור עבורך :תיקיה בשולחן העבודה"
    design = [[text, "", "Arial 14", "black", "white", (45, 2), 0, "c", True, ""],
              ["button text", "", "Arial 12", ["white", "blue"], (20, 3), 20, True, False, ""],
              ["PayOff", "layout", (800, 600), True, "c"]]
    state = 0
    parent_dir = "C:/"
    dir_list = os.listdir(parent_dir)
    if "Users" in dir_list:
        parent_dir = "C:/Users/"
        dir_list = os.listdir(parent_dir)
    else:
        state = 1
        parent_dir = "C:/משתמשים/"
        dir_list = os.listdir(parent_dir)

    layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])]]
    for i in dir_list:
        layout.append([sg.Button(i, key=design[1][1], font=design[1][2], button_color=design[1][3], size=design[1][4], pad=design[1][5], visible=design[1][6], disabled=design[1][7], tooltip=design[1][8])])

    window = sg.Window(title=design[2][0], layout=layout, size=design[2][2], modal=design[2][3], element_justification=design[2][4])
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            event = ""
            break
    window.close()

    if not event == "" or not event == None:
        if state == 0:
            parent_dir = "C:/Users/" + event + "/Desktop"
        else:
            parent_dir = "C:/Users/" + event + "משתמשים/"
        mode = 0o666
        path = os.path.join(parent_dir, directory)
        os.mkdir(path, mode)
    else:
        exit()


# login function

def check_login1(user_name, user_password, friends_names):  # check input data and existing user
    ok = 1
    if user_name == "" and user_password == "":
        ok = 0
    elif user_name == "" or user_password == "":
        ok = 0
    else:
        ok = 2
        for i in friends_names:
            if user_name in i:
                ok = 1
    return ok


def check_login2(user_name, user_password, cur_user_name, cur_user_password):  # check input data and existing user
    ok = 1
    if user_name == "" and user_password == "":
        ok = 0
    elif user_name == "" or user_password == "":
        ok = 0
    else:
        ok = 2
        if user_name == cur_user[0] and user_password == cur_user[1]:
            ok = 1
    return ok


global user_name

# database check, create database in case has not done yet or deleted
if not os.path.exists(filename):  # if database does not exists in directory (folder)
    design = [["התחברות", "", "Arial 14", "black", "white", (30, 3), 5, "c", True, ""],
              ["", "name", "Arial 12", "black", "white", (20, 3), 2, "c", True, False, ""],
              [":שם משתמש", "", "Arial 12", "black", "white", (20, 3), 2, "c", True, ""],
              ["", "password", "Arial 12", "black", "white", (20, 3), 2, "c", True, False, ""],
              [":סיסמא", "", "Arial 12", "black", "white", (20, 3), 2, "c", True, ""],
              [":התחברות אוטומטית", "auto", "Arial 12", (20, 3), 3, False, "black"],
              [":זכור אותי", "remember", "Arial 12", (20, 3), 3, True, "black"],
              ["התחבר/י", "התחבר/י", "Arial 12", ["black", "blue"], (10, 2), 20, True, False, ""],
              ["PayOff", "", (800, 600), True, "c"]]

    open_memory_values = ['סך חיוב בש"ח:', 'עסקאות בחו' + chr(733) + 'ל', 'שם בית עסק', 'סכום חיוב', 'TOTAL FOR DATE',
                          'עסקאות בחו"ל', 'סך חיוב בש' + chr(733) + 'ח:']

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
              [sg.Input(default_text=design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], disabled=design[1][9], tooltip=design[1][10]),
               sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
              [sg.Input(default_text=design[3][0], key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[4][0], key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9])],
              [sg.Checkbox(design[5][0], key=design[5][1], font=design[5][2], size=design[5][3], pad=design[5][4], default=design[5][5], text_color=design[5][6]),
               sg.Checkbox(design[6][0], key=design[6][1], font=design[6][2], size=design[6][3], pad=design[6][4], default=design[6][5], text_color=design[6][6])],
              [sg.Button(design[7][0], key=design[7][1], font=design[7][2], button_color=design[7][3], size=design[7][4], pad=design[7][5], visible=design[7][6], disabled=design[7][7], tooltip=design[7][8])]]

    window = sg.Window(title=design[8][0], layout=layout, size=design[8][2], modal=design[8][3], element_justification=design[8][4])
    ok = 0
    while ok == 0 or ok == 2:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            exit()
        elif ok == 2:
            general_error("שגיאה! שם משתמש ו/או סיסמא לא נכונים")
        elif event == "התחבר/י":
            user_name = values['name']
            user_password = values['password']
            user_address = socket.gethostbyname(socket.gethostname())
            user_remember = values['remember']
            user_auto = values['auto']
            ok = check_login1(user_name, user_password, friends_names)
    window.close()

    for i in categories:
        cursor.executescript("""

                CREATE TABLE """ + i[0] + """(
                    name
                    );
            """)
        connection.commit()
    cursor.executescript("""
        CREATE TABLE categories(
            key_name,
            display_name
            );
     
        CREATE TABLE open_memory(
            name
            );

        CREATE TABLE expenses(
            day,
            month,
            year,
            name,
            charge,
            category
            );

        CREATE TABLE analysis_exports(
            month,
            year,
            total_food,
            total_gas,
            total_fun,
            total_food_out,
            total_flat_bills,
            total_private_bills,
            total_clothes,
            total_equipment,
            total_bit,
            total_cash,
            total_other,
            total_abroad,
            total,
            income,
            current
            );

        CREATE TABLE login(
            user,
            password,
            address,
            remember,
            auto,
            log_day,
            log_month,
            log_year
            );
        
        CREATE TABLE flow_exports(
            month,
            year,
            total_food,
            total_gas,
            total_fun,
            total_food_out,
            total_flat_bills,
            total_private_bills,
            total_clothes,
            total_equipment,
            total_bit,
            total_cash,
            total_other,
            total_abroad,
            total,
            income,
            current
            );
            
        CREATE TABLE current(
            day,
            month,
            year,
            current
            );
    """)
    connection.commit()
    cursor.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_name, user_password, user_address, user_remember, user_auto, cur_day, cur_month, cur_year])
    connection.commit()

    for i in open_memory_values:
        cursor.execute("INSERT INTO open_memory VALUES (?)", [i])
        connection.commit()

# else run normally
else:  # if database exists in directory (folder)
    design = [["התחברות", "", "Arial 14", "black", "white", (30, 3), 5, "c", True, ""],
              ["", "name", "Arial 12", "black", "white", (20, 3), 2, "c", True, False, ""],
              [":שם משתמש", "", "Arial 12", "black", "white", (20, 3), 2, "c", True, ""],
              ["", "password", "Arial 12", "black", "white", (20, 3), 2, "c", True, False, ""],
              [":סיסמא", "", "Arial 12", "black", "white", (20, 3), 2, "c", True, ""],
              [":התחברות אוטומטית", "auto", "Arial 12", (20, 3), 3, False, "black"],
              [":זכור אותי", "remember", "Arial 12", (20, 3), 3, True, "black"],
              ["התחבר/י", "התחבר/י", "Arial 12", ["black", "blue"], (10, 2), 20, True, False, ""],
              ["PayOff", "", (800, 600), True, "c"]]
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM login")
    cur_user = cursor.fetchone()
    user_name = cur_user[0]
    user_password = cur_user[1]
    user_address = cur_user[2]
    user_remember = cur_user[3]
    user_auto = cur_user[4]
    log_day = cur_user[5]
    log_month = cur_user[6]
    log_year = cur_user[7]

    categories = []
    cats = []
    cursor.execute("SELECT * FROM categories")
    for i in cursor.fetchall():
        categories.append([i[0], i[1]])
        cats.append([i[0]])

    # check if user wants to log automatically
    if not cur_user[4] == 1 or not cur_user[2] == socket.gethostbyname(socket.gethostname()):
        layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
                  [sg.Input(default_text=design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], disabled=design[1][9], tooltip=design[1][10]),
                   sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
                  [sg.Input(default_text=design[3][0], key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
                   sg.Text(design[4][0], key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9])],
                  [sg.Checkbox(design[5][0], key=design[5][1], font=design[5][2], size=design[5][3], pad=design[5][4], default=design[5][5], text_color=design[5][6]),
                   sg.Checkbox(design[6][0], key=design[6][1], font=design[6][2], size=design[6][3], pad=design[6][4], default=design[6][5], text_color=design[6][6])],
                  [sg.Button(design[7][0], key=design[7][1], font=design[7][2], button_color=design[7][3], size=design[7][4], pad=design[7][5], visible=design[7][6], disabled=design[7][7], tooltip=design[7][8])]]

        window = sg.Window(title=design[8][0], layout=layout, size=design[8][2], modal=design[8][3], element_justification=design[8][4])
        ok = 0
        while ok == 0 or ok == 2:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                exit()
            elif ok == 2:
                general_error("שגיאה! שם משתמש ו/או סיסמא לא נכונים")
            elif event == "התחבר/י":
                check_user_name = values['name']
                check_user_password = values['password']
                user_address = socket.gethostbyname(socket.gethostname())
                user_remember = values['remember']
                user_auto = values['auto']
                ok = check_login2(check_user_name, check_user_password, user_name, user_password)
                if ok == 1:
                    cursor.executescript("""

                        DROP TABLE login;

                        CREATE TABLE login(
                            user,
                            password,
                            address,
                            remember,
                            auto,
                            log_year,
                            log_month,
                            log_day
                            );
                    """)
                    cursor.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                   [user_name, user_password, user_address, user_remember, user_auto, 2022, 5, 27])
                    connection.commit()
                    if not cur_user[2] == user_address:
                        try:
                            gmail_user = 'payoffapplication@gmail.com'
                            gmail_password = 'b8k2a2a0'
                            context = ssl.create_default_context()

                            sent_from = gmail_user
                            to = ['payoffapplication@gmail.com']
                            subject = 'New Login'
                            body = user_address

                            email_text = """\
                                                                    From: %s
                                                                    To: %s
                                                                    Subject: %s

                                                                    There is a new login from user: """ + user_name + """
                                                                     with ip address: """ + user_address + """
                                                                    %s
                                                                    """ % (sent_from, ", ".join(to), subject, body)

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls(context=context)

                            server.login(gmail_user, gmail_password)
                            server.sendmail(sent_from, to, email_text)
                            server.close()
                            parent_dir = "C:/"
                            dir_list = os.listdir(parent_dir)
                        except:
                            print("Error sending Email")
        window.close()

# create opening

if 5 <= cur_hour < 12:
    title = "!בוקר טוב " + user_name
elif 12 <= cur_hour < 16:
    title = "!צהריים טובים " + user_name
elif 16 <= cur_hour < 19:
    title = "!אחר הצהריים טובים " + user_name
elif 19 <= cur_hour < 21:
    title = "!ערב טוב " + user_name
else:
    title = "!לילה טוב " + user_name


# main functions

# check functions
def check_file_name(file, cur_month, cur_year):  # suppose to get: file - "Export_12_2020.xls" (str), cur_month (int), cur_year (int)
    design = [[":מצטערים לא הצלחנו לזהות את תאריך החודש, אנא הכנס/י ידנית", "", "Arial 14", "black", "white", (50,3), 5, "c", True, ""],  # text1: headline
              ["", "month", "Arial 12", "black", "white", (10, 3), 5, "c", True, False, ""],  # input1: month
              [":חודש", "", "Arial 12", "black", "white", (10, 3), 5, "c", True, ""],  # text2: month
              ["", "year", "Arial 12", "black", "white", (10, 3), 5, "c", True, False, ""],  # input2: year
              [":שנה", "", "Arial 12", "black", "white", (10, 3), 5, "c", True, ""],  # text2: year
              ["פתח/י קובץ", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י כדי לפתוח את קובץ החיוב"],  # button1: open file
              ["ביטול", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י לביטול"],  # button2: cancel
              ["PayOff", "layout", (600, 600), True, "c"]]  # window
    year = ""
    month = ""
    mon = 0
    error = 0
    a = 1
    for i in file:
        if i == "_" and file[a + 2] == "_":  # months: 10, 11, 12
            month = file[a:a + 2]
            mon = int(month[1])
            year = file[a + 3:len(file) - 4]
            break
        if i == "_" and file[a + 1] == "_":  # months: 1-9
            month = "0" + file[a]
            mon = int(month)
            year = file[a + 2:len(file) - 4]
            break
        a += 1

    if len(month) != 2 and len(year) != 4 or len(month) != 2 or len(year) != 4:
        error = 1

    if error == 1:
        error_layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
                        [sg.Input(default_text=design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], disabled=design[1][9], tooltip=design[1][10]),
                         sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
                        [sg.Input(default_text=design[3][0], key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
                         sg.Text(design[0][0], key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9])],
                        [sg.Button(design[5][0], key=design[5][1], font=design[5][2], button_color=design[5][3], size=design[5][4], pad=design[5][5], visible=design[5][6], disabled=design[5][7], tooltip=design[5][8]),
                         sg.Button(design[6][0], key=design[6][1], font=design[6][2], button_color=design[6][3], size=design[6][4], pad=design[6][5], visible=design[6][6], disabled=design[6][7], tooltip=design[6][8])]]

        window = sg.Window(title=design[7][0], layout=layout, size=design[7][2], modal=design[7][3], element_justification=design[7][4])

        year = ""
        month = ""
        error = 1
        mon = 0
        while error == 1:
            event, values = window.read()
            if event == "ביטול" or event == sg.WINDOW_CLOSED:
                break
            elif values['month'] == "" or values['year'] == "" or len(values['month']) > 2 or not len(values['year']) == 4 or int(values['year']) > cur_year or (int(values['month']) > cur_month and int(values['year']) == cur_year):
                general_error("!יש להכניס ערכים תקינים")
            elif event == "פתח/י קובץ":
                year = values['month']
                month = values['year']
                mon = 0

                if len(month) == 1:
                    month = "0" + month
                    mon = int(month)
                    if len(year) == 4:
                        error = 0
                        break
                elif len(month) == 2:
                    mon = int(month)
                    if len(year) == 4:
                        error = 0
                        break
        window.close()

    return error, year, month, mon


def check_report(month, year, analysis_exports):  # month export has already been opened in the past, asks for user decision to proceed or not
    design = [["!שים/י לב! חיוב זה כבר נפתח בעבר", "", "Arial 14", "black", "white", (30, 3), 5, "c", True, ""],  # text1: headline
              ["?להמשיך בכל זאת", "", "Arial 12", "black", "white", (30, 3), 5, "c", True, ""],  # text2: instructions
              ["כן", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י כדי לפתוח את קובץ החיוב"],  # button1: proceed
              ["לא", "", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, "לחצ/י כדי לפתוח את קובץ החיוב"], # button2: do not proceed
              ["PayOff", "layout", (600, 600), True, "c"]]  # window
    answer = ""
    a = 0
    for i in analysis_exports:
        if month == i[0] and year == i[1]:
            error_layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
                            [sg.Text(design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])],
                            [sg.Button(design[2][0], key=design[2][1], font=design[2][2], button_color=design[2][3], size=design[2][4], pad=design[2][5], visible=design[2][6], disabled=design[2][7], tooltip=design[2][8]),
                             sg.Button(design[3][0], key=design[3][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])]]

            window = sg.Window(title=design[4][0], layout=layout, size=design[4][2], modal=design[4][3], element_justification=design[4][4])

            while True:
                event, values = window.read()
                if event == "לא" or event == sg.WINDOW_CLOSED:
                    answer = "No"
                    break
                elif event == "כן":
                    answer = event
                    break
            window.close()
            break
        a += 1
    return answer, a


# data arrangement functions
def find_first_year(analysis_exports):  # first year means the year of the first export to display (latest export or flow)
    a = 0
    f_year_pos = 0
    f_year = analysis_exports[0][1]
    for i in analysis_exports:
        if int(i[1]) > int(f_year):
            f_year_pos = a
            f_year = i[1]
        a += 1
    return f_year_pos, f_year


def find_first_month(analysis_exports, f_year_pos):  # first month means the month of the first export to display (latest export or flow)
    a = 0
    f_month_pos = f_year_pos
    f_month = analysis_exports[f_year_pos][0]
    for i in analysis_exports:
        if int(i[0]) > int(f_month) and int(analysis_exports[a][1]) == int(analysis_exports[f_year_pos][1]):
            f_month_pos = a
            f_month = i[0]
        else:
            a += 1
    return f_month_pos, f_month


def find_last_year(analysis_exports):  # last year means the year of the last export to display (oldest export or flow)
    a = 0
    l_year_pos = 0
    l_year = analysis_exports[0][1]
    for i in analysis_exports:
        if int(i[1]) < int(l_year):
            l_year_pos = a
            l_year = i[1]
        a += 1
    return l_year_pos, l_year


def find_last_month(analysis_exports, l_year_pos):  # last month means the month of the last export to display (oldest export or flow)
    a = 0
    l_month = analysis_exports[l_year_pos][0]
    l_month_pos = l_year_pos
    for i in analysis_exports:
        if int(i[0]) < int(l_month) and int(analysis_exports[a][1]) == int(analysis_exports[l_year_pos][1]):
            l_month = i[0]
            l_month_pos = a
        else:
            a += 1
    return l_month_pos, l_month


def find_month(event, month_list, empty_month_list, cats):
    for i in month_list:
        if event[len(event) - 7:len(event)] == ".export":  # returns the chosen month exports itself (list of all categories, total, income al current)
            if len(event) == 15 or len(event) == 16:
                return empty_month_list[int(event[0:len(event) - 14])]
            elif event[0:len(event) - 14] == str(i[0]) + "." + str(i[1]):
                return i
        elif event[len(event) - 5:len(event)] == ".flow":  # returns the chosen month flow itself (list of all categories, total, income al current)
            if len(event) == 13 or len(event) == 14:
                return empty_month_list[int(event[0:len(event) - 12])]
            elif event[0:len(event) - 12] == str(i[0]) + "." + str(i[1]):
                return i
        else:  # returns the name from the right category, without .button
            for j in i:
                if event[0:len(event) - 7] == j:
                    return j
            for j in empty_month_list:
                for k in j:
                    if empty_month_list[cats.index(event[0:event.index(".")])][int(event[event.index("."):len(event) - 7])] == k:
                        return k


def make_averages(analysis_exports):  # makes averages for each category from all existing data
    averages = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    analysis_exports.reverse()
    for i in analysis_exports:
            for j in i[2:len(i)]:
                averages[i.index(j) - 2] = averages[i.index(j) - 2] + j
    for i in averages:
        i = i / len(analysis_exports)

    return averages


# errors and buttons functions


def update_buttons(window, month_list, empty_month_list, buttons_list, event, exports_to, cats):  # empty/month list - export/flow months or categories
    for i in buttons_list:
        if i[1] == event and event == "analysis" or event == "flow":  # adds all months
            if i[2] == 1:
                # selected state
                buttons_list[buttons_list.index(i)][2] = 0
                all_sub_buttons = 0
                window[event].update(text=i[0][0])
                exports_to = []
            else:
                # not selected state
                buttons_list[buttons_list.index(i)][2] = 1
                all_sub_buttons = 1
                window[event].update(text=i[0][1])
                exports_to = list(month_list)
            window[event].update(button_color=(i[3], i[4][all_sub_buttons]))
            for j in buttons_list:
                if not j[1] == event:
                    if not j[2] == all_sub_buttons:
                        buttons_list[buttons_list.index(j)][2] = all_sub_buttons
                        if all_sub_buttons == 0:
                            window[j[1]].update(text=j[0][0])
                        else:
                            window[j[1]].update(text=j[0][1])
                        window[j[1]].update(button_color=(i[3], j[4][all_sub_buttons]))
            break
        elif i[1] == event and event == "settings":  # adds all categories and their names
            if i[2] == 1:
                buttons_list[buttons_list.index(i)][2] = 0
                all_sub_buttons = 0
                window[event].update(text=i[0][0])
                exports_to = []
            else:
                buttons_list[buttons_list.index(i)][2] = 1
                all_sub_buttons = 1
                window[event].update(text=i[0][1])
                for j in month_list:
                    exports_to.append(j[0])
                    j = j[2:len(j)]
            window[event].update(button_color=(i[3], i[4][all_sub_buttons]))
            for j in buttons_list:
                if not j[1] == event:
                    if not j[2] == all_sub_buttons:
                        buttons_list[buttons_list.index(j)][2] = all_sub_buttons
                        if all_sub_buttons == 0:
                            window[j[1]].update(text=j[0][0])
                        else:
                            window[j[1]].update(text=j[0][1])
                        window[j[1]].update(button_color=(j[3], j[4][all_sub_buttons]))
            break
        elif i[1] == event and event[0:len(event) - 9] in cats:  # adds the name itself: food.settings - food
            if i[2] == 1:  # selected state
                buttons_list[buttons_list.index(i)][2] = 0
                all_sub_buttons = 0
                window[event].update(text=i[0][0])
                exports_to.remove(event[0:len(event) - 9])
            else:  # not selected state
                buttons_list[buttons_list.index(i)][2] = 1
                all_sub_buttons = 1
                window[event].update(text=i[0][1])
                exports_to.append(event[0:len(event) - 9])
            window[event].update(button_color=(i[3], i[4][all_sub_buttons]))
            for j in buttons_list:
                if not j[1] == event and not j[1] == "settings":
                    if j[1][0:len(j[1]) - 7] in categories[cats.index(event[0:len(event) - 9])]:
                        if not j[2] == all_sub_buttons:
                            buttons_list[buttons_list.index(j)][2] = all_sub_buttons
                            if all_sub_buttons == 0:
                                window[j[1]].update(text=i[0][0])
                            else:
                                window[j[1]].update(text=i[0][1])
                            window[j[1]].update(button_color=(i[3], j[4][all_sub_buttons]))
            break
        elif i[1] == event:
            if i[2] == 1:  # adds the name itself
                # selected state
                buttons_list[buttons_list.index(i)][2] = 0
                window[event].update(text=i[0][0])
                window[event].update(button_color=(i[3], i[4][0]))
                exports_to.remove(find_month(event, month_list, empty_month_list, cats))
            else:
                # not selected state
                buttons_list[buttons_list.index(i)][2] = 1
                window[event].update(text=i[0][1])
                window[event].update(button_color=(i[3], i[4][1]))
                exports_to.append(find_month(event, month_list, empty_month_list, cats))
    return exports_to


def reset_button(window, button_list, buttons_pars):  # brings all buttons from button_list to - not chosen state
    for i in button_list:
        if i[1] == buttons_pars[1]:
            window[i[1]].update(text=buttons_pars[0][0])
        else:
            window[i[1]].update(text=buttons_pars[2][0])
        i[2] = 0
        window[i[1]].update(button_color=(buttons_pars[7], buttons_pars[8][0]))


def change_button_color(window, button_list, key, background_color_one, background_color_all):  # changes all buttons color but one
    for i in button_list:
        if i == key:
            window[i].update(button_color=background_color_one)
        else:
            window[i].update(button_color=background_color_all)


# new month function
def sorting_layout(text, categories, empty_categories, cats, dates, names, charges):
    design = [[":אנחנו לא מכירים את ההוצאה הבאה", "", "Arial 14", "black", "white", (30, 3), "pad", "c", True, ""],  # sort layout headline 1
              [text, "", "Arial 12", "black", "white", (30, 3), "pad", "c", True, ""],  # sort layout headline 2
              ["?לאיזו קטגוריה שייכת ההוצאה", "", "Arial 14", "black", "white", (30, 3), "pad", "c", True, ""],  # sort layout headline 3
              ["button_text", "", "Arial 12", ["white", "blue"], (12, 2), 1, True, False, "בחר/י קטגוריה זו במידה והיא מתאימה להוצאה המדוברת"],  # sort layout buttons - categories
              ["text", "", "Arial 14", "black", "white", (20, 1), "1", "c", True, ""],  # export layout headlines
              ["text", "", "Arial 12", "black", "white", (20, 1), "1", "c", True, ""],  # sort layout names
              ["column_layout", "-col1-", "white", (400, 800), 1, "c", "c", True, True, True],  # sort layout
              ["column_layout", "-col2-", "white", (600, 800), 1, "c", "c", True, True, True],  # export layout
              ["PayOff", "layout", (1000, 800), True]]  # window

    sort_layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
                   [sg.Text(design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])],
                   [sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],

                   [sg.Button(categories[1][1], key=categories[1][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[0][1], key=categories[0][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button(categories[3][1], key=categories[3][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[2][1], key=categories[2][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button(categories[5][1], key=categories[5][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[4][1], key=categories[4][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button(categories[7][1], key=categories[7][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[6][1], key=categories[6][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button(categories[9][1], key=categories[9][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[8][1], key=categories[8][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button(categories[11][1], key=categories[11][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                    sg.Button(categories[10][1], key=categories[10][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])],
                   [sg.Button("דלג/י", key="דלג/י", font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])]]
    export_layout = [[sg.Text(":חיוב", key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9]),
                      sg.Text(":שם בית עסק", key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9]),
                      sg.Text(":תאריך", key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9])]]

    a = 0
    for i in names:
        if i == text:
            row = [sg.Text(charges.iloc[a], key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9]),
                   sg.Text(i, key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9]),
                   sg.Text(dates.iloc[a], key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9])]
            export_layout.append(row)
            a += 1
        else:
            row = [sg.Text(charges.iloc[a], key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9]),
                   sg.Text(i, key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9]),
                   sg.Text(dates.iloc[a], key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9])]
            export_layout.append(row)
            a += 1

    layout = [[sg.Column(sort_layout, key=design[6][1], background_color=design[6][2], size=design[6][3], pad=design[6][4], justification=design[6][5], element_justification=design[6][6], visible=design[6][7], scrollable=design[6][8], vertical_scroll_only=design[6][9]),
               sg.Column(export_layout, key=design[7][1], background_color=design[7][2], size=design[7][3], pad=design[7][4], justification=design[7][5], element_justification=design[7][6], visible=design[7][7], scrollable=design[7][8], vertical_scroll_only=design[7][9])]]
    window = sg.Window(title=design[8][0], layout=layout, background_color=design[8][2], size=design[8][3], modal=design[8][4])

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            a = 0
            break
        elif event == "דלג/י":
            a = 13
            break
        else:
            a = 1
            for i in categories: # first category choose (food) is a = 1 and not 0 because of exit option
                if event == i[1]:
                    break
                a += 1
            break
    window.close()
    return a


# analysis functions
def delete_month(window, connection, exports_to, month_list, empty_month_list, display_keys, analysis_exports_or_flow_exports, button_list): # for analysis and flow
    if analysis_exports_or_flow_exports == "analysis_exports":  # case: export month
        page1 = ".export"
        page2 = "export_"
        end = 14
    else: # case: flow month
        page1 = ".flow"
        page2 = "flow_"
        end = 12

    for i in exports_to: # make month un-visible
        if i in empty_month_list:
            for j in display_keys:
                window[str(empty_month_list.index(i)) + j + page1].update(visible=False)
        else:
            for j in display_keys:
                window[i[0] + "." + i[1] + j + page1].update(visible=False)

    if exports_to == month_list: # updates database, month list and button list
        cursor = connection.cursor()
        cursor.executescript("""

                    Drop TABLE """ + analysis_exports_or_flow_exports + """;

                    CREATE TABLE """ + analysis_exports_or_flow_exports + """(
                        month,
                        year,
                        total_food,
                        total_gas,
                        total_fun,
                        total_food_out,
                        total_flat,
                        total_private,
                        total_clothes,
                        total_equipment,
                        total_bit,
                        total_cash,
                        total_other,
                        total_abroad,
                        total,
                        income,
                        current
                        );
                """)
        connection.commit()

        for i in month_list:
            cursor.executescript("""
                                Drop TABLE """ + page2 + i[0] + "_" + i[1] + """;
                            """)
            connection.commit()
        month_list = []
        button_list = button_list[0:1]
        general_error("!חודשים נמחקו בהצלחה")

    else: # updates database, month list and button list
        cursor = connection.cursor()
        cursor.executescript("""

                    Drop TABLE """ + analysis_exports_or_flow_exports + """;

                    CREATE TABLE """ + analysis_exports_or_flow_exports + """(
                        month,
                        year,
                        total_food,
                        total_gas,
                        total_fun,
                        total_food_out,
                        total_flat,
                        total_private,
                        total_clothes,
                        total_equipment,
                        total_bit,
                        total_cash,
                        total_other,
                        total_abroad,
                        total,
                        income,
                        current
                        );
                """)
        connection.commit()

        for i in exports_to:
            if i in month_list:
                month_list.remove(i)
                for j in button_list:
                    if i[0] + "." + i[1] == j[1][0:len(j[1]) - end] or j[1][0:len(j[1]) - end] == int(empty_month_list.index(i)):
                        button_list.remove(j)
            cursor.executescript("""
                                Drop TABLE """ + page2 + i[0] + "_" + i[1] + """;
                            """)
            connection.commit()

        for k in month_list:
            cursor.execute(
                "INSERT INTO " + analysis_exports_or_flow_exports + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",
                [k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7],
                 k[8], k[9], k[10], k[11], k[12], k[13], k[14], k[15], k[16]])
            connection.commit()

        general_error("!חודשים נמחקו בהצלחה")

    for i in empty_month_list: #  # updatesempty month list
        empty_month_list[empty_month_list.index(i)] = []
    exports_to = []

    return month_list, empty_month_list, exports_to, button_list


def sort_analysis_exports(analysis_exports):  # sort order: latest to oldest
    temp_analysis_exports = []
    if bool(analysis_exports):  # if there are already exports
        [f_year_pos, f_year] = find_first_year(analysis_exports)
        [f_month_pos, f_month] = find_first_month(analysis_exports, f_year_pos)
        [l_year_pos, l_year] = find_last_year(analysis_exports)
        [l_month_pos, l_month] = find_last_month(analysis_exports, l_year_pos)
        # copy first month and year find and update
        a = f_month_pos
        while int(l_year) != int(f_year) and int(l_month) != int(f_month):
            temp_analysis_exports.append(analysis_exports[a])
            analysis_exports.remove(analysis_exports[a])
            # update
            [f_year_pos, f_year] = find_first_year(analysis_exports)
            [f_month_pos, f_month] = find_first_month(analysis_exports, f_year_pos)
            a = f_month_pos
        while int(l_year) == int(f_year) and int(l_month) != int(f_month):
            temp_analysis_exports.append(analysis_exports[a])
            analysis_exports.remove(analysis_exports[a])
            # update
            [f_year_pos, f_year] = find_first_year(analysis_exports)
            [f_month_pos, f_month] = find_first_month(analysis_exports, f_year_pos)
            a = f_month_pos
        temp_analysis_exports.append(analysis_exports[a])
        analysis_exports.remove(analysis_exports[a])
        analysis_exports = temp_analysis_exports
    return analysis_exports


def compare_months(exports_to, categories, cats):  # compares chosen month exports/flow
    design = [[(1920, 850), (0, 0), (1850, 850), "graph", "white", 1, True, ""],  # graph
              ["", "", "Arial 14", "black", "white", (7, 2), 1, "", True, ""],  # text1
              [" ,", "", "Arial 14", "black", "white", (2, 2), 1, "", True, ""],  # text2
              [" ,", "", "Arial 14", "black", "white", (7, 2), 1, "", True, ""],  # text3
              ["button_text", "", "font", ["white", "blue"], (25, 1), 2, True, False, ""],  # buttons: 1, 2
              [" ,", "", "Arial 12", "black", "white", (20, 1), 2, "", True, ""],  # text3
              ["button_text", "", "font", ["white", "blue"], (12, 1), 1, True, False, ""],  # buttons: categories
              ["PayOff", "layout", (1920, 1080), True, "c"]]  # window]

    exports_to = sort_analysis_exports(exports_to)
    exports_to.reverse()
    colors = ["green", "blue", "red", "black", "pink", "teal", "orange", "gray", "olive", "purple", "navy",
                  "maroon", "lime", "aliceblue", "antiquewhite"]

    compared_months = []
    for i in exports_to:
        compared_months.append(i[0] + "." + i[1])

    # constant
    graph = sg.Graph(design[0][0], design[0][1], design[0][2], key=design[0][3], background_color=design[0][4], pad=design[0][5], visible=design[0][6], tooltip=design[0][7])
    row = []

    for i in compared_months:
        if not compared_months.index(i) == len(compared_months) - 1:
            row.append(sg.Text(i, key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]))
            row.append(sg.Text(" ,", key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9]))
        else:
            row.append(sg.Text(i, key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9]))
    row.append(sg.Text(":השוואת חודשים", key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9]))

    layout = [row,
             [graph],
             [sg.Button('סיכום הוצאות - היסטוגרמה', key='סיכום הוצאות - היסטוגרמה', font=design[4][2], button_color=design[4][3], size=design[4][4], pad=design[4][5], visible=design[4][6], disabled=design[4][7], tooltip=design[4][8]),
              sg.Button('התפלגות לפי חודש', key='התפלגות לפי חודש', font=design[4][2], button_color=design[4][3], size=design[4][4], pad=design[4][5], visible=design[4][6], disabled=design[4][7], tooltip=design[4][8])],
             [sg.Text(':התפלגות לפי קטגוריה', key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9])]]
    row2 = []
    row2.append(sg.Button("הכנסה", key="income", font=design[6][2], button_color=design[6][3], size=design[6][4], pad=design[6][5], visible=design[6][6], disabled=design[6][7], tooltip=design[6][8]))
    categories.reverse()
    for i in categories:
        row2.append(sg.Button(i[1], key=i[0], font=design[6][2], button_color=design[6][3], size=design[6][4], pad=design[6][5], visible=design[6][6], disabled=design[6][7], tooltip=design[6][8]))
    categories.reverse()
    layout.append(row2)

    window = sg.Window(title=design[7][0], layout=layout, size=design[7][2], modal=design[7][3], element_justification=design[7][4])

    while True:
        event, values = window.Read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'סיכום הוצאות - היסטוגרמה':
            graph.Erase()

            high_expn = 0.0
            summery = []
            for i in exports_to:
                summery.append(i[14])

            for i in summery:
                if i > high_expn:
                    high_expn = i

            if high_expn == 0:
                high_expn = 1

            x1 = []
            for i in summery:
                x1.append(i / high_expn * 750)

            spacing = round(1750 / len(exports_to))
            x = range(50, spacing * len(exports_to), spacing)

            a = 0
            for i in x:
                file = exports_to[a][0] + "." + exports_to[a][1]
                graph.DrawRectangle(top_left=(i - 15, x1[a]), bottom_right=(i + 15, 0), fill_color=colors[a])
                graph.DrawText(text="%.2f" % summery[a], location=(i, x1[a] + 20))
                graph.DrawText(text=file, location=(i, x1[a] + 40))
                a += 1

        elif event == 'התפלגות לפי חודש':
            graph.erase()

            high_expn = 0.0
            summery = []
            for i in exports_to:
                summery.append(i[14])

            for i in summery:
                if i > high_expn:
                    high_expn = i

            if high_expn == 0:
                high_expn = 1

            x1 = []
            for i in summery:
                x1.append(i / high_expn * 750)

            spacing = round(1750 / len(exports_to))
            x = range(50, spacing * len(exports_to), spacing)

            a = 0
            for i in compared_months:
                if a == len(summery) - 1:
                    graph.draw_line(point_from=(x[a], x1[a]), point_to=(x[a], x1[a]))
                    graph.draw_text(text=i, location=(x[a], x1[a] + 40))
                    graph.draw_text(text="%.2f" % summery[a], location=(x[a], x1[a] + 20))
                else:
                    graph.draw_line(point_from=(x[a], x1[a]), point_to=(x[a+1], x1[a + 1]))
                    graph.draw_text(text=i, location=(x[a], x1[a] + 40))
                    graph.draw_text(text="%.2f" % summery[a], location=(x[a], x1[a] + 20))
                    a += 1

        elif event == categories[0][0] or event == categories[1][0] or event == categories[2][0] or event == categories[3][0]\
            or event == categories[4][0] or event == categories[5][0] or event == categories[6][0] or event == categories[7][0]\
               or event == categories[8][0] or event == categories[9][0] or event == categories[10][0] or event == categories[11][0]:

            b = 0
            for i in categories:
                if event in i:
                    break
                b += 1

            graph.Erase()
            change_button_color(window, cats, event, 'red', 'blue')

            high_expn = 0.0
            summery = []
            for i in exports_to:
                summery.append(i[b + 2])

            for i in summery:
                if i > high_expn:
                    high_expn = i

            if high_expn == 0:
                high_expn = 1

            x1 = []
            for i in summery:
                x1.append(i/high_expn * 750)

            spacing = round(1750 / len(summery))
            x = range(50, spacing * len(summery), spacing)

            a = 0
            for i in x:
                graph.DrawRectangle(top_left=(i - 15, x1[a]), bottom_right=(i + 15, 0), fill_color=colors[b])
                graph.DrawText(text=categories[b][0] + ": " + str("%.2f" % summery[a]), location=(i, x1[a] + 20))
                graph.DrawText(text=exports_to[a][0] + "." + exports_to[a][1], location=(i, x1[a] + 40))
                a += 1

        elif event == "income":
            graph.Erase()
            change_button_color(window, cats, event, 'red', 'blue')

            high_expn = 0.0
            summery = []
            for i in exports_to:
                summery.append(i[2])
            for i in summery:
                if i > high_expn:
                    high_expn = i

            x1 = []
            for i in summery:
                x1.append(i/high_expn * 750)

            spacing = round(1750 / len(summery))
            x = range(50, spacing * len(summery), spacing)

            a = 0
            for i in x:
                graph.DrawRectangle(top_left=(i - 15, x1[a]), bottom_right=(i + 15, 0), fill_color=colors[12])
                graph.DrawText(text=categories[a][0] + ": " + str("%.2f" % summery[a]), location=(i, x1[a] + 20))
                graph.DrawText(text=exports_to[a][0] + "." + exports_to[a][1], location=(i, x1[a] + 40))
                a += 1
    window.Close()


def analyse_month(connection, exports_to, page, categories):  # present data analysis for chosen month export/flow
    design = [[(1900, 850), (0, 0), (1800, 800), "graph", "white", 1, True, ""], # graph
              [":ניתוח חודש", "", "Arial 14", "black", "white", (13, 2), 2, "", True, ""],  # texts 1, 2 : analysed month
              [" ,", "", "Arial 12", "black", "white", (13, 2), 1, "", False, ""],  # text 3, 4
              ["button_text", "", "Arial 12", ["white", "blue"], (25, 2), 2, True, False, ""],  # buttons: 1, 2, 3, 4
              ["PayOff", "layout", (1920, 1080), True, "c"],  # window
              ["column_layout", "column", "white", (1900, 930), 5, "c", "c", False, True, True]]  # column

    if page == "export_":
        text = "סיכום הוצאות"
    else:
        text = "תזרים"
    analyse_pars = [[], [], [], [], []]
    file = exports_to[0] + "." + exports_to[1]
    file2 = exports_to[0] + "_" + exports_to[1]

    data_for_pie = exports_to
    data_for_pie = data_for_pie[2:14]
    data_for_pie.append(exports_to[15])

    sum = 0.0
    for i in data_for_pie:
        sum += i
    if sum == 0:
        sum = 1

    month_all_expn = []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM " + page + file2)
        for i in cursor.fetchall():
            month_all_expn.append(list(i))
    except Exception as e:
        general_error('שגיאה:' + str(e))

    row = [[sg.Text("קטגוריה", key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
            sg.Text("חיוב", key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
            sg.Text("שם", key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
            sg.Text("תאריך", key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])]]

    for i in month_all_expn:
        row.append([sg.Text(i[3], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
                    sg.Text(i[2], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
                    sg.Text(i[1], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
                    sg.Text(i[0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])

    column = sg.Column(row, key=design[5][1], background_color=design[5][2], size=design[5][3], pad=design[5][4], justification=design[5][5], element_justification=design[5][6], visible=design[5][7], scrollable=design[5][8], vertical_scroll_only=design[5][9])

    colors = ["green", "blue", "red", "black", "pink", "teal", "orange", "gray", "olive", "purple", "navy",
                  "maroon", "lime", "aliceblue", "antiquewhite"]

    graph = sg.Graph(design[0][0], design[0][1], design[0][2], key=design[0][3], background_color=design[0][4], pad=design[0][5], visible=design[0][6], tooltip=design[0][7])

    layout = [[sg.Text(file, key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9]),
               sg.Text(design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])],
              [graph, column]]
    row = []
    for i in categories:
        row.append(sg.Text(i[1], key=i[0], font=design[2][2], text_color=colors[categories.index(i)], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9]))
    row.append(sg.Text('מקרא', key='map', font=design[2][2], text_color=colors[categories.index(i)], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9]))
    layout.append(row)
    layout.append([sg.Button(text + ' - לפי הוצאה', key="הוצאה", font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                   sg.Button(text + ' - לפי תאריך', key="תאריך", font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                   sg.Button(text + ' - עוגה', key="עוגה", font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),
                   sg.Button(text + ' - היסטוגרמה', key="היסטוגרמה", font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8]),])
    window = sg.Window(title=design[4][0], layout=layout, size=design[4][2], modal=design[4][3], element_justification=design[4][4])

    while True:
        event, values = window.Read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == 'היסטוגרמה':
            window['graph'].update(visible=True)
            window['column'].update(visible=False)
            graph.erase()
            for i in categories:
                window[i[0]].update(visible=False)

            high_expn = 0.0
            for i in data_for_pie:
                if i > high_expn:
                    high_expn = i

            if high_expn == 0:
                high_expn = 1

            x1 = []
            for i in data_for_pie:  # normalized values as location on the graph
                x1.append(i/high_expn * 750)

            spacing = round(1750 / 12)
            x = range(50, spacing * 12, spacing)

            a = 0
            for i in x:
                graph.DrawRectangle(top_left=(i - 15, x1[a]), bottom_right=(i + 15, 0), fill_color=colors[a])
                text = "%.2f" % data_for_pie[a]
                graph.DrawText(text=categories[a][1] + ": " + str(text), location=(i, x1[a] + 20))
                a += 1

        elif event == 'עוגה':
            window['graph'].update(visible=True)
            window['column'].update(visible=False)
            graph.erase()
            for i in categories:
                window[i[0]].update(visible=True)

            pie_start = 90
            x2 = []
            for i in data_for_pie:
                x2.append(i / sum * 360)
            a = 0
            for i in x2:
                window.finalize()
                graph.DrawArc((250, 250), (750, 750), extent=i, start_angle=pie_start, arc_color=colors[a], fill_color=colors[a], style="pieslice")
                pie_start += i
                a += 1

        elif event == 'תאריך':
            window['graph'].update(visible=True)
            window['column'].update(visible=False)
            graph.erase()
            for i in categories:
                window[i[0]].update(visible=False)
            dates = [month_all_expn[0][0]]
            charges = [month_all_expn[0][2]]
            a = 1
            b = 0
            for i in month_all_expn[1:len(month_all_expn)]:# no seperation between income and outcome
                if i[0] == month_all_expn[a - 1][0]:
                    charges[b] += i[2]
                else:
                    dates.append(i[0])
                    charges.append(i[2])
                    b += 1
                a += 1

            high_expn = 0.0
            for i in charges:
                if i > high_expn:
                    high_expn = i

            if high_expn == 0:
                high_expn = 1

            x1 = []
            for i in charges:
                x1.append(i/high_expn * 750)

            spacing = round(1750 / len(dates))
            x = range(50, spacing * len(dates), spacing)

            a = 0
            text_color = "red"
            for i in dates:
                day = i[0:len(i) - 5]
                if a == len(dates) - 1:
                    graph.draw_line(point_from=(x[a], x1[a]), point_to=(x[a], x1[a]))
                    graph.draw_text(text=day, location=(x[a], x1[a] + 40))
                    graph.draw_text(text="%.2f" % charges[a], color=text_color, location=(x[a], x1[a] + 20))
                else:
                    graph.draw_line(point_from=(x[a], x1[a]), point_to=(x[a+1], x1[a + 1]))
                    graph.draw_text(text=day, location=(x[a], x1[a] + 40))
                    graph.draw_text(text="%.2f" % charges[a], color=text_color, location=(x[a], x1[a] + 20))
                    a += 1

        elif event == 'הוצאה':
            window['graph'].update(visible=False)
            window['column'].update(visible=True)

            for i in categories:
                window[i[0]].update(visible=False)
    window.Close()


# flow functions
def sort_month_flow(connection, month_flow, new_flow):  # sort all future expenses for the month - by date
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flow_" + month_flow)
    month_all_flow = []
    for i in cursor.fetchall():
        month_all_flow.append(list(i))
    month_all_flow.append([new_flow[0] + "/" + new_flow[1] + "/" + new_flow[2], new_flow[3], new_flow[4], new_flow[5], new_flow[6]])
    temp_month_all_flow = []
    first = 31
    last = 1
    for i in month_all_flow:
        if i[0][1] == "/":
            day = int(i[0][0])
        if i[0][2] == "/":
            day = int(i[0][0:2])
        if day < first:
            first = day
        if day > last:
            last = day
    while not first == last + 1:
        for i in month_all_flow:
            if i[0][1] == "/":
                day = int(i[0][0])
            if i[0][2] == "/":
                day = int(i[0][0:2])
            if day == first:
                temp_month_all_flow.append(i)
        first += 1
    month_all_flow = temp_month_all_flow
    try:
        cursor.executescript("""

                                      DROP TABLE flow_""" + month_flow + """;
                                      CREATE TABLE flow_""" + month_flow + """(
                                          date,
                                          name,
                                          charge,
                                          category,
                                          kind
                                          );
                                  """)
        connection.commit()
    except Exception as e:
        general_error(e)

    for i in month_all_flow:
        try:
            cursor.execute("INSERT INTO flow_" + month_flow + " VALUES (?, ?, ?, ?, ?)",
                           [i[0], i[1], i[2], i[3], i[4]])
            connection.commit()
        except Exception as e:
            general_error(e)
    return month_all_flow


def delete_month_flow(connection, flow_exports_to):  # deletes chosen month flow
    cursor.execute("SELECT * FROM flow_exports")
    year_flow = cursor.fetchall()
    for i in flow_exports_to:
        cursor.executescript("""
            DROP TABLE """ + i + """.flow;
        """)
        connection.commit()
        for j in year_flow:
            if str(j[0]) + "." + str(j[1]) == i:
                year_flow.remove(j)

    for i in year_flow:
        cursor.execute("INSERT INTO flow_exports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [i[0], i[2], i[3], i[4],
                        i[5], i[6], i[7], i[8],
                        i[9], i[10], i[11], i[12],
                        i[13], i[14], i[15], i[16]])
        connection.commit()
    return year_flow


def insert_month_flow(categories, cats, analysis_keys, flow_exports, empty_flow_exports, flow_design, flow_display, window2, cur_month, cur_year, flow_exports_list, home_keys, graph1):  # inserts new future expense, up to 12 months ahead
    next_month = cur_month + 1
    next_year = cur_year
    if next_month == 13:
        next_month = 1
        next_year = cur_year + 1

    design = [["הוספה לתזרים", "", "Arial 14", "black", "white", (30, 3), 1, "c", True, ""], # text1
              ["!יש למלא את כל הפרטים ובצורה תקינה", "error1", "Arial 12", "black", "white", (40, 3), 1, "c", False, ""], # text2
              [":פרטי ההוצאה/הכנסה", "", "Arial 12", "black", "white", (20, 3), 1, "r", True, ""], # text3
              ["input_text", "input_default_text", "key", "Arial 12", "black", "white", (10, 3), 1, "c", True, False, "הכנס/י לכאן את הערכים המבוקשים"], # input
              [":יום החיוב", "", "Arial 12", "black", "white", (10, 3), 1, "c", True, ""],  # text4
              [":סכום", "", "Arial 12", "black", "white", (5, 3), 1, "c", True, ""],  # text5
              [":שם", "", "Arial 12", "black", "white", (3, 3), 1, "c", True, ""],  # text6
              [":מתאריך", "", "Arial 12", "black", "white", (20, 3), 1, "r", True, ""],  # text7
              [":שנה", "", "Arial 12", "black", "white", (4, 3), 1, "c", True, ""],  # text8
              [":חודש", "", "Arial 12", "black", "white", (5, 3), 1, "c", True, ""],  # text9
              [":עד תאריך", "", "Arial 12", "black", "white", (20, 3), 1, "r", True, ""],  # text10
              [":שנה", "", "Arial 12", "black", "white", (4, 3), 1, "c", True, ""],  # text11
              [":חודש", "", "Arial 12", "black", "white", (5, 3), 1, "c", True, ""],  # text12
              [":יום", "", "Arial 12", "black", "white", (4, 3), 1, "c", True, ""],  # text13
              [":בחר/י קטגוריה", "", "Arial 12", "black", "white", (15, 3), 1, "c", True, ""],  # text14
              ["button_text", "key", "Arial 12", ["white", "blue"], (15, 3), 1, True, False, "אנא לחצ/י לבחירת הקטגוריה המבוקשת להוצאה או להכנסה"],  # buttons: categories
              ["PayOff", "layout", (600, 900), True]]  # window

    layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
              [sg.Text(design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])],
              [sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
              [sg.Input(key='day1', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[4][0], key=design[4][1], font=design[4][2], text_color=design[4][3], background_color=design[4][4], size=design[4][5], pad=design[4][6], justification=design[4][7], visible=design[4][8], tooltip=design[4][9]),
               sg.Input(key='charge', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[5][0], key=design[5][1], font=design[5][2], text_color=design[5][3], background_color=design[5][4], size=design[5][5], pad=design[5][6], justification=design[5][7], visible=design[5][8], tooltip=design[5][9]),
               sg.Input(key='name', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[6][0], key=design[6][1], font=design[6][2], text_color=design[6][3], background_color=design[6][4], size=design[6][5], pad=design[6][6], justification=design[6][7], visible=design[6][8], tooltip=design[6][9])],
              [sg.Text(design[7][0], key=design[7][1], font=design[7][2], text_color=design[7][3], background_color=design[7][4], size=design[7][5], pad=design[7][6], justification=design[7][7], visible=design[7][8], tooltip=design[7][9])],
              [sg.Input(key='year1', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[8][0], key=design[8][1], font=design[8][2], text_color=design[8][3], background_color=design[8][4], size=design[8][5], pad=design[8][6], justification=design[8][7], visible=design[8][8], tooltip=design[8][9]),
               sg.Input(key='month1', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[9][0], key=design[9][1], font=design[9][2], text_color=design[9][3], background_color=design[9][4], size=design[9][5], pad=design[9][6], justification=design[9][7], visible=design[9][8], tooltip=design[9][9])],
              [sg.Text(design[10][0], key=design[10][1], font=design[10][2], text_color=design[10][3], background_color=design[10][4], size=design[10][5], pad=design[10][6], justification=design[10][7], visible=design[10][8], tooltip=design[10][9])],
              [sg.Input(key='year2', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[11][0], key=design[11][1], font=design[11][2], text_color=design[11][3], background_color=design[11][4], size=design[11][5], pad=design[11][6], justification=design[11][7], visible=design[11][8], tooltip=design[11][9]),
               sg.Input(key='month2', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[12][0], key=design[12][1], font=design[12][2], text_color=design[12][3], background_color=design[12][4], size=design[12][5], pad=design[12][6], justification=design[12][7], visible=design[12][8], tooltip=design[12][9]),
               sg.Input(key='day2', font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], disabled=design[3][9], tooltip=design[3][10]),
               sg.Text(design[13][0], key=design[13][1], font=design[13][2], text_color=design[13][3], background_color=design[13][4], size=design[13][5], pad=design[13][6], justification=design[13][7], visible=design[13][8], tooltip=design[13][9])],
              [sg.Text(design[14][0], key=design[14][1], font=design[14][2], text_color=design[14][3], background_color=design[14][4], size=design[14][5], pad=design[14][6], justification=design[14][7], visible=design[14][8], tooltip=design[14][9])],
              [sg.Button(categories[2][1], key=categories[2][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[1][1], key=categories[1][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[0][1], key=categories[0][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8])],
              [sg.Button(categories[5][1], key=categories[5][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[4][1], key=categories[4][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[3][1], key=categories[3][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8])],
              [sg.Button(categories[8][1], key=categories[8][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[7][1], key=categories[7][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[6][1], key=categories[6][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8])],
              [sg.Button(categories[11][1], key=categories[11][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[10][1], key=categories[10][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8]),
               sg.Button(categories[9][1], key=categories[9][0], font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8])],
              [sg.Button("הכנסה", key='income', font=design[15][2], button_color=design[15][3], size=design[15][4],pad=design[15][5], visible=design[15][6], disabled=design[15][7], tooltip=design[15][8])]]

    window = sg.Window(title=design[16][0], layout=layout, background_color=design[16][2], size=design[16][3], modal=design[16][4])
    while True:
        event, values = window.read()

        if event in (None, "יציאה") or event == sg.WINDOW_CLOSED:
            break

        # check for choice
        elif event == categories[0][0] or event == categories[1][0] or event == categories[2][0] or event == \
                categories[3][0] or event == categories[4][0] or event == categories[5][0] or event == categories[6][
            0] or event == categories[7][0] or event == categories[8][0] or event == categories[9][0] or event == \
                categories[10][0] or event == categories[11][0] or event == "income":

            # check inserted data
            if values['name'] == "" or values['charge'] == "" or values['day1'] == "":
                window['error1'].update(visible=True)
            elif values['month1'] == "" or values['year1'] == "":
                window['error1'].update(visible=True)
            elif values['month2'] == "" and not values['year2'] == "" or not values['month2'] == "" and values['year2'] == "":
                window['error1'].update(visible=True)
            elif int(values['year2']) < int(values['year1']) or int(values['month1']) > int(values['month2']) and int(
                    values['year1']) == int(values['year2']):
                window['error1'].update(visible=True)
            elif int(values['month1']) < cur_month and int(values['year1']) == cur_year or int(values['month1']) < cur_month\
                    and int(values['year1']) < cur_year or int(values['month1']) > cur_month and int(values['year1']) < cur_year:
                window['error1'].update(visible=True)
            else:
                window['error1'].update(visible=False)

                name = str(values['name'])
                charge = float(values['charge'])
                start_day = int(values['day1'])  # case1: 9, case2: 09
                start_month = int(values['month1'])
                start_year = int(values['year1'])
                end_month = int(values['month2'])
                end_year = int(values['year2'])

                # characterize the insertion
                if event == "income":
                    category = ""
                    kind = "income"
                else:
                    category = event
                    kind = "outcome"

                empty_flow_exports_list = []
                for i in empty_flow_exports:  # make a list of dates for the flow months
                    if not len(i) == 0:
                        empty_flow_exports_list.append(i[0] + "." + i[1])
                    else:
                        empty_flow_exports_list.append("")

                if end_month == "" and end_year == "":  # if the insert it for just one month ahead
                    end_month = start_month
                    end_year = start_year

                while not start_month == end_month + 1 and not start_year == end_year + 1:
                    month_flow = ["", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    month_all_flow = []
                    new_flow = [str(start_day), str(start_month), str(start_year), name, charge, category, kind]

                    if str(start_month) + "." + str(start_year) in flow_exports_list: # means the flow already exist in database
                        if kind == "income":
                            flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][15] += charge
                            window2[str(start_month) + "." + str(start_year) + ".income" + ".flow"].update(
                                value=flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][15])
                        else:
                            flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][
                                cats.index(event) + 2] += charge
                            window2[str(start_month) + "." + str(start_year) + "." + event + ".flow"].update(
                                value=flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][cats.index(event) + 2])
                        month_flow = flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))]
                        sum = 0.0
                        for i in flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][2:14]:
                            sum += i
                        flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][14] = sum
                        window2[str(start_month) + "." + str(start_year) + "." + "total" + ".flow"].update(
                            value=flow_exports[flow_exports_list.index(str(start_month) + "." + str(start_year))][14])
                    elif str(start_month) + "." + str(start_year) in empty_flow_exports_list: # means the flow does not exist in database but already inserted
                        if kind == "income":
                            empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][15] += charge
                            window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + ".income" + ".flow"].update(
                                value=empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][15])
                        else:
                            empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][cats.index(event) + 2] += charge
                            window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + "." + event + ".flow"].update(
                                value=empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][cats.index(event) + 2])
                        month_flow = empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))]
                        sum = 0.0
                        for i in empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][2:14]:
                            sum += i
                        empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][14] = sum
                        window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + "." + "total" + ".flow"].update(
                            value=empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][14])
                    else: # first insert of the month flow
                        if len(flow_exports) == 0 and len(empty_flow_exports) == 0:
                            for i in flow_display:
                                window2[flow_design[8][1] + i].update(visible=False)
                        month_flow[0] = str(start_month)
                        month_flow[1] = str(start_year)
                        month_flow[cats.index(event) + 2] += charge
                        month_flow[14] += charge
                        flow_exports.append(month_flow)
                        empty_flow_exports.append(month_flow)
                        empty_flow_exports_list.append(str(start_month) + "." + str(start_year))
                        flow_exports = sort_flow_exports(flow_exports)

                        a = 16
                        for i in analysis_keys:
                            if i == ".button":
                                window2[empty_place1[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))] + i + ".flow"].update(button_color=(f_buttons[7], f_buttons[8][0]))
                                window2[empty_place1[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))] + i + ".flow"].update(disabled=False)
                                flow_buttons.append([f_buttons[2], empty_place1[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))] + i + ".flow", buttonstate, f_buttons[7], f_buttons[8]])
                                continue
                            elif i == ".month":
                                window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + i + ".flow"].update(value=str(start_month) + "." + str(start_year))
                            else:
                                window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + i + ".flow"].update(value=empty_flow_exports[empty_flow_exports_list.index(str(start_month) + "." + str(start_year))][a])
                            window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + i + ".flow"].update(visible=True)
                            a -= 1
                        window2[str(empty_flow_exports_list.index(str(start_month) + "." + str(start_year))) + ".total" + ".flow"].update(value=charge)

                        cursor.executescript("""
                            CREATE TABLE flow_""" + str(start_month) + "_" + str(start_year) + """(
                                date,
                                name,
                                charge,
                                category,
                                kind
                                );
                        """)
                        connection.commit()

                    if start_month == next_month and start_year == next_year:# update graph1 of next month
                        window2['next'].update(value=str(start_month) + "." + str(start_year))

                        pie_start = 90
                        month_flow = month_flow[2:len(month_flow)]
                        a = 0
                        for k in home_keys:
                            window2[k + ".last"].update(value=month_flow[a])
                            window2[k + ".last"].update(visible=True)
                            a += 1
                        income = month_flow[13]
                        month_data2 = month_flow[0:12]
                        month_data2.append(income)
                        high_expn = 0
                        sum = 0
                        for i in month_data2:
                            if i > high_expn:
                                high_expn = i
                            sum += i
                        x2 = []
                        for i in month_data2:
                            x2.append(i / sum * 360)
                        a = 0
                        for i in x2:
                            window2.finalize()
                            graph1.DrawArc((0, 250), (250, 0), extent=i, start_angle=pie_start, arc_color=pie_colors[a], fill_color=pie_colors[a], style="pieslice")
                            pie_start += i
                            a += 1

                    month_all_flow = sort_month_flow(connection, str(start_month) + "_" + str(start_year), new_flow)
                    start_month += 1
                    if start_month == 13:
                        start_month = 1
                        start_year += 1

                # create new table for flow exports
                cursor.executescript("""

                                                  DROP TABLE flow_exports;
                                                  CREATE TABLE flow_exports(
                                                      month,
                                                      year,
                                                      total_food,
                                                      total_gas,
                                                      total_fun,
                                                      total_food_out,
                                                      total_flat,
                                                      total_private,
                                                      total_clothes,
                                                      total_equipment,
                                                      total_bit,
                                                      total_cash,
                                                      total_other,
                                                      total_abroad,
                                                      total,
                                                      income,
                                                      current
                                                      );
                                              """)
                connection.commit()

                # update the relevant flow month at flow page and flow exports table
                for i in flow_exports:
                    if i[0] == str(start_month) and i[1] == str(start_year):
                        window2[event + ".next"].update(value=i[cats.index(event) + 2])
                    cursor.execute(
                        "INSERT INTO flow_exports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13],
                         i[14], i[15], i[16]])
                    connection.commit()
                break

    window.close()
    return flow_exports, empty_flow_exports


def sort_flow_exports(flow_exports):  # sort months flow (future expenses) by order: soonest to latest
    temp_flow_exports = []

    [f_year_pos, f_year] = find_last_year(flow_exports)
    [f_month_pos, f_month] = find_last_month(flow_exports, f_year_pos)
    [l_year_pos, l_year] = find_first_year(flow_exports)
    [l_month_pos, l_month] = find_first_month(flow_exports, l_year_pos)

    a = f_month_pos
    while int(l_year) != int(f_year) and int(l_month) != int(f_month):
        temp_flow_exports.append(flow_exports[a])
        flow_exports.remove(flow_exports[a])
        [f_year_pos, f_year] = find_last_year(flow_exports)
        [f_month_pos, f_month] = find_last_month(flow_exports, f_year_pos)
        a = f_month_pos

    while int(l_year) == int(f_year) and int(l_month) != int(f_month):
        temp_flow_exports.append(flow_exports[a])
        flow_exports.remove(flow_exports[a])
        [f_year_pos, f_year] = find_last_year(flow_exports)
        [f_month_pos, f_month] = find_last_month(flow_exports, f_year_pos)
        a = f_month_pos

    temp_flow_exports.append(flow_exports[a])
    flow_exports.remove(flow_exports[a])
    flow_exports = temp_flow_exports

    return flow_exports


def insert_current(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year):  # insert for cur date, to current without sort
    design = [['עדכון עו"ש', "", "Arial 16", "black", "white", (30, 3), 1, "c", True, ""], # text1: page headline
              ['הכנס/י עו"ש מעודכן ליום זה או לפי תאריך', "", "Arial 14", "black", "white", (30, 3), 1, "c", True, ""],  # text2: instructions
              ["input_default_text", "key", "Arial 12", "black", "white", (10, 3), 1, "c", True, False, "הכנס/י את הערכים המבוקשים לכאן"],  # inputs
              ["text", "", "Arial 12", "black", "white", (10, 3), 1, "c", True, ""],  # text3: input texts
              ["לפי תאריך", "bydate", "Arial 12", (10, 3), 1, False, "black"],  # check box
              ["הכנס/י", "הכנס/י", "Arial 12", ["black", "blue"], (10, 3), 5, True, False, ""],  # button
              ["PayOff", "layout", (400, 600), True, "c"]]  # window

    layout = [[sg.Text(design[0][0], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
              [sg.Text(design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])],
              [sg.Input(key='value', font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], disabled=design[2][9], tooltip=design[2][10]),
               sg.Text(':עו"ש', key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9])],
              [sg.Checkbox(design[4][0], key=design[4][1], font=design[4][2], size=design[4][3], pad=design[4][4], default=design[4][5], text_color=design[4][6])],
              [sg.Input(key='year1', font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], disabled=design[2][9], tooltip=design[2][10]),
               sg.Text(':שנה', key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9])],
              [sg.Input(key='month1', font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], disabled=design[2][9], tooltip=design[2][10]),
               sg.Text(':חודש', key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9])],
              [sg.Input(key='day1', font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], disabled=design[2][9], tooltip=design[2][10]),
               sg.Text(':יום', key=design[3][1], font=design[3][2], text_color=design[3][3], background_color=design[3][4], size=design[3][5], pad=design[3][6], justification=design[3][7], visible=design[3][8], tooltip=design[3][9])],
              [sg.Button(design[5][0], key=design[5][1], font=design[5][2], button_color=design[5][3], size=design[5][4], pad=design[5][5], visible=design[5][6], disabled=design[5][7], tooltip=design[5][8])]]

    window = sg.Window(title=design[6][0], layout=layout, size=design[6][2], modal=design[6][3], element_justification=design[6][4])
    temp_current = []
    ok = 0
    while True:  # without input check
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "הכנס/י" and values['bydate'] == False and not values['value'] == "":  # current for now date
            temp_current.append([cur_day, cur_month, cur_year, float(values['value'])])
            break
        elif event == "הכנס/י" and values['bydate'] == True and not values['value'] == "" and not values['year1'] == "" and not values['month1'] == "" and not values['day1'] == "":  # current by specific date
            temp_current.append([values['day1'], values['month1'], values['year1'], float(values['value'])])
            break
        else:
            general_error("שגיאה! יש להכניס ערכים תקינים")

    if not values['value'] is None:
        for i in current:
            if i[2] > temp_current[2]:
                current.insert(current.index(i), temp_current)
            elif i[2] == temp_current[2] and i[1] > temp_current[1]:
                current.insert(current.index(i), temp_current)
            elif i[2] == temp_current[2] and i[1] == temp_current[1] and i[0] > temp_current[0]:
                current.insert(current.index(i), temp_current)
            else:
                continue
        try:
            cursor.executescript("""
                DROP TABLE current;
                CREATE TABLE current(
                    day,
                    month,
                    year,
                    current
                    );
            """)
            connection.commit()
            for i in current:
                cursor.execute("INSERT INTO current VALUES (?, ?, ?, ?)", [i[0], i[1], i[2], i[3]])
                connection.commit()
        except Exception as e:
            general_error('שגיאה:' + str(e))
        analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = calculate_all_months(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)
    window.close()
    return analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current


def calculate_all_months(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year):
    # calculates all export and flow months according to current update
    sum_month_total = 0.0
    avg_month_total = 0.0
    sum_month_income = 0.0
    avg_month_income = 0.0
    month_current = 0.0
    analysis_exports.reverse()  # to start from the oldest month
    a = 1
    for i in analysis_exports:
        sum_month_total += i[14]
        avg_month_total = sum_month_total / a
        sum_month_income += i[15]
        avg_month_income = sum_month_income / a
        if i[16] == 0:
            general_error(':מומלץ לעדכן עו"ש לחודש ' + i[0] + "." + i[1])
            analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = insert_current(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)
            for j in current:
                if j[1] == i[0] and j[2] == i[1]:
                    i[16] = j[3]
        if i[16] == 0:
            if i[14] == 0:
                i[14] = avg_month_total
            if i[15] == 0:
                i[15] = avg_month_income
            i[16] = avg_month_income - i[14]
        a += 1
    analysis_exports.reverse()  # bring back to right order - most recent to oldest month

    a = 1
    for i in flow_exports:
        sum_month_total += i[14]
        avg_month_total = sum_month_total / a
        sum_month_income += i[15]
        avg_month_income = sum_month_income / a
        if i[16] == 0:
            for j in current:
                if j[1] == i[0] and j[2] == i[1]:
                    i[16] = j[3]
        if i[16] == 0:
            if i[14] == 0:
                i[14] = avg_month_total
            if i[15] == 0:
                i[15] = avg_month_income
            i[16] = avg_month_income - i[14]
        a += 1

    return analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current


def update_all_months(month_list, empty_month_list, display_keys, analysis_exports_or_flow_exports):
    # after calculate all months, updates gui display accordingly
    if analysis_exports_or_flow_exports == "analysis_exports":  # case: export month
        page1 = ".export"
        page2 = "export_"
        end = 14
    else:  # case: flow month
        page1 = ".flow"
        page2 = "flow_"
        end = 12

    # update page display
    display_keys.reverse()
    display_keys = display_keys[1:len(display_keys) - 1]
    for i in month_list:
        key = i[0] + "." + i[1]
        i = i[2:len(i)]
        if i in empty_month_list:
            for j in display_keys:
                window[str(empty_month_list.index(i)) + j + page1].update(value=i[display_keys.index(j)])
        else:
            for j in display_keys:
                window[key + j + page1].update(value=i[display_keys.index(j)])
    display_keys.reverse()

    # update database - just month list and not all month expn
    try:
        cursor.executescript("""

                    Drop TABLE """ + analysis_exports_or_flow_exports + """;

                    CREATE TABLE """ + analysis_exports_or_flow_exports + """(
                        month,
                        year,
                        total_food,
                        total_gas,
                        total_fun,
                        total_food_out,
                        total_flat,
                        total_private,
                        total_clothes,
                        total_equipment,
                        total_bit,
                        total_cash,
                        total_other,
                        total_abroad,
                        total,
                        income,
                        current
                        );
                """)
        connection.commit()
        for i in analysis_exports:
            cursor.execute(
                "INSERT INTO analysis_exports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13],
                 i[14], i[15], i[16]])
            connection.commit()

    except Exception as e:
        general_error('שגיאה:' + str(e))


# settings functions
def delete_memory(window, exports_to, categories, empty_categories, cats, button_list):  # does not update all export and flow months that exist
    temp_button_list = []
    for i in exports_to:
        if i in cats:  # whole category was chosen
            for j in button_list: # creates new buttons list - without the names of chosen category to delete
                    if j[1] == i + ".settings" or j[1] == "settings":
                        temp_button_list.append(j)
                    elif j[1][0:j[1].index(".")] in categories[cats.index(i)][2:len(categories[cats.index(i)])]:
                        continue
                    elif j[1][0:j[1].index(".")] == i and len(empty_categories[cats.index(i)]) > 1:
                        if empty_categories[cats.index(i)][int(j[j.index(".") + 1:len(j) - 7])] in categories[cats.index(i)]:
                            continue
                    else:
                        temp_button_list.append(j)
            for j in categories[cats.index(i)][2:len(categories[cats.index(i)])]:  # make names of chosen category from categories list - Invisible
                window[j + ".button"].update(visible=False)
                window[j + ".text"].update(visible=False)
            for j in empty_categories[cats.index(i)][1:len(empty_categories[cats.index(i)])]:  # make names of chosen category from empty categories list - Invisible
                window[i + "." + str(empty_categories[cats.index(i)].index(j)) + ".button"].update(visible=False)
                window[i + "." + str(empty_categories[cats.index(i)].index(j)) + ".text"].update(visible=False)
            categories[cats.index(i)] = categories[cats.index(i)][0:2]
            empty_categories[cats.index(i)] = empty_categories[cats.index(i)][0:1]
            cats[cats.index(i)] = ""
        else: # one name from a category was chosen
            # if old name - already exists in memory
            if i in empty_categories[0] or i in empty_categories[1] or i in empty_categories[2] or i in empty_categories[3] or i in empty_categories[4] or i in empty_categories[5] or i in empty_categories[6] or i in empty_categories[7] or i in empty_categories[8] or i in empty_categories[9] or i in empty_categories[10] or i in empty_categories[11]:
                for j in empty_categories:
                    for k in j[1:len(j)]:  # look for the category of the chosen name
                        if len(k) >= int(i[i.index(".") + 1:len(i) - 7]):  # make sure category is not empty
                            if k == empty_categories[empty_categories.index(j)][int(i[i.index(".") + 1:len(i) - 7])]:  # finds the right name
                                window[j[0] + "." + str(empty_categories[empty_categories.index(j)].index(k)) + "." + ".button"].update(visible=False) # make button un visible
                                window[j[0] + "." + str(empty_categories[empty_categories.index(j)].index(k)) + "." + ".text"].update(visible=False) # make text un visible
                                for l in button_list:  # removes the name from categories list
                                        if k == empty_categories[empty_categories.index(j)][int(l[1][l[1].index(".") + 1:len(l[1]) - 7])]:
                                            button_list.remove(l)
                                j.remove(k)
                                categories[cats.index(j[0])].remove(k)
                                break
            # if new name
            else:
                for j in categories:
                    for k in j:
                        if k == i:
                            window[k + ".button"].update(visible=False)
                            window[k + ".text"].update(visible=False)
                            index1 = cats.index(j[0]) + 1
                            index2 = j.index(k) - 1
                            button_list.pop(cats.index(j[0]) + 1 * j.index(k) - 1)
                            j.remove(i)
                            break
        general_error("!שמות נמחקו בהצלחה")

        return categories, empty_categories, cats, temp_button_list


def update_memory(connection, categories):  # update categories in memory when user exit program
    cursor = connection.cursor()
    for i in categories:
        cursor.executescript("""

                        DROP TABLE """ + i[0] + """;
                        CREATE TABLE """ + i[0] + """(
                            name
                            );
                    """)
        connection.commit()
        for j in i[2:len(i)]:
            cursor.execute("INSERT INTO " + i[0] + " VALUES (?)", [j])
            connection.commit()

    cursor.executescript("""
        DROP TABLE categories;
        CREATE TABLE categories(
            key_name,
            display_name
            );
    """)
    connection.commit()
    for i in categories:
        cursor.execute("INSERT INTO categories VALUES (?, ?)", [i[0], i[1]])
        connection.commit()


def make_displays(categories, home_display, analysis_display, flow_display, settings_display):  # creates home, analysis, flow and settings displays - according to users categories
    categories.reverse()
    for i in categories:
        home_display.append(i[1])
        analysis_display.append(i[1])
        settings_display.append(i[1])
    categories.reverse()
    home_display.reverse()
    home_display.append('סה"כ הוצאות')
    home_display.append('הכנסה')
    home_display.append('יתרת עו"ש')
    analysis_display.append('חודש')
    flow_display = analysis_display
    return home_display, analysis_display, flow_display, settings_display


def change_category_name(connection, categories, empty_categories, cats, home_display, analysis_display, flow_display, settings_display, window2, exports_to):  # changes the display of a chosen category - according to users input
    design = [["שינוי שם קטגוריה", "", "Arial 14", "black", "white", (30, 3), 10, "c", True, ""], # headline,
              ["", "name", "Arial 12", "black", "white", (10, 3), 5, "c", True, False, "tooltip"], # input
              [":שם חדש", "", "Arial 12", "black", "white", (10, 3), 5, "c", True, ""], # input text
              ["הכנס", "insert", "Arial 12", ["black", "blue"], (15, 3), 10, True, False, ""],  # button
              ["PayOff", "layout", (600, 600), "visible", "c"]]  # window
    # create window of change
    pre_name = exports_to[0]
    layout = [[sg.Text(design[0][0] + ": " + categories[cats.index(pre_name)][1], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])],
              [sg.Input(default_text=design[1][0], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], disabled=design[1][9], tooltip=design[1][10]),
               sg.Text(design[2][0], key=design[2][1], font=design[2][2], text_color=design[2][3], background_color=design[2][4], size=design[2][5], pad=design[2][6], justification=design[2][7], visible=design[2][8], tooltip=design[2][9])],
              [sg.Button(design[3][0], key=design[3][1], font=design[3][2], button_color=design[3][3], size=design[3][4], pad=design[3][5], visible=design[3][6], disabled=design[3][7], tooltip=design[3][8])]]

    window = sg.Window(title=design[4][0], layout=layout, size=design[4][2], modal=design[4][3], element_justification=design[4][4])
    while True:
        event, values = window.read()

        if event in (None, "יציאה") or event == sg.WINDOW_CLOSED:
            break
        elif not values['name'] == "":
            new_name = str(values['name'])
            # update main vars of display
            for i in categories:
                if i[0] == pre_name:
                    window2[i[1] + ".next"].update(value=new_name)
                    window2[i[1] + ".last"].update(value=new_name)
                    window2[i[1] + ".analysis"].update(value=new_name)
                    window2[i[1] + ".flow"].update(value=new_name)
                    window2[i[1] + ".settings"].update(value=new_name)
                    i[1] = new_name
            home_display, analysis_display, flow_display, settings_display = make_displays(categories, home_display, analysis_display, flow_display, settings_display)
            general_error("!קטגוריה עודכנה בהצלחה")
            break
    window.close()
    return categories, home_display, analysis_display, flow_display, settings_display


def display_category(categories, cats, category):  # display names of a chosen category
    design = [["text", "key", "Arial 14", "black", "white", (30, 2), 10, "c", True, ""],  # text1: category
              ["text", "key", "Arial 12", "black", "white", (30, 2), 1, "c", True, ""],  # text2: category
              ["column_layout", "key", "white", (275, 800), 5, "c", "c", True, True, True],  # column
              ["PayOff", "layout", (1600, 900), True, "c"]]  # window

    layout = [[sg.Text("קטגוריה" + ": " + categories[cats.index(category)][1], key=design[0][1], font=design[0][2], text_color=design[0][3], background_color=design[0][4], size=design[0][5], pad=design[0][6], justification=design[0][7], visible=design[0][8], tooltip=design[0][9])]]
    a = 2
    column1 = []
    column2 = []
    column3 = []
    column4 = []
    column5 = []
    columns = [column1, column2, column3, column4, column5]
    spacing = int(len(categories[cats.index(category)][2:len(categories[cats.index(category)])]) / 5)
    for i in range(2, spacing * 5, 5): # divide all names to display in 5 columns
        column1.append([sg.Text(categories[cats.index(category)][a], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        column2.append([sg.Text(categories[cats.index(category)][a + 1], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        column3.append([sg.Text(categories[cats.index(category)][a + 2], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        column4.append([sg.Text(categories[cats.index(category)][a + 3], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        column5.append([sg.Text(categories[cats.index(category)][a + 4], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        a += 5
    for i in range(0, (len(categories[cats.index(category)]) - 2) % 5, 1): # display the modulo if there is
        columns[i].append([sg.Text(categories[cats.index(category)][a], key=design[1][1], font=design[1][2], text_color=design[1][3], background_color=design[1][4], size=design[1][5], pad=design[1][6], justification=design[1][7], visible=design[1][8], tooltip=design[1][9])])
        a += 1
    layout.append([sg.Column(column5, key=design[2][1], background_color=design[2][2], size=design[2][3], pad=design[2][4], justification=design[2][5], element_justification=design[2][6], visible=design[2][7], scrollable=design[2][8], vertical_scroll_only=design[2][9]),
                   sg.Column(column4, key=design[2][1], background_color=design[2][2], size=design[2][3], pad=design[2][4], justification=design[2][5], element_justification=design[2][6], visible=design[2][7], scrollable=design[2][8], vertical_scroll_only=design[2][9]),
                   sg.Column(column3, key=design[2][1], background_color=design[2][2], size=design[2][3], pad=design[2][4], justification=design[2][5], element_justification=design[2][6], visible=design[2][7], scrollable=design[2][8], vertical_scroll_only=design[2][9]),
                   sg.Column(column2, key=design[2][1], background_color=design[2][2], size=design[2][3], pad=design[2][4], justification=design[2][5], element_justification=design[2][6], visible=design[2][7], scrollable=design[2][8], vertical_scroll_only=design[2][9]),
                   sg.Column(column1, key=design[2][1], background_color=design[2][2], size=design[2][3], pad=design[2][4], justification=design[2][5], element_justification=design[2][6], visible=design[2][7], scrollable=design[2][8], vertical_scroll_only=design[2][9])])

    window = sg.Window(title=design[3][0], layout=layout, size=design[3][2], modal=design[3][3], element_justification=design[3][4])
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()


def make_change_details(user_name, user_password, user_address, user_remember, user_auto, cur_year, cur_month, cur_day):  # changes user log in details
    password_layout = [[sg.Text("הכנס/י סיסמא כדי להמשיך", font="Arial 14", size=(20, 3))],
                       [sg.Text("סיסמא לא נכונה! נסה/י שנית", key='error', font="Arial 12", text_color='red', size=(20, 3), visible=False)],
                       [sg.Input(key='pass', size=(20, 3)), sg.Text(":סיסמא", font="Arial 12", size=(20, 3))],
                       [sg.Button("המשך", size=(20, 3))]]
    change_layout = [[sg.Text("שינוי פרטי התחברות", font="Arial 14", size=(100, 3))],
                     [sg.Input(default_text="שם משתמש חדש", key='name', size=(20, 3)),
                      sg.Text("הכנס/י שם משתמש חדש", font="Arial 12", size=(20, 3))],
                     [sg.Input(default_text="סיסמא חדשה", key='password', size=(20, 3)),
                      sg.Text("הכנס/י סיסמא חדשה", font="Arial 12", size=(20, 3))],
                     [sg.Checkbox(":זכור אותי", key='remember', default=True, size=(20, 3)),
                      sg.Checkbox(":התחברות אוטומטית", key='auto', default=False, size=(20, 3))],
                     [sg.Button("עדכן", size=(20, 3))]]
    layout = [[sg.Column(password_layout, element_justification='c', justification='c', key='col1'),
               sg.Column(change_layout, element_justification='c', justification='c', key='col2', visible=False)]]
    window2 = sg.Window(title="PayOff", layout=layout, element_justification='c', size=(400, 400))
    while True:
        event, values = window2.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "המשך":
            if values['pass'] == user_password:
                window2['col1'].update(visible=False)
                window2['col2'].update(visible=True)
            else:
                window2['error'].update(visible=True)
        elif event == "עדכן":
            user_name = values['name']
            user_password = values['password']
            user_remember = values['remember']
            user_auto = values['auto']
            try:
                filename = 'database.db'
                connection = sqlite3.connect(filename)
                cursor = connection.cursor()
                cursor.executescript("""
                    DROP TABLE login;
                """)
                connection.commit()
                cursor.executescript("""
                    CREATE TABLE login(
                        user,
                        password,
                        address,
                        remember,
                        auto,
                        log_year,
                        log_month,
                        log_day
                    );
                """)
                connection.commit()
                cursor.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               [user_name, user_password, user_address, user_remember, user_auto, cur_year, cur_month,
                                cur_day])
                connection.commit()

                change_details_layout = [[sg.Text("!פרטי התחברות עודכנו בהצלחה", font="Arial 12", size=(30, 3))]]

                window1 = sg.Window(title="PayOff", layout=change_details_layout, element_justification='c', size=(400, 400))
                while True:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED:
                        break
                window1.close()
                window2.close()
            except:
                general_error('שגיאה! קיימת בעיה עם מס"ד הנתונים')
                window2.close()
    window2.close()
    return user_name, user_password, user_address, user_remember, user_auto, cur_year, cur_month, cur_day


# definitions

# memory vars
open_memory = []

connection = sqlite3.connect(filename)
cursor = connection.cursor()

# memory read and get stored data
for i in categories: # program categories
    cursor.execute("SELECT * FROM " + i[0]) # with no attention to names that are in more than one category
    for j in cursor.fetchall():
        i.append(j[0])

cursor.execute("SELECT * FROM open_memory")  # letters and signs for export files read and prepare
for i in cursor.fetchall():
    open_memory.append(i)

analysis_exports = []
last_month = []
analysis_exports_list = []
averages = []
cursor.execute("SELECT * FROM analysis_exports")  # all exports months summery
for i in cursor.fetchall():
    analysis_exports.append(list(i))
if not len(analysis_exports) == 0: # case: at least one export month was already opened and analysed
    last_month = analysis_exports[0] # define last export file that was analysed - to display at main page
    for i in analysis_exports: # make a list of all the export months
        analysis_exports_list.append(i[0] + "." + i[1])
    averages = make_averages(analysis_exports)
else: # case: no export month was opened and analysed yet
    first_run = 1
    mon_num = 0

flow_exports = []
next_month = []
flow_exports_list = []
cursor.execute("SELECT * FROM flow_exports")  # all flow months summery
for i in cursor.fetchall():
    flow_exports.append(list(i))
    flow_exports_list.append(i[0] + "." + i[1])
if not len(flow_exports) == 0: # sort the order of the flow months and define the flow for current month
    flow_exports = sort_flow_exports(flow_exports)
    next_month = flow_exports[0]

exports_to = []  # list of chosen export months/flow months/categories/names from category
empty_analysis_exports = []  # for the empty slots that are to be filled in analysis
empty_analysis_exports_place = 0

empty_flow_exports = []  # for the empty slots that are to be filled in flow
empty_flow_exports_place = 0

cursor.execute("SELECT * FROM current")  # all current updates for keeping the calculations and predictions accurate
current = cursor.fetchall()
month_current = 0.0
if not len(current) == 0:
    for i in current:
        if i[1] == cur_month and i[2] == cur_year:
            month_current = current[len(current) - 1][3]
    if month_current == 0.0:
        general_error('היי ' + user_name + ', לפי נתוני המערכת מומלץ לעדכן את העו"ש שלך')
        analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = insert_current(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)  # without sort
else:
    general_error('היי ' + user_name + ', לפי נתוני המערכת מומלץ לעדכן את העו"ש שלך')
    analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = insert_current(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)  # without sort

# all vars

active_categories = ['אוכל וקניות', 'הוצאות רכב', 'בילויים', 'אוכל בחוץ', 'ביגוד והנעלה', 'ציוד ואביזרים', 'משיכות מזומן', 'העברות ביט',
                     'חשבונות בית', 'חשבונות פרטיים', 'חו"ל וטיולים', 'אחר']  # categories display - hebrew

cats = ['food', 'gas', 'fun', 'food_out', 'flat', 'private', 'clothes', 'equipment', 'bit', 'cash', 'abroad', 'other']  # categories keys - english

pie_colors = ["green", "blue", "red", "black", "pink", "teal", "orange", "gray", "olive", "purple", "navy",
              "maroon", "lime", "aliceblue", "antiquewhite"]  # colors for the categories in pie display
pie_start = 90

home_display = []  # home page elements

home_keys = ['food', 'gas', 'fun', 'food_out', 'flat', 'private', 'clothes', 'equipment', 'bit', 'cash', 'abroad', 'other', 'total', 'income', 'current']  # keys of home page elements

home_design = [[title, "title", "Arial 18", "black", "white", (100, 2), 2, "c", True, ""],
               ["הגדרות", "הגדרות", "Arial 14", ["black", "blue"], (10, 2), 15, True, False, "לחץ להצגת הקטגוריות שלך ופעולות נוספות"],
               ["תזרים", "תזרים", "Arial 14", ["black", "blue"], (10, 2), 15, True, False, "לחץ להצגת התזרים השנתי שלך מהיום והלאה"],
               ["נתונים", "נתונים", "Arial 14", ["black", "blue"], (10, 2), 15, True, False, "לחץ להצגת כלל חודשי החיוב שנותחו עד כה"],
               ["בית", "בית", "Arial 14", ["black", "blue"], (10, 2), 15, True, False, "לחץ לחזרה לדף הבית"],
               ["דף הבית", "home_title", "Arial 16", "black", "white", (15, 2), 10, "c", True, ""],
               ["הוצאות לחודש הבא:", "next", "Arial 14", "black", "white", (50, 2), 5, "r", True, ""],
               ["הוצאות לחודש אחרון:", "last", "Arial 14", "black", "white", (50, 2), 5, "r", True, ""],
               ["", "", "Arial 12", "black", "white", (12, 1), 1, "c", True, ""],# categories headline
               ["0.0", "", "Arial 12", "black", "white", (12, 1), 1, "c", True, ""],# categories data
               [(300, 300), (0, 0), (300, 300), "graph1", "white", 30, True, ""],
               [(300, 300), (0, 0), (300, 300), "graph2", "white", 30, True, ""],
               ["column layout", "column key", "white", (1900, 1000), 0, "c", "c", True, True, True],# columns
               ["PayOff", "layout", (1920, 1080), True, "c"],# window
               [":כמה הוצאתי עד עכשיו", "", "Arial 14", "black", "white", (19, 2), 10, "c", True, ""],# averages title
               ["", "", "Arial 12", "", "white", (10, 1), 1, "c", True, ""],# average titles
               ["", "", "Arial 12", "black", "white", (10, 1), 1, "c", True, ""],
               [(1920, 1), (0, 300), (1920, 301), "graph3", "black", 10, True, ""]]  # average data

analysis_display = ['הכל', 'יתרת עו"ש', 'הכנסה', 'סה"כ הוצאות']  # analysis page elements

analysis_keys = ['.button', '.current', '.income', '.total', '.other', '.abroad', '.cash', '.bit', '.equipment', '.clothes', '.private', '.flat', '.food_out', '.fun', '.gas', '.food', '.month']  # keys of analysis page elements

analysis_design = [["סיכום חודשי חיוב", "home_title", "Arial 16", "black", "white", (15, 2), 10, "c", True, ""],
                   ["מחיקה", "מחיקה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ למחיקת חודש חיוב או מספר חודשים יחד"],
                   ["השוואה", "השוואה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ להשוואת ההוצאות בין שני חודשים או יותר"],
                   ["ניתוח", "ניתוח", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ לקבלת ניתוח הוצאות של חודש נבחר"],
                   ["חודש חדש", "חודש חדש", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ לפתיחת חודש חיוב חדש ומיון ההוצאות"],
                   ["בחר/י", "", "Arial 12", ["black", "blue"], (5, 2), 1, "c", True, ""],
                   ["", "", "Arial 12", "black", "white", (12, 2), 1, "c", True, ""], # categories headline
                   ["", "", "Arial 10", "black", "white", (13, 2), 1, "c", True, ""], # months data for categories
                   ["לא קיים מידע זמין", "a_no_data", "Arial 10", "black", "white", (17, 2), 1, "c", True, ""],# no data
                   ["column layout", "column key", "white", (1920, 600), 5, "c", "c", True, True, True],# column
                  ]# design  for analysis page

a_buttons = [["הכל", "בטל/י"], "analysis", ["בחר/י", "בטל/י"], "Arial 12", (5, 1), 3, True, "black", ["blue", "red"]]  # features of analysis page buttons

flow_display = ['הכל', 'יתרת עו"ש', 'הכנסה', 'סה"כ הוצאות', 'אחר', 'חו"ל וטיולים', 'משיכות מזומן', 'העברות ביט',
                    'ציוד ואביזרים', 'ביגוד והנעלה', 'חשבונות פרטיים', 'חשבונות בית', 'אוכל בחוץ', 'בילויים', 'הוצאות רכב',
                    'אוכל וקניות', 'חודש']  # flow page elements

flow_keys = ['.button', '.current', '.income', '.total', '.other', '.abroad', '.cash', '.bit', '.equipment', '.clothes', '.private', '.flat', '.food_out', '.fun', '.gas', '.food', '.month']  # keys of flow page elements

flow_design = [["תזרים שנתי", "home_title", "Arial 16", "black", "white", (15, 2), 10, "c", True, ""],
                   ["מחיקה", "מחיקה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ למחיקת תזרים לחודש אחד או יותר"],
                   ["השוואה", "השוואה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ להשוואת הוצאות עתידיות בין שני חודשים"],
                   ["צפייה", "צפייה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ לקבלת ניתוח הוצאות של חודש עתידי נבחר"],
                   ["הכנסה", "הכנסה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ להכנסת הוצאה/הכנסה עתידיים לחודש אחד או יותר"],
                   ["בחר/י", "", "Arial 12", ["black", "blue"], (5, 2), 1, "c", True, ""],
                   ["", "", "Arial 12", "black", "white", (12, 2), 1, "c", True, ""], # the categories headline
                   ["", "", "Arial 10", "black", "white", (13, 2), 1, "c", True, ""], # flow data for categories
                   ["לא קיים מידע זמין", "a_no_data", "Arial 10", "black", "white", (14, 2), 1, "c", True, ""], # no data
                   ["column layout", "column key", "white", (1920, 600), 5, "c", "c", True, True, True],# column
                ]  # design  for flow page


f_buttons = [["הכל", "בטל/י"], "flow", ["בחר/י", "בטל/י"], "Arial 12", (5, 1), 5, True, "black", ["blue", "red"]]  # features of flow page buttons

settings_display = []  # design  for settings page

settings_keys = ['.button', '.current', '.income', '.total', '.other', '.abroad', '.cash', '.bit', '.equipment', '.clothes', '.private', '.flat', '.food_out', '.fun', '.gas', '.food', '.month']  # keys of page elements

settings_design = [["הקטגוריות שלי", "home_title", "Arial 16", "black", "white", (15, 2), 10, "c", True, ""],
                   ["מחיקה", "מחיקה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ למחיקת שם בית עסק/קטגוריה אחת או יותר"],
                   ["שינוי שם", "שינוי שם", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ לשינוי שם קטגוריה נבחרת"],
                   ["צפייה", "צפייה", "Arial 14", ["black", "blue"], (8, 2), 10, True, False, "לחץ לצפייה בשמות בתי העסק בקטגוריה נבחרת"],
                   ["הכל", "settings", "Arial 12", ["black", "blue"], (4, 2), 2, True, False, "לחץ לבחירת כל הקטגוריות"],
                   ["בחר/י", "", "Arial 12", ["black", "blue"], (5, 2), 5, True, False, "לחץ לבחירת כל הקטגוריה"],
                   ["", "", "Arial 12", "black", "white", (13, 1), 1, "r", True, ""], # category name
                   [":שם בית עסק", "", "Arial 12", "black", "white", (13, 1), 1, "r", True, ""], # category headline
                   ["", "", "Arial 10", "black", "white", (15, 1), 1, "r", True, ""], # names of category
                   ["לא קיים מידע זמין", "", "Arial 10", "black", "white", (15, 1), 1, "r", True, ""], # no data
                   ["column_layout", "", "white", (275, 300), 10, "c", "c", True, True, True],]  # columns

s_buttons = [["הכל", "בטל/י"], "settings", ["בחר/י", "בטל/י"], "Arial 12", (5, 1), 5, True, "black", ["blue", "red"]]  # features of analysis page buttons

empty_categories = [['food'], ['gas'], ['fun'], ['food_out'], ['flat'], ['private'], ['clothes'], ['equipment'], ['bit'], ['cash'], ['abroad'], ['other']]  # for the empty places of categories

home_display, analysis_display, flow_display, settings_display = make_displays(categories, home_display, analysis_display, flow_display, settings_display)

analysis_buttons = []  # analysis page buttons list
flow_buttons = []  # flow page buttons list
settings_buttons = []  # settings page buttons list

statecolor = ['blue', 'red']  # buttons background colors
buttonstate = 0  # buttons initial state (not chosen)
btc = 'white'  # buttons text colour

error_keys = ["a_error1", "a_error2", "a_error3", "f_error1", "f_error2", "f_error3", "s_error1"]  # keys of all pages errors

month_expenses = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # expenses summery by category for an opened export month
month_all_expn = []  # list of all expenses dates names charges and category for an opened export month
average_months_expn = 0.0  # average expn of all months by now

# empty widgets for the pages
x1 = range(0, 50, 1)
empty_place1 = []
for i in x1:  # for export months and flow months
    empty_place1.append(str(i))
x2 = range(1, 101, 1)
empty_place2 = []
for i in x2:  # for categories names
    empty_place2.append(str(i))

# analysis page
analysis_layout = [[sg.Text(home_design[0][0], key=home_design[0][1], font=home_design[0][2], text_color=home_design[0][3], background_color=home_design[0][4], size=home_design[0][5], pad=home_design[0][6], justification=home_design[0][7], visible=home_design[0][8], tooltip=home_design[0][9])],
                   [sg.Button(home_design[1][0], key=home_design[1][1], font=home_design[1][2], button_color=home_design[1][3], size=home_design[1][4], pad=home_design[1][5], visible=home_design[1][6], disabled=home_design[1][7], tooltip=home_design[1][8]),
                    sg.Button(home_design[2][0], key=home_design[2][1], font=home_design[2][2], button_color=home_design[2][3], size=home_design[2][4], pad=home_design[2][5], visible=home_design[2][6], disabled=home_design[2][7], tooltip=home_design[2][8]),
                    sg.Button(home_design[3][0], key=home_design[3][1], font=home_design[3][2], button_color=home_design[3][3], size=home_design[3][4], pad=home_design[3][5], visible=home_design[3][6], disabled=home_design[3][7], tooltip=home_design[3][8]),
                    sg.Button(home_design[4][0], key=home_design[4][1], font=home_design[4][2], button_color=home_design[4][3], size=home_design[4][4], pad=home_design[4][5], visible=home_design[4][6], disabled=home_design[4][7], tooltip=home_design[4][8])],

                   [sg.Graph(home_design[17][0], home_design[10][1], home_design[10][2], key=home_design[17][3], background_color=home_design[17][4], pad=home_design[17][5], visible=home_design[17][6], tooltip=home_design[17][7])],

                   [sg.Text(analysis_design[0][0], key=analysis_design[0][1], font=analysis_design[0][2], text_color=analysis_design[0][3], background_color=analysis_design[0][4], size=analysis_design[0][5], pad=analysis_design[0][6], justification=analysis_design[0][7], visible=analysis_design[0][8], tooltip=analysis_design[0][9])],
                   [sg.Button(analysis_design[1][0], key=analysis_design[1][1], font=analysis_design[1][2], button_color=analysis_design[1][3], size=analysis_design[1][4], pad=analysis_design[1][5], visible=analysis_design[1][6], disabled=analysis_design[1][7], tooltip=analysis_design[1][8]),
                    sg.Button(analysis_design[2][0], key=analysis_design[2][1], font=analysis_design[2][2], button_color=analysis_design[2][3], size=analysis_design[2][4], pad=analysis_design[2][5], visible=analysis_design[2][6], disabled=analysis_design[2][7], tooltip=analysis_design[2][8]),
                    sg.Button(analysis_design[3][0], key=analysis_design[3][1], font=analysis_design[3][2], button_color=analysis_design[3][3], size=analysis_design[3][4], pad=analysis_design[3][5], visible=analysis_design[3][6], disabled=analysis_design[3][7], tooltip=analysis_design[3][8]),
                    sg.Input(key='-IN-', visible=False, enable_events=True),
                    sg.FilesBrowse(analysis_design[4][0], key=analysis_design[4][1], font=analysis_design[4][2], button_color=analysis_design[4][3], size=analysis_design[4][4], pad=analysis_design[4][5], visible=analysis_design[4][6], disabled=analysis_design[4][7], tooltip=analysis_design[4][8],
                     file_types=(('xlsx', '*.**'), ('xls', '*.**')), initial_folder="C:/Users/97250/Desktop/managment", target='-IN-')]]
row = []
for i in analysis_display:
    if i == "הכל":
        row.append(sg.Button(a_buttons[0][0], key=a_buttons[1], font=a_buttons[3], size=a_buttons[4], pad=a_buttons[5], visible=a_buttons[6], button_color=(a_buttons[7], a_buttons[8][0])))
        analysis_buttons.append([a_buttons[0], a_buttons[1], buttonstate, a_buttons[7], a_buttons[8]])
    else:
       row.append(sg.Text(i, key=i + ".analysis", font=analysis_design[6][2], text_color=analysis_design[6][3], background_color=analysis_design[6][4], size=analysis_design[6][5], pad=analysis_design[6][6], justification=analysis_design[6][7], visible=analysis_design[6][8], tooltip=analysis_design[6][9]))
analysis_layout.append(row)
column = []
if not len(analysis_exports) == 0:
    for i in analysis_exports:
        if not len(i) == 0:
            a = 0
            row = []
            i.reverse()
            key = str(i[16]) + "." + str(i[15])
            row.append(sg.Button(a_buttons[2][0], key=key + analysis_keys[0] + ".export", font=a_buttons[3], size=a_buttons[4], pad=a_buttons[5], visible=a_buttons[6], button_color=(a_buttons[7], a_buttons[8][0])))
            analysis_buttons.append([a_buttons[2], key + analysis_keys[0] + ".export", buttonstate, a_buttons[7], a_buttons[8]])
            for j in i[0:len(i) - 2]:
                row.append(sg.Text(j, key=key + analysis_keys[a + 1] + ".export", font=analysis_design[7][2], text_color=analysis_design[7][3], background_color=analysis_design[7][4], size=analysis_design[7][5], pad=analysis_design[7][6], justification=analysis_design[7][7], visible=analysis_design[7][8], tooltip=analysis_design[7][9]))
                a += 1
            row.append(sg.Text(key, key=key + analysis_keys[a + 1] + ".export", font=analysis_design[7][2], text_color=analysis_design[7][3], background_color=analysis_design[7][4], size=analysis_design[7][5], pad=analysis_design[7][6], justification=analysis_design[7][7], visible=analysis_design[7][8], tooltip=analysis_design[7][9]))
            column.append(row)
            i.reverse()
else:
    row = []
    for i in analysis_display:
        row.append(sg.Text(analysis_design[8][0], key=analysis_design[8][1] + i, font=analysis_design[8][2], text_color=analysis_design[8][3], background_color=analysis_design[8][4], size=analysis_design[8][5], pad=analysis_design[8][6], justification=analysis_design[8][7], visible=analysis_design[8][8], tooltip=analysis_design[8][9]))
    analysis_layout.append(row)
for i in empty_place1:
    row = []
    row.append(sg.Button(a_buttons[2][0], key=i + ".button" + ".export", font=a_buttons[3], size=a_buttons[4], pad=a_buttons[5], visible=True, button_color=(a_buttons[7], '#64778d'), disabled=True))
    for j in analysis_keys[1:len(analysis_keys)]:
        row.append(sg.Text("", key=i + j + ".export", font=analysis_design[7][2], text_color=analysis_design[7][3], background_color=analysis_design[7][4], size=analysis_design[7][5], pad=analysis_design[7][6], justification=analysis_design[7][7], visible=False, tooltip=analysis_design[7][9]))
    column.append(row)
analysis_layout.append([sg.Column(column, justification='c', vertical_scroll_only=True, scrollable=True, size=(1900, 600), pad=5)])

# flow page
flow_layout = [[sg.Text(home_design[0][0], key=home_design[0][1], font=home_design[0][2], text_color=home_design[0][3], background_color=home_design[0][4], size=home_design[0][5], pad=home_design[0][6], justification=home_design[0][7], visible=home_design[0][8], tooltip=home_design[0][9])],
                   [sg.Button(home_design[1][0], key=home_design[1][1], font=home_design[1][2], button_color=home_design[1][3], size=home_design[1][4], pad=home_design[1][5], visible=home_design[1][6], disabled=home_design[1][7], tooltip=home_design[1][8]),
                    sg.Button(home_design[2][0], key=home_design[2][1], font=home_design[2][2], button_color=home_design[2][3], size=home_design[2][4], pad=home_design[2][5], visible=home_design[2][6], disabled=home_design[2][7], tooltip=home_design[2][8]),
                    sg.Button(home_design[3][0], key=home_design[3][1], font=home_design[3][2], button_color=home_design[3][3], size=home_design[3][4], pad=home_design[3][5], visible=home_design[3][6], disabled=home_design[3][7], tooltip=home_design[3][8]),
                    sg.Button(home_design[4][0], key=home_design[4][1], font=home_design[4][2], button_color=home_design[4][3], size=home_design[4][4], pad=home_design[4][5], visible=home_design[4][6], disabled=home_design[4][7], tooltip=home_design[4][8])],

               [sg.Graph(home_design[17][0], home_design[10][1], home_design[10][2], key=home_design[17][3], background_color=home_design[17][4], pad=home_design[17][5], visible=home_design[17][6], tooltip=home_design[17][7])],

               [sg.Text(flow_design[0][0], key=flow_design[0][1], font=flow_design[0][2], text_color=flow_design[0][3], background_color=flow_design[0][4], size=flow_design[0][5], pad=flow_design[0][6], justification=flow_design[0][7], visible=flow_design[0][8], tooltip=flow_design[0][9])],
               [sg.Button(flow_design[1][0], key=flow_design[1][1], font=flow_design[1][2], button_color=flow_design[1][3], size=flow_design[1][4], pad=flow_design[1][5], visible=flow_design[1][6], disabled=flow_design[1][7], tooltip=flow_design[1][8]),
                sg.Button(flow_design[2][0], key=flow_design[2][1], font=flow_design[2][2], button_color=flow_design[2][3], size=flow_design[2][4], pad=flow_design[2][5], visible=flow_design[2][6], disabled=flow_design[2][7], tooltip=flow_design[2][8]),
                sg.Button(flow_design[3][0], key=flow_design[3][1], font=flow_design[3][2], button_color=flow_design[3][3], size=flow_design[3][4], pad=flow_design[3][5], visible=flow_design[3][6], disabled=flow_design[3][7], tooltip=flow_design[3][8]),
                sg.Button(flow_design[4][0], key=flow_design[4][1], font=flow_design[4][2], button_color=flow_design[4][3], size=flow_design[4][4], pad=flow_design[4][5], visible=flow_design[4][6], disabled=flow_design[4][7], tooltip=flow_design[4][8])]]
row = []
for i in flow_display:
    if i == "הכל":
        row.append(sg.Button(f_buttons[0][0], key=f_buttons[1], font=f_buttons[3], size=f_buttons[4], pad=f_buttons[5], visible=f_buttons[6], button_color=(f_buttons[7], f_buttons[8][0])))
        flow_buttons.append([f_buttons[0], f_buttons[1], buttonstate, f_buttons[7], f_buttons[8]])
    else:
       row.append(sg.Text(i, key=i + ".flow", font=flow_design[6][2], text_color=flow_design[6][3], background_color=flow_design[6][4], size=flow_design[6][5], pad=flow_design[6][6], justification=flow_design[6][7], visible=flow_design[6][8], tooltip=flow_design[6][9]))
flow_layout.append(row)
column = []
if not len(flow_exports) == 0 and not len(flow_exports[0]) == 0:
    column = []
    for i in flow_exports:
        if not len(i) == 0:
            a = 0
            row = []
            i.reverse()
            key = str(i[16]) + "." + str(i[15])
            row.append(sg.Button(f_buttons[2][0], key=key + flow_keys[0] + ".flow", font=f_buttons[3], size=f_buttons[4], pad=f_buttons[5], visible=f_buttons[6], button_color=(f_buttons[7], f_buttons[8][0])))
            flow_buttons.append([f_buttons[2], key + flow_keys[0] + ".flow", buttonstate, f_buttons[7], f_buttons[8]])
            for j in i[0:len(i) - 2]:
                row.append(sg.Text(j, key=key + flow_keys[a + 1] + ".flow", font=flow_design[7][2], text_color=flow_design[7][3], background_color=flow_design[7][4], size=flow_design[7][5], pad=flow_design[7][6], justification=flow_design[7][7], visible=flow_design[7][8], tooltip=flow_design[7][9]))
                a += 1
            row.append(sg.Text(key, key=key + flow_keys[a + 1] + ".export", font=flow_design[7][2], text_color=flow_design[7][3], background_color=flow_design[7][4], size=flow_design[7][5], pad=flow_design[7][6], justification=flow_design[7][7], visible=flow_design[7][8], tooltip=flow_design[7][9]))
            column.append(row)
            i.reverse()
else:
    row = []
    for i in flow_display:
        row.append(sg.Text(flow_design[8][0], key=flow_design[8][1] + i, font=flow_design[8][2], text_color=flow_design[8][3], background_color=flow_design[8][4], size=flow_design[8][5], pad=flow_design[8][6], justification=flow_design[8][7], visible=flow_design[8][8], tooltip=flow_design[8][9]))
    flow_layout.append(row)
for i in empty_place1:
    row = []
    row.append(sg.Button(a_buttons[2][0], key=i + ".button" + ".flow", font=a_buttons[3], size=a_buttons[4], pad=a_buttons[5], visible=True, button_color=(f_buttons[7], '#64778d'), disabled=True))
    for j in flow_keys[1:len(flow_keys)]:
        row.append(sg.Text("", key=i + j + ".flow", font=analysis_design[7][2], text_color=analysis_design[7][3], background_color=analysis_design[7][4], size=analysis_design[7][5], pad=analysis_design[7][6], justification=analysis_design[7][7], visible=False, tooltip=analysis_design[7][9]))
    column.append(row)
flow_layout.append([sg.Column(column, justification='c', vertical_scroll_only=True, scrollable=True, size=(1900, 400), pad=5)])

# settings page
a = 0
b = 0
for i in categories:
        column = []
        # adds the category name and button
        column.append([sg.Button(s_buttons[2][0], key=i[0] + ".settings", font=s_buttons[3], size=s_buttons[4], pad=s_buttons[5], visible=s_buttons[6], button_color=(s_buttons[7], s_buttons[8][0])),
                       sg.Text(i[1], key=i[1] + ".settings", font=settings_design[6][2], text_color=settings_design[6][3], background_color=settings_design[6][4], size=settings_design[6][5], pad=settings_design[6][6], justification=settings_design[6][7], visible=settings_design[6][8], tooltip=settings_design[6][9])])
        # adds the headline - שם בית עסק:
        column.append([sg.Text(settings_design[7][0], key=settings_design[7][1], font=settings_design[7][2], text_color=settings_design[7][3], background_color=settings_design[7][4], size=settings_design[7][5], pad=settings_design[7][6], justification=settings_design[7][7], visible=settings_design[7][8], tooltip=settings_design[7][9])])
        settings_buttons.append([s_buttons[2], i[0] + ".settings", buttonstate, s_buttons[7], s_buttons[8]])
        if len(i) > 2:
            j = i[2:len(i)]
            for k in j:
                column.append([sg.Button(s_buttons[2][0], key=k + ".button", font=s_buttons[3], size=s_buttons[4], pad=s_buttons[5], visible=s_buttons[6], button_color=(s_buttons[7], s_buttons[8][0])),
                               sg.Text(k, key=k + ".text", font=settings_design[8][2], text_color=settings_design[8][3], background_color=settings_design[8][4], size=settings_design[8][5], pad=settings_design[8][6], justification=settings_design[8][7], visible=settings_design[8][8], tooltip=settings_design[8][9])])
                settings_buttons.append([s_buttons[2], k + ".button", buttonstate, s_buttons[7], s_buttons[8]])
        else:
            column.append([sg.Text(settings_design[9][0], key=settings_design[9][1], font=settings_design[9][2], text_color=settings_design[9][3], background_color=settings_design[9][4], size=settings_design[9][5], pad=settings_design[9][6], justification=settings_design[9][7], visible=settings_design[9][8], tooltip=settings_design[9][9])])

        for j in empty_place2:
            column.append([sg.Button(s_buttons[2][0], key=empty_categories[b][0] + "." + j + ".button", font=s_buttons[3], size=s_buttons[4], pad=s_buttons[5], visible=True, button_color=('#64778d', '#64778d'), disabled=True),
                           sg.Text("", key=empty_categories[b][0] + "." + j + ".text", font=settings_design[8][2], text_color=settings_design[8][3], background_color=settings_design[8][4], size=settings_design[8][5], pad=settings_design[8][6], justification=settings_design[8][7], visible=False, tooltip=settings_design[8][9])])
            settings_buttons.append([s_buttons[2], empty_categories[b][0] + "." + j + ".button", buttonstate, s_buttons[7], s_buttons[8]])

        if i[0] == 'food':
            column0 = column
            a += 1
        elif i[0] == 'gas':
            column1 = column
            a += 1
        elif i[0] == 'fun':
            column2 = column
            a += 1
        elif i[0] == 'food_out':
            column3 = column
            a += 1
        elif i[0] == 'flat':
            column4 = column
            a += 1
        elif i[0] == 'private':
            column5 = column
            a += 1
        elif i[0] == 'clothes':
            column6 = column
            a += 1
        elif i[0] == 'equipment':
            column7 = column
            a += 1
        elif i[0] == 'bit':
            column8 = column
            a += 1
        elif i[0] == 'cash':
            column9 = column
            a += 1
        elif i[0] == 'abroad':
            column10 = column
            a += 1
        else:
            column11 = column
            a += 1
        b += 1
settings_layout = [[sg.Text(home_design[0][0], key=home_design[0][1], font=home_design[0][2], text_color=home_design[0][3], background_color=home_design[0][4], size=home_design[0][5], pad=home_design[0][6], justification=home_design[0][7], visible=home_design[0][8], tooltip=home_design[0][9])],
                   [sg.Button(home_design[1][0], key=home_design[1][1], font=home_design[1][2], button_color=home_design[1][3], size=home_design[1][4], pad=home_design[1][5], visible=home_design[1][6], disabled=home_design[1][7], tooltip=home_design[1][8]),
                    sg.Button(home_design[2][0], key=home_design[2][1], font=home_design[2][2], button_color=home_design[2][3], size=home_design[2][4], pad=home_design[2][5], visible=home_design[2][6], disabled=home_design[2][7], tooltip=home_design[2][8]),
                    sg.Button(home_design[3][0], key=home_design[3][1], font=home_design[3][2], button_color=home_design[3][3], size=home_design[3][4], pad=home_design[3][5], visible=home_design[3][6], disabled=home_design[3][7], tooltip=home_design[3][8]),
                    sg.Button(home_design[4][0], key=home_design[4][1], font=home_design[4][2], button_color=home_design[4][3], size=home_design[4][4], pad=home_design[4][5], visible=home_design[4][6], disabled=home_design[4][7], tooltip=home_design[4][8])],

                   [sg.Graph(home_design[17][0], home_design[10][1], home_design[10][2], key=home_design[17][3], background_color=home_design[17][4], pad=home_design[17][5], visible=home_design[17][6], tooltip=home_design[17][7])],

                   [sg.Text(settings_design[0][0], key=settings_design[0][1], font=settings_design[0][2], text_color=settings_design[0][3], background_color=settings_design[0][4], size=settings_design[0][5], pad=settings_design[0][6], justification=settings_design[0][7], visible=settings_design[0][8], tooltip=settings_design[0][9])],
                   [sg.Button(settings_design[1][0], key=settings_design[1][1], font=settings_design[1][2], button_color=settings_design[1][3], size=settings_design[1][4], pad=settings_design[1][5], visible=settings_design[1][6], disabled=settings_design[1][7], tooltip=settings_design[1][8]),
                    sg.Button(settings_design[2][0], key=settings_design[2][1], font=settings_design[2][2], button_color=settings_design[2][3], size=settings_design[2][4], pad=settings_design[2][5], visible=settings_design[2][6], disabled=settings_design[2][7], tooltip=settings_design[2][8]),
                    sg.Button(settings_design[3][0], key=settings_design[3][1], font=settings_design[3][2], button_color=settings_design[3][3], size=settings_design[3][4], pad=settings_design[3][5], visible=settings_design[3][6], disabled=settings_design[3][7], tooltip=settings_design[3][8])],
                    [sg.Button(settings_design[4][0], key=settings_design[4][1], font=settings_design[4][2], button_color=settings_design[4][3], size=settings_design[4][4], pad=settings_design[4][5], visible=settings_design[4][6], disabled=settings_design[4][7], tooltip=settings_design[4][8])],

                   [sg.Column(column5, key=settings_design[10][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column4, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column3, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column2, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column1, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column0, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9])],
                   [sg.Column(column11, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column10, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column9, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column8, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column7, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9]),
                    sg.Column(column6, key=settings_design[8][1], background_color=settings_design[10][2], size=settings_design[10][3], pad=settings_design[10][4], justification=settings_design[10][5], element_justification=settings_design[10][6], visible=settings_design[10][7], scrollable=settings_design[10][8], vertical_scroll_only=settings_design[10][9])]]
settings_buttons.append([s_buttons[0], s_buttons[1], buttonstate, s_buttons[7], s_buttons[8]])

# main page
main_layout = [[sg.Text(home_design[0][0], key=home_design[0][1], font=home_design[0][2], text_color=home_design[0][3], background_color=home_design[0][4], size=home_design[0][5], pad=home_design[0][6], justification=home_design[0][7], visible=home_design[0][8], tooltip=home_design[0][9])],
                   [sg.Button(home_design[1][0], key=home_design[1][1], font=home_design[1][2], button_color=home_design[1][3], size=home_design[1][4], pad=home_design[1][5], visible=home_design[1][6], disabled=home_design[1][7], tooltip=home_design[1][8]),
                    sg.Button(home_design[2][0], key=home_design[2][1], font=home_design[2][2], button_color=home_design[2][3], size=home_design[2][4], pad=home_design[2][5], visible=home_design[2][6], disabled=home_design[2][7], tooltip=home_design[2][8]),
                    sg.Button(home_design[3][0], key=home_design[3][1], font=home_design[3][2], button_color=home_design[3][3], size=home_design[3][4], pad=home_design[3][5], visible=home_design[3][6], disabled=home_design[3][7], tooltip=home_design[3][8]),
                    sg.Button(home_design[4][0], key=home_design[4][1], font=home_design[4][2], button_color=home_design[4][3], size=home_design[4][4], pad=home_design[4][5], visible=home_design[4][6], disabled=home_design[4][7], tooltip=home_design[4][8])],
               [sg.Graph(home_design[17][0], home_design[10][1], home_design[10][2], key=home_design[17][3], background_color=home_design[17][4], pad=home_design[17][5], visible=home_design[17][6], tooltip=home_design[17][7])],
               [sg.Text(home_design[5][0], key=home_design[5][1], font=home_design[5][2], text_color=home_design[5][3], background_color=home_design[5][4], size=home_design[5][5], pad=home_design[5][6], justification=home_design[5][7], visible=home_design[5][8], tooltip=home_design[5][9])]]
if not len(next_month) == 0 and not len(last_month) == 0:
    home_design[6][0] = home_design[6][0] + " " + next_month[0] + "." + next_month[1]
    home_design[7][0] = home_design[7][0] + " " + last_month[0] + "." + last_month[1]
elif len(next_month) == 0 and not len(last_month) == 0:
    home_design[6][0] = home_design[6][0] + " " + "לא קיים מידע זמין"
    home_design[7][0] = home_design[7][0] + " " + last_month[0] + "." + last_month[1]
elif not len(next_month) == 0 and len(last_month) == 0:
    home_design[6][0] = home_design[6][0] + " " + next_month[0] + "." + next_month[1]
    home_design[7][0] = home_design[7][0] + " " + "לא קיים מידע זמין"
else:
    home_design[6][0] = home_design[6][0] + "לא קיים מידע זמין"
    home_design[7][0] = home_design[7][0] + "לא קיים מידע זמין"
main_layout.append([sg.Text(home_design[7][0], key=home_design[7][1], font=home_design[7][2], text_color=home_design[7][3], background_color=home_design[7][4], size=home_design[7][5], pad=home_design[7][6], justification=home_design[7][7], visible=home_design[7][8], tooltip=home_design[7][9]),
                    sg.Text(home_design[6][0], key=home_design[6][1], font=home_design[6][2], text_color=home_design[6][3], background_color=home_design[6][4], size=home_design[6][5], pad=home_design[6][6], justification=home_design[6][7], visible=home_design[6][8], tooltip=home_design[6][9])])
layout1 = [[]]
layout2 = [[]]
layout3 = [[]]
layout4 = [[]]
layout5 = [[]]
layout6 = [[]]
next_month = next_month[2: len(next_month)]
last_month = last_month[2: len(last_month)]
x = range(0, 15, 3)
for i in x:
    if not len(next_month) == 0:
        text1 = float(next_month[i])
        text2 = float(next_month[i + 1])
        text3 = float(next_month[i + 2])
    else:
        text1 = text2 = text3 = home_design[9][0]

    layout1.append([sg.Text(home_display[i], key=home_display[i] + ".next", font=home_design[8][2], text_color=pie_colors[i], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout1.append([sg.Text(text1, key=home_keys[i] + ".next", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])
    layout2.append([sg.Text(home_display[i + 1], key=home_display[i + 1] + ".next", font=home_design[8][2], text_color=pie_colors[i + 1], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout2.append([sg.Text(text2, key=home_keys[i + 1] + ".next", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])
    layout3.append([sg.Text(home_display[i + 2], key=home_display[i + 2] + ".next", font=home_design[8][2], text_color=pie_colors[i + 2], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout3.append([sg.Text(text3, key=home_keys[i + 2] + ".next", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])

    if not len(last_month) == 0:
        text1 = float(last_month[i])
        text2 = float(last_month[i + 1])
        text3 = float(last_month[i + 2])
    else:
        text1 = text2 = text3 = home_design[9][0]

    layout4.append([sg.Text(home_display[i], key=home_display[i] + ".last", font=home_design[8][2], text_color=pie_colors[i], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout4.append([sg.Text(text1, key=home_keys[i] + ".last", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])
    layout5.append([sg.Text(home_display[i + 1], key=home_display[i + 1] + ".last", font=home_design[8][2], text_color=pie_colors[i + 1], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout5.append([sg.Text(text2, key=home_keys[i + 1] + ".last", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])
    layout6.append([sg.Text(home_display[i + 2], key=home_display[i + 2] + ".last", font=home_design[8][2], text_color=pie_colors[i + 2], background_color=home_design[8][4], size=home_design[8][5], pad=home_design[8][6], justification=home_design[8][7], visible=home_design[8][8], tooltip=home_design[8][9])])
    layout6.append([sg.Text(text3, key=home_keys[i + 2] + ".last", font=home_design[9][2], text_color=home_design[9][3], background_color=home_design[9][4], size=home_design[9][5], pad=home_design[9][6], justification=home_design[9][7], visible=home_design[9][8], tooltip=home_design[9][9])])
graph1 = sg.Graph(home_design[10][0], home_design[10][1], home_design[10][2], key=home_design[10][3], background_color=home_design[10][4], pad=home_design[10][5], visible=home_design[10][6], tooltip=home_design[10][7])
graph2 = sg.Graph(home_design[11][0], home_design[11][1], home_design[11][2], key=home_design[11][3], background_color=home_design[11][4], pad=home_design[11][5], visible=home_design[11][6], tooltip=home_design[11][7])
layout7 = [graph2, sg.Column(layout6), sg.Column(layout5), sg.Column(layout4), graph1, sg.Column(layout3), sg.Column(layout2), sg.Column(layout1)]
main_layout.append(layout7)

# averages
main_layout.append([sg.Text(home_design[14][0], key=home_design[14][1], font=home_design[14][2], text_color=home_design[14][3], background_color=home_design[14][4], size=home_design[14][5], pad=home_design[14][6], justification=home_design[14][7], visible=home_design[14][8], tooltip=home_design[14][9])])
column = []
for i in analysis_display[1:len(analysis_display) - 1]:  # titles
    column.append(sg.Text(i, key=home_design[15][1], font=home_design[15][2], text_color=pie_colors[analysis_display.index(i) - 1], background_color=home_design[15][4], size=home_design[15][5], pad=home_design[15][6], justification=home_design[15][7], visible=home_design[15][8], tooltip=home_design[15][9]))
column.append(sg.Text("", key=home_design[15][1], font=home_design[15][2], text_color=pie_colors[analysis_display.index(i) - 1], background_color=home_design[15][4], size=home_design[15][5], pad=home_design[15][6], justification=home_design[15][7], visible=home_design[15][8], tooltip=home_design[15][9]))
main_layout.append(column)
column = []
averages.reverse()
for i in averages:  # per month
    column.append(sg.Text("%.2f" % i, key=home_design[16][1], font=home_design[16][2], text_color=home_design[16][3], background_color=home_design[16][4], size=home_design[16][5], pad=home_design[16][6], justification=home_design[16][7], visible=home_design[16][8], tooltip=home_design[16][9]))
column.append(sg.Text("לחודש", key=home_design[15][1], font=home_design[15][2], text_color="black", background_color=home_design[15][4], size=home_design[15][5], pad=home_design[15][6], justification=home_design[15][7], visible=home_design[15][8], tooltip=home_design[15][9]))
main_layout.append(column)
column = []
for i in averages:  # per week
    i = i / 4.3
    column.append(sg.Text("%.2f" % i, key=home_design[16][1], font=home_design[16][2], text_color=home_design[16][3], background_color=home_design[16][4], size=home_design[16][5], pad=home_design[16][6], justification=home_design[16][7], visible=home_design[16][8], tooltip=home_design[16][9]))
column.append(sg.Text("לשבוע", key=home_design[15][1], font=home_design[15][2], text_color="black", background_color=home_design[15][4], size=home_design[15][5], pad=home_design[15][6], justification=home_design[15][7], visible=home_design[15][8], tooltip=home_design[15][9]))
main_layout.append(column)

layout = [[sg.Column(main_layout, key='main_page', size=home_design[12][3], pad=home_design[12][4], justification=home_design[12][5], element_justification=home_design[12][6], visible=home_design[12][7], scrollable=home_design[12][8], vertical_scroll_only=home_design[12][9]),
           sg.Column(analysis_layout, key='analysis_page', size=home_design[12][3], pad=home_design[12][4], justification=home_design[12][5], element_justification=home_design[12][6], visible=False, scrollable=home_design[12][8], vertical_scroll_only=home_design[12][9]),
           sg.Column(flow_layout, key='flow_page', size=home_design[12][3], pad=home_design[12][4], justification=home_design[12][5], element_justification=home_design[12][6], visible=False, scrollable=home_design[12][8], vertical_scroll_only=home_design[12][9]),
           sg.Column(settings_layout, key='settings_page', size=home_design[12][3], pad=home_design[12][4], justification=home_design[12][5], element_justification=home_design[12][6], visible=False, scrollable=home_design[12][8], vertical_scroll_only=home_design[12][9])]]
window = sg.Window(title=home_design[13][0], layout=layout, size=home_design[13][2], modal=home_design[13][3], element_justification=home_design[13][4])

# create pie charts of next and last month export, at main page
if len(next_month) != 0:
    income = next_month[13]
    month_data1 = next_month[0:12]
    month_data1.append(income)
    high_expn = 0
    sum = 0
    for i in month_data1:
        if i > high_expn:
            high_expn = i
        sum += i
    if sum == 0:
        sum = 1
    x2 = []
    for i in month_data1:
        x2.append(i / sum * 360)
    if not high_expn == 0 and high_expn == sum:
        window.finalize()
        graph1.DrawArc((0, 250), (250, 0), extent=pie_start + 269, start_angle=pie_start, arc_color=pie_colors[month_data1.index(sum)], fill_color=pie_colors[month_data1.index(sum)], style="pieslice")
    else:
        a = 0
        for i in x2:
            window.finalize()
            graph1.DrawArc((0, 250), (250, 0), extent=i, start_angle=pie_start, arc_color=pie_colors[a],
                           fill_color=pie_colors[a], style="pieslice")
            pie_start += i
            a += 1

if len(last_month) != 0:
    income = last_month[13]
    month_data2 = last_month[0:12]
    month_data2.append(income)
    high_expn = 0
    sum = 0
    for i in month_data2:
        if i > high_expn:
            high_expn = i
        sum += i
    if sum == 0:
        sum = 1
    x2 = []
    for i in month_data2:
        x2.append(i / sum * 360)
    if not high_expn == 0 and high_expn == sum:
        window.finalize()
        graph2.DrawArc((0, 250), (250, 0), extent=pie_start + 269, start_angle=pie_start, arc_color=pie_colors[month_data2.index(sum)], fill_color=pie_colors[month_data2.index(sum)], style="pieslice")
    else:
        a = 0
        for i in x2:
            window.finalize()
            graph2.DrawArc((0, 250), (250, 0), extent=i, start_angle=pie_start, arc_color=pie_colors[a],
                           fill_color=pie_colors[a], style="pieslice")
            pie_start += i
            a += 1

exports_to = []  # list of chosen export months/flow months/categories/names from category
empty_analysis_exports = []  # for the empty slots that are to be filled in analysis
empty_analysis_exports_place = 0

empty_flow_exports = []  # for the empty slots that are to be filled in flow
empty_flow_exports_place = 0

# main
while True:
    event, values = window.read()

    if event in (None, "יציאה") or event == sg.WINDOW_CLOSED:
        break
    elif event == "-IN-":# פורמט של ישרכרט בלבד
        # file name preparation - get export month name and prepare name for opening
        file = values['-IN-']
        file2 = file[::-1]
        a = 0
        for i in file2:
            if i == '/':
                break
            a += 1
        file = file[len(file) - a:len(file)] # makes file name from "Export" to ".xls", type string
        files = 1
        [error, year, month, mon] = check_file_name(file, cur_month, cur_year)

        if error == 1:
            continue
        # move on
        month_expenses[0] = month
        month_expenses[1] = year
        answer = ""

        if not len(analysis_exports) == 0:
            answer, report_exist = check_report(month, year, analysis_exports)
            if answer == "No":
                continue

        # open file
        data_error = 0
        try:
            data = pd.read_excel(file)
            abroad = data['Unnamed: 0']
            total_abroad_charge = data['Unnamed: 3']
            dates = data['Unnamed: 0']
            dates_abroad = data['Unnamed: 0']
            names_abroad = data['Unnamed: 2']
            charges_abroad = data['Unnamed: 5']
            names = data['Unnamed: 1']
            charges = data['Unnamed: 4']
            total_expense = 0.0
        except Exception as e:
            general_error(":שגיאה" + str(e))
            continue
        sort_complete = 0
        if files == 0:
            break

        # arrange file data
        abroad = abroad[5:abroad.size]
        dates = dates[5:dates.size]
        dates_abroad = dates_abroad[5:names_abroad.size]
        names = names[5:names.size]
        names_abroad = names_abroad[5:names_abroad.size]
        total_abroad_charge = total_abroad_charge[5:total_abroad_charge.size]
        charges = charges[5:charges.size]
        charges_abroad = charges_abroad[5:charges_abroad.size]

        l = 0
        abroad_expn = 0
        for i in abroad:
            if i in open_memory:
                abroad_expn = 1
                break
            l += 1

        if abroad_expn == 1:

            dates = dates[0:l - 1]
            names = names[0:l - 1]
            charges = charges[0:l - 1]
            abroad = abroad[l + 2:abroad.size]
            names_abroad = names_abroad[l + 2:names_abroad.size]
            total_abroad_charge = total_abroad_charge[l + 2:total_abroad_charge.size]
            charges_abroad = charges_abroad[l + 2:charges_abroad.size]

            k = 0
            for i in names_abroad:
                if i in open_memory:
                    break
                k += 1

            abroad = abroad[0:k]
            names_abroad = names_abroad[0:k]
            total_abroad_charge = total_abroad_charge[0:k + 1]
            charges_abroad = charges_abroad[0:k]
            total_expense += total_abroad_charge.iloc[k]
            month_expenses[14] = month_expenses[14] + total_expense

            for i in names_abroad:
                j = pd.Series(i)
                names = names.append(j)

            for i in charges_abroad:
                j = pd.Series(i)
                charges = charges.append(j)

            for i in abroad:
                j = pd.Series(i)
                dates = dates.append(j)

        else:
            l = 0
            for i in abroad:
                if not type(i) == str:
                    if math.isnan(i) and not names.iloc[l - 1] in categories[9]:
                        if names.iloc[l] == 'סך חיוב בש"ח:' or names.iloc[l] == 'סך חיוב בש' + chr(733) + 'ח:':
                            break
                        if math.isnan(names.iloc[l]):
                            l -= 1
                            break
                l += 1

            month_expenses[14] = month_expenses[14] + charges.iloc[l]
            total_expense += charges.iloc[l]
            dates = dates[0:l]
            names = names[0:l]
            charges = charges[0:l]

        new_dates = pd.Series(dtype=object)
        new_names = pd.Series(dtype=object)
        new_charges = pd.Series(dtype=object)
        skip_cash = ['סך חיוב בש"ח:', 'סך חיוב בש' + chr(733) + 'ח:']
        a = 0
        for i in names:
            if not type(i) == str or not type(charges.iloc[a]) == int or not type(charges.iloc[a]) == float or not type(dates.iloc[a]) == str: # make sure data from file is ok
                data_error = 1
                break
            if i in skip_cash:
                continue
            else:
                d = pd.Series(dates.iloc[a])
                n = pd.Series(i)
                c = pd.Series(charges.iloc[a])
                new_abroad = new_dates.append(d)
                new_names = new_names.append(n)
                new_charges = new_charges.append(c)
            a += 1

        if data_error == 1:
            general_error("!שגיאה קיימת בעיה עם נתוני הקובץ")
            continue

        abroad = new_dates
        names = new_names
        charges = new_charges

        # sorting loop - names and charges sort
        a = 0
        for i in names:
            sort = 0
            if i in open_memory:
                a += 1
                continue
            b = 2
            for j in categories: # check if charge name is in categories
                if i in j:
                    month_expenses[b] = month_expenses[b] + charges.iloc[a]
                    month_all_expn.append([dates.iloc[a], i, charges.iloc[a], j[1]])
                    sort = 1
                    if j == 'cash':
                        month_expenses[14] = month_expenses[14] + charges.iloc[a]
                    break
                b += 1

            if sort == 0: # if not in categories
                choice3 = sorting_layout(i, categories, empty_categories, cats, dates, names, charges)
                if choice3 == 0:
                    break
                if choice3 == 13:
                    a += 1
                    continue
                b = 0
                for j in categories:
                    if b + 1 == choice3: # finds the chosen category from user choice and update text and button for this name in the category
                        if len(j) == 2:
                            window[j[0] + "." + settings_design[9][1]].update(visible=False)
                        month_expenses[b + 2] = month_expenses[b + 2] + charges.iloc[a]
                        month_all_expn.append([dates.iloc[a], i, charges.iloc[a], j[0]])
                        window[empty_categories[b][0] + "." + str(len(empty_categories[b])) + ".text"].update(value=i)
                        window[empty_categories[b][0] + "." + str(len(empty_categories[b])) + ".text"].update(visible=True)
                        window[empty_categories[b][0] + "." + str(len(empty_categories[b])) + ".button"].update(button_color=(s_buttons[7], s_buttons[8][0]))
                        window[empty_categories[b][0] + "." + str(len(empty_categories[b])) + ".button"].update(disabled=False)
                        j.append(i)
                        empty_categories[b].append(i)
                        if j == 'cash':
                            month_expenses[14] = month_expenses[14] + charges.iloc[a]
                        try:
                            cursor.execute("INSERT INTO " + j[0] + " VALUES (?)", [i]) # with no attention to doubles currently - between more than one category
                            connection.commit()
                        except:
                            general_error('שגיאה! קיימת בעיה עם מס"ד הנתונים')
                        break
                    b += 1
            a += 1

        if a == len(names): # make sure all charges were sorted
            sort_complete = 1

            # results

            # total expense
            total_expn = 0.0
            for i in month_expenses:
                if i == month_expenses[14]:
                    break
                elif type(i) == str:
                    continue
                else:
                    total_expn += float(i)
            if not total_expense == total_expn:
                general_error("שגיאה בניתוח! שים לב לסיכום ההוצאות")

            for i in month_expenses[2:len(month_expenses)]:
                month_expenses[month_expenses.index(i)] = float("%.2f" % month_expenses[month_expenses.index(i)])

            last_month = month_expenses
            empty_analysis_exports.append(last_month)
            analysis_exports.append(month_expenses)
            key = str(last_month[0]) + "." + str(last_month[1])

            # make un-visible - no data display at analysis page
            if first_run == 1:
                for i in analysis_display:
                    window[analysis_design[8][1] + i].update(visible=False)
                first_run = 0

            # display month at analysis page
            window['last'].update(value=str(month_expenses[0]) + "." + str(month_expenses[1]))
            month_expenses.reverse()
            c = 0
            for i in analysis_keys:
                if i == ".button":
                    window[empty_place1[empty_analysis_exports_place] + i + ".export"].update(button_color=(a_buttons[7], a_buttons[8][0]))
                    window[empty_place1[empty_analysis_exports_place] + i + ".export"].update(disabled=False)
                    analysis_buttons.append([a_buttons[2], empty_place1[empty_analysis_exports_place] + i + ".export", buttonstate, a_buttons[7], a_buttons[8]])
                    continue
                elif c == 15:
                    window[empty_place1[empty_analysis_exports_place] + i + ".export"].update(value=key)
                else:
                    window[empty_place1[empty_analysis_exports_place] + i + ".export"].update(value=str(month_expenses[c]))
                window[empty_place1[empty_analysis_exports_place] + i + ".export"].update(visible=True)
                c += 1

            # update graph 2 - last export month
            month_expenses.reverse()
            last_month = last_month[2:len(last_month)]
            a = 0
            for k in home_keys:
                window[k + ".last"].update(value=last_month[a])
                window[k + ".last"].update(visible=True)
                a += 1
            income = last_month[13]
            month_data2 = last_month[0:12]
            month_data2.append(income)
            high_expn = 0
            sum = 0
            for i in month_data2:
                if i > high_expn:
                    high_expn = i
                sum += i
            x2 = []
            for i in month_data2:
                x2.append(i / sum * 360)
            if not high_expn == 0 and high_expn == sum:
                window.finalize()
                graph2.DrawArc((0, 250), (250, 0), extent=pie_start + 269, start_angle=pie_start,
                               arc_color=pie_colors[month_data2.index(sum)],
                               fill_color=pie_colors[month_data2.index(sum)], style="pieslice")
            else:
                a = 0
                for i in x2:
                    window.finalize()
                    graph2.DrawArc((0, 250), (250, 0), extent=i, start_angle=pie_start, arc_color=pie_colors[a],
                                   fill_color=pie_colors[a], style="pieslice")
                    pie_start += i
                    a += 1

            # update or create this month export database
            if answer == "Yes": # if this export has already been opened in the past, data will be replaced
                analysis_exports[analysis_exports.index(month_expenses)] = month_expenses

                try:
                    cursor.executescript("""
                                Drop TABLE export_""" + month + "_" + year + """;

                                CREATE TABLE export_""" + month + "_" + year + """(
                                    date,
                                    name,
                                    category,
                                    charge
                                    );
                            """)
                    connection.commit()
                    for i in month_all_expn:
                        cursor.execute("INSERT INTO export_" + month + "_" + year + " VALUES (?, ?, ?, ?)",
                                       [i[0], i[1], i[2], i[3]])
                        connection.commit()
                except Exception as e:
                    general_error('שגיאה:' + str(e))

            else:
                analysis_exports.append(month_expenses)
                analysis_exports_list.append(file)

                try:
                    cursor.executescript("""
                                    CREATE TABLE export_""" + month + "_" + year + """(
                                        date,
                                        name,
                                        category,
                                        charge
                                        );
                                """)
                    connection.commit()
                    for i in month_all_expn:
                        cursor.execute("INSERT INTO export_" + month + "_" + year + " VALUES (?, ?, ?, ?)",
                                       [i[0], i[1], i[2], i[3]])
                        connection.commit()
                except Exception as e:
                    general_error('שגיאה:' + str(e))

            # sort data and update all months export database
            if bool(analysis_exports): # if there are already exports
                analysis_exports = sort_analysis_exports(analysis_exports)

                try:
                    cursor.executescript("""
                                Drop TABLE analysis_exports;
                                
                                CREATE TABLE analysis_exports(
                                    month,
                                    year,
                                    total_food,
                                    total_gas,
                                    total_fun,
                                    total_food_out,
                                    total_flat_bills,
                                    total_private_bills,
                                    total_clothes,
                                    total_equipment,
                                    total_bit,
                                    total_cash,
                                    total_other,
                                    total_abroad,
                                    total,
                                    income,
                                    current
                                    );
                            """)
                    connection.commit()
                    for i in analysis_exports:
                        cursor.execute(
                            "INSERT INTO analysis_exports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13],
                             i[14], i[15], i[16]])
                        connection.commit()

                except Exception as e:
                    general_error('שגיאה:' + str(e))

                # update all months current and expenses
                analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = calculate_all_months(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)
                update_all_months(analysis_exports, empty_analysis_exports, analysis_keys, "analysis_exports")

            else: # if there are not already exports
                try:
                    cursor.executescript("""
                                CREATE TABLE analysis_exports(
                                    month,
                                    year,
                                    total_food,
                                    total_gas,
                                    total_fun,
                                    total_food_out,
                                    total_flat_bills,
                                    total_private_bills,
                                    total_clothes,
                                    total_equipment,
                                    total_bit,
                                    total_cash,
                                    total_other,
                                    total_abroad,
                                    total,
                                    income,
                                    current
                                    );
                            """)
                    connection.commit()

                    cursor.execute("INSERT INTO analysis_exports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   [month_expenses[0], month_expenses[1],  month_expenses[2], month_expenses[3], month_expenses[4],
                                    month_expenses[5], month_expenses[6], month_expenses[7], month_expenses[8],
                                    month_expenses[9], month_expenses[10], month_expenses[11], month_expenses[12],
                                    month_expenses[13], month_expenses[14], month_expenses[15], month_expenses[16]])
                    connection.commit()
                except Exception as e:
                    general_error('שגיאה:' + str(e))

            empty_analysis_exports_place += 1

        else:
            general_error("אנחנו רואים שהפסקת את המיון! לידיעתך סיווג הקטגוריות עד העצירה נשמר")

        month_expenses = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # menu options

    # analysis options
    elif event == home_design[3][1] or event == "נתונים58" or event == "נתונים67":
        exports_to = []
        window['main_page'].update(visible=False)
        window['analysis_page'].update(visible=True)
        window['flow_page'].update(visible=False)
        window['settings_page'].update(visible=False)
    elif event == analysis_design[1][1]:  # מחיקה
        if len(analysis_exports) == 0 and len(empty_analysis_exports) == 0:
            general_error("!סיכום ההוצאות ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
            general_error("!לא התבצעה בחירה")
        else:
            analysis_exports, empty_analysis_exports, exports_to, analysis_buttons = delete_month(window, connection, exports_to, analysis_exports, empty_analysis_exports, analysis_keys, "analysis_exports", analysis_buttons)
            reset_button(window, analysis_buttons, a_buttons)
    elif event == analysis_design[2][1]:  # השוואת חודשים
        if len(analysis_exports) == 0 and len(empty_analysis_exports) == 0:
            general_error("!סיכום ההוצאות ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 12:
            general_error("!ניתן לבחור עד 12 חודשים")
        elif len(exports_to) == 1:
            general_error("!יש לבחור לפחות שני חודשים")
        else:
            compare_months(exports_to, categories, cats)
            reset_button(window, analysis_buttons, a_buttons)
            exports_to = []
    elif event == analysis_design[3][1]:  # ניתוח חודש
        if len(analysis_exports) == 0 and len(empty_analysis_exports) == 0:
            general_error("!סיכום ההוצאות ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 1:
            general_error("!ניתן לבחור חודש אחד בלבד")
        else:
            analyse_month(connection, exports_to[0], "export_", categories)
            analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = calculate_all_months(
                connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current,
                cur_day, cur_month, cur_year)
            update_all_months(flow_exports, empty_flow_exports, flow_keys, "analysis_exports")
            reset_button(window, analysis_buttons, a_buttons)
            exports_to = []

    # flow options
    elif event == home_design[2][1] or event == "תזרים50" or event == "תזרים66":
        exports_to = []
        window['main_page'].update(visible=False)
        window['analysis_page'].update(visible=False)
        window['flow_page'].update(visible=True)
        window['settings_page'].update(visible=False)
    elif event == flow_design[1][1]:  # מחיקה
        if len(flow_exports) == 0 and len(empty_flow_exports) == 0:
            general_error("!התזרים ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        else:
            flow_exports, empty_flow_exports, exports_to, flow_buttons = delete_month(window, connection, exports_to, flow_exports, empty_flow_exports, flow_keys, "flow_exports", flow_buttons)
            reset_button(window, flow_buttons, f_buttons)
    elif event == flow_design[2][1]:  # השוואה
        if len(flow_exports) == 0 and len(empty_flow_exports) == 0:
            general_error("!סיכום ההוצאות ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 12:
            general_error("!ניתן לבחור עד 12 חודשים")
        elif len(exports_to) == 1:
            general_error("!יש לבחור לפחות שני חודשים")
        else:
            compare_months(exports_to, categories, cats)
            reset_button(window, flow_buttons, f_buttons)
            exports_to = []
    elif event == flow_design[3][1]:  # צפייה
        if len(flow_exports) == 0 and len(empty_flow_exports) == 0:
            general_error("!סיכום ההוצאות ריק כרגע")
        elif len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 1:
            general_error("!ניתן לבחור חודש אחד בלבד")
        else:
            analyse_month(connection, exports_to[0], "flow_", categories)
            reset_button(window, flow_buttons, f_buttons)
            exports_to = []
    elif event == flow_design[4][1]:  #הכנסה לתזרים
        if len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        else:
            flow_exports, empty_flow_exports = insert_month_flow(categories, cats, analysis_keys, flow_exports, empty_flow_exports, flow_design, flow_display, window, cur_month, cur_year, flow_exports_list, home_keys, graph1)
            analysis_exports, flow_exports, empty_analysis_exports, empty_flow_exports, current = calculate_all_months(connection, analysis_exports, empty_analysis_exports, flow_exports, empty_flow_exports, current, cur_day, cur_month, cur_year)
            update_all_months(flow_exports, empty_flow_exports, flow_keys, "flow_exports")

    # settings options
    elif event == home_design[1][1] or event == "הגדרות56" or event == "הגדרות34":
        categories_to = []
        window['main_page'].update(visible=False)
        window['analysis_page'].update(visible=False)
        window['flow_page'].update(visible=False)
        window['settings_page'].update(visible=True)
    elif event == settings_design[1][1] or event == "מחיקה71":  # מחיקה
        if len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        else:
            categories, empty_categories, cats, settings_buttons = delete_memory(window, exports_to, categories, empty_categories, cats, settings_buttons)
            reset_button(window, settings_buttons, s_buttons)
        exports_to = []
    elif event == settings_design[2][1]:  # שינוי
        if len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 1:
            general_error("!ניתן לבחור קטגוריה אחת")
        elif exports_to[0] in cats:
            reset_button(window, settings_buttons, s_buttons)
            categories, home_display, analysis_display, flow_display, settings_display = change_category_name(connection, categories, empty_categories, cats, home_display, analysis_display, flow_display, settings_display, window, exports_to)
            reset_button(window, settings_buttons, s_buttons)
        else:
            general_error("!יש לבחור שם קטגוריה ולא שם בית עסק")
        exports_to = []
    elif event == settings_design[3][1] or event == "צפייה72":  # צפייה
        if len(exports_to) == 0:
            general_error("!לא התבצעה בחירה")
        elif len(exports_to) > 1:
            general_error("!ניתן לבחור קטגוריה אחד")
        elif exports_to[0] in cats:
            reset_button(window, settings_buttons, s_buttons)
            display_category(categories, cats, exports_to[0])
            reset_button(window, settings_buttons, s_buttons)
        else:
            general_error("!יש לבחור שם קטגוריה ולא שם בית עסק")
        exports_to = []

    # home page
    elif event == home_design[4][1] or event == "בית52" or event == "בית59" or event == "בית68":
        window['main_page'].update(visible=True)
        window['analysis_page'].update(visible=False)
        window['flow_page'].update(visible=False)
        window['settings_page'].update(visible=False)

    # choosing options
    elif event == "analysis":  # all export months
        if not len(analysis_exports) == 0:
            exports_to = update_buttons(window, analysis_exports, empty_analysis_exports, analysis_buttons, event, exports_to, cats)
        else:
            general_error("לא קיימים חודשי חיוב כרגע")
    elif event[len(event) - 7:len(event)] == ".export":  # one export month
        exports_to = update_buttons(window, analysis_exports, empty_analysis_exports, analysis_buttons, event, exports_to, cats)

    elif event == "flow":  # all flow months
        if not len(flow_exports) == 0:
            exports_to = update_buttons(window, flow_exports, empty_flow_exports, flow_buttons, event, exports_to, cats)
        else:
            general_error("לא קיים תזרים כרגע")
    elif event[len(event) - 5:len(event)] == ".flow":  # one flow month
        exports_to = update_buttons(window, flow_exports, empty_flow_exports, flow_buttons, event, exports_to, cats)

    elif event == "settings":  # all categories
        if len(categories[0]) == 2 and len(categories[1]) == 2 and len(categories[2]) == 2 and len(categories[3]) == 2 and len(categories[4]) == 2 and len(categories[5]) == 2 and len(categories[6]) == 2 and len(categories[7]) == 2 and len(categories[8]) == 2 and len(categories[9]) == 2 and len(categories[10]) == 2 and len(categories[11]) == 2:
            general_error("לא קיים מידע בקטגוריות")
        else:
            exports_to = update_buttons(window, categories, empty_categories, settings_buttons, event, exports_to, cats)
    elif len(event) > 9 and event[0:len(event) - 9] in cats:  # one category
        for i in categories:
            if i[0] == event[0:len(event) - 9]:
                if len(i) == 2:
                    general_error("לא קיים מידע בקטגוריה זו")
                else:
                    exports_to = update_buttons(window, categories, empty_categories, settings_buttons, event, exports_to, cats)

    elif event in categories[0] or event in categories[1] or event in categories[2] or event in categories[3] or event\
            in categories[4] or event in categories[5] or event in categories[6] or event in categories[7] or event in\
            categories[8] or event in categories[9] or event in categories[10] or event in categories[11] or\
            event[len(event) - 6:len(event)] == "button": # name from a category
        exports_to = update_buttons(window, categories, empty_categories, settings_buttons, event, exports_to, cats)
window.close()
update_memory(connection, categories)
connection.close()


