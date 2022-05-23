import sqlite3
from cv2 import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import random
import sys
import os

os.system("mkdir -p ~/.cache/book-manage-real")
username = os.getlogin()
try:
    conn = sqlite3.connect("/home/"+username+'/.config/book-manage-real/maindb.db')
    cur = conn.cursor()
except:
    print("seems like you launch this program for the first time!")
    print("Creating a empty database")
    os.system("mkdir -p ~/.config/book-manage-real/")
    os.system("wget https://github.com/seabass6969/book_manage/raw/master/maindb.db -O ~/.config/book-manage-real/maindb.db")
    print("please reopen the program in order to active!")
    sys.exit()
print("/---------------------------------\\")
print("|Welcome to book managment system!|")
print("\\---------------------------------/")

def addingtosystem():
    results = []
    resreal = []

    # adding to the database
    print("press [q] to scan or exit scanning qrcode / barcode ")
    cam = cv2.VideoCapture(0)
    if cam.isOpened() == True:
        while(True):
            ret, frame = cam.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                status = cv2.imwrite('/home/'+username+'/.cache/book-manage-real/out.png', frame)
                break
        print("captured")
        results = decode(Image.open('/home/'+username+'/.cache/book-manage-real/out.png'))
        for i,obj in enumerate(results):
           print(str(i)+"| "+obj.type + " | " + obj.data.decode("utf-8"))
           resreal.append(obj.data.decode("utf-8"))
    cv2.destroyAllWindows()
    chooseing_value = input("input ISBN number (Type letter \"q\" if you want to type it yourself): ")
    if chooseing_value == "q":
        real_ISBNinput = input("Type your alterative ISBN you have: ")
    else:
        try:
            real_ISBNinput = resreal[int(chooseing_value)]
        except:
            real_ISBNinput = "?r " + str(random.randint(1,1000000))

    book_name = input("Input the book name: ")
    Author = input("Input the author: ")

    connection_string = "INSERT INTO \"main\".\"BookInfomation\"(\"ISBN\",\"Book name\",\"Author\") VALUES (\'"+real_ISBNinput+"\',\'"+book_name+"\',\'"+Author+"\');"
    conn.commit()
    try:
        conn.execute(connection_string)
    except:
        print("unsuccessful of adding book, possable reason: repeated ISBN")
    finally:
        print("Added the record!")
        conn.commit()

def PreviewItem():
    print("Preview Item")
    print("ISBN","book Name", "Author", sep="   |   ")
    for row in cur.execute("SELECT * FROM BookInfomation ORDER BY KEY"):
        print(row[0], end="  ")
        print(row[1], end="  ")
        print(row[3], end="  ")
    print("\nfinish printing \n \n")
def RemoveItem():
    print("Remove Item")
    print("id",end="|")
    print("ISBN","book Name", "Author", sep="   |   ")
    for row in cur.execute("SELECT * FROM BookInfomation ORDER BY KEY"):
        print(row[2], end="  ")
        print(row[0], end="  ")
        print(row[1], end="  ")
        print(row[3], end="  ")
    try:
        removeItemID = int(input("\nType the ID of the book you wanna delete: "))
        cur.execute("DELETE FROM BookInfomation WHERE KEY="+str(removeItemID))
        conn.commit()
    except ValueError:
        print("Try again!")
while True:
    try:
        print("\nPlease type an appropate character to get started!\n")
        print("[A]dding item \n[R]emove Item \n[P]review Item \n[Q]uit program")
        getstarted_Character = input("[A],[R],[P]:")
        if getstarted_Character == "A" or getstarted_Character=="a":
            addingtosystem()
        elif getstarted_Character == "Q" or getstarted_Character=="q":
            conn.close()
            print("Bye Bye")
            sys.exit()
        elif getstarted_Character == "P" or getstarted_Character=="p":
            PreviewItem()
        elif getstarted_Character == "r" or getstarted_Character=="R":
            RemoveItem()
        else:
            print("Please try again")
    except KeyboardInterrupt:
        conn.close()
        print("\n\nBye bye have a nice day!👋")
        sys.exit()
    finally:
        conn.close()

