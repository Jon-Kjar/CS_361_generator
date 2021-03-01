#Created By Benjamin Hutkoff  #pass back dictionary with an index on it (turn output into a string) #city&state as a list #use pickle to unpickle
#Content Generator
#File Name ContentMain.py
#Date: 2/16/21

# tkinter library
import tkinter as tk
import wikipedia
import csv  #use to extract output csv to string or something
import socket #for infromation transfer between code
import pickle


#global definitions
global searchedParagraph
global searchedParagraph2
global content
global entry3

#function definitions

def Client(): #client function for information from person gen
    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5425))

    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg received")
            new_object = pickle.loads(full_msg[HEADERSIZE:])
            print(new_object)

            # for i in range(0,2):
            primaryString = '"' + new_object[0] + ", " + new_object[1] + '"'
            secondaryString = ',population'
            f = open('input.csv', "a")  # Opens input.csv
            f.truncate(17)
            f.write("\n")
            # f.write(new_object[i] + ",")  # Prints the line searched for to the input.csv file.
            f.write(primaryString)
            f.write(secondaryString)

            f.close()

            break

def read_input():

    root = tk.Tk()

    canvas3 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas3.pack()

    label8= tk.Label(root, text='Paste CSV file.')
    label8.config(font=('helvetica', 14))
    canvas3.create_window(200, 25, window=label8)

    label9 = tk.Label(root, text='Use this format: \n Primary Keyword,Secondary Keyword')
    label9.config(font=('helvetica', 14))
    canvas3.create_window(200, 85, window=label9)

    entry4 = tk.Entry(root)
    canvas3.create_window(200, 160, window=entry4)

    def secondSearch():
        global content

        term3 = entry4.get()
        f = open("input.csv", "a")

        content = term3
        f.write(content)
        f.close()

        # new canvas window 4
        root = tk.Tk()

        canvas4 = tk.Canvas(root, width=400, height=300, relief='raised')
        canvas4.pack()

        label10 = tk.Label(root, text='Paragraph Found.')
        label10.config(font=('helvetica', 14))
        canvas4.create_window(200, 25, window=label10)

        button10 = tk.Button(root, text='QUIT', command=quit, bg='brown', fg='white',
                             font=('helvetica', 9, 'bold'))
        canvas4.create_window(200, 240, window=button10)




        #end of new canvas window

        with open("input.csv", "r") as f_input:
            csv_input = csv.DictReader(f_input)

            for row in csv_input:
                Primary = row['Primary']
                Secondary = row['Secondary']

                print("Primary Keyword is: " + Primary + ". Secondary keyword is: " + Secondary + ".")
                #needs a way to truncate the second line after primary and secondary assignment

            f = open("search.csv", "a", encoding="utf-8", errors='ignore')
            # content = (wikipedia.page("Puppy(dog)").content)
            content = (wikipedia.page(f"{Primary}", auto_suggest=True).content)
            content.encode("utf-8")
            f.write(content)
            f.close()

            f = open('search.csv', 'r', errors='ignore')  # opens the search.csv file

            content = f.read()  # reads the search.csv file into a variable called content

            print(content)  # prints the content to the screen

            f.close()  # closes the original file

            term = Secondary  # make this user input
            file = open('search.csv', "r+", errors='ignore')
            for line in file:
                line.strip().split('/n')
                if term in line:
                    print(line)
                    # global searchedParagraph2
                    searchedParagraph2 = 'a'  # creates a string variable
                    searchedParagraph2 = line  # sets searchedParagraph equal to line contents
                    print(searchedParagraph2)
                    label7 = tk.Label(root, text=searchedParagraph2, font=('helvetica', 6, 'bold'), wraplength=300)
                    canvas4.create_window(200, 140, window=label7)
                    f = open('output.csv', "a")  # Opens output.csv
                    f.write(searchedParagraph2)  # Prints the line searched for to the output.csv file.
                    f.close()  # closes the file.

            file.truncate(0)  # deletes all the file data in the search.csv
            file.close()

    #canvas 3
    button8 = tk.Button(root, text='Upload CSV', command=secondSearch, bg='orange', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas3.create_window(200, 200, window=button8)

    button9 = tk.Button(root, text='QUIT', command=quit, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas3.create_window(200, 240, window=button9)



def write_import_batch(term2 = "puppydogs"):
    print(wikipedia.search(f"{term2}", results=1, suggestion=False))
    f = open("search.csv", "a", encoding="utf-8", errors='ignore')
    # content = (wikipedia.page("Puppy(dog)").content)
    content = (wikipedia.page(f"{term2}").content)
    f.write(content)
    f.close()

    f = open('search.csv', 'r')  # opens the search.csv file

    content = f.read()  # reads the search.csv file into a variable called content

    print(content)  # prints the content to the screen

    f.close()  # closes the original file

def write_import(): #sets term2 default to puppydogs
    global content
    term2 = entry3.get()
    write_import_batch(term2)

def write_run_batch(term = "breeds"):
    global searchedParagraph
    file = open('search.csv', "r+")
    for line in file:
        line.strip().split('/n')
        if term in line:
            print(line)
            searchedParagraph = 'a'  # creates a string variable
            searchedParagraph = line  # sets searchedParagraph equal to line contents

    file.truncate(0)  # deletes all the file data in the search.csv
    file.close()


def write_run():
    print("Running Program!")
    # term2 = entry3.get()
    # print(term2)
    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas1.pack()

    label1 = tk.Label(root, text='What word would you like to search for?')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)

    label2 = tk.Label(root, text='Enter Keyword:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)

    entry1 = tk.Entry(root)
    canvas1.create_window(200, 140, window=entry1)

    entry2 = tk.Entry(root)
    canvas1.create_window(200, 100, window=entry2)



    def getUI():
        global searchedParagraph
        x1 = entry1.get()
        term = entry1.get()  # make this user input
        write_run_batch(term)
        #content in between

        label7 = tk.Label(root, text=searchedParagraph, font=('helvetica', 6, 'bold'), wraplength=300)
        canvas1.create_window(200, 230, window=label7)



    def download():
        global searchedParagraph
        f = open('output.csv', "a")    #Opens output.csv
        f.write(searchedParagraph)     #Prints the line searched for to the output.csv file.
        f.close()                      #closes the file.

    #Buttons and Input for Second Canvas.

    button1 = tk.Button(root, text='Find Paragraph', command=getUI, bg='green', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)

    button2 = tk.Button(root, text='QUIT', command=quit, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(120, 180, window=button2)

    button6 = tk.Button(root, text='Download', command=download, bg='blue', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(295, 180, window=button6)

    label4 = tk.Label(root, text='Enter a secondary keyword:')
    label4.config(font=('helvetica', 14))
    canvas1.create_window(200, 100, window=label4)




    root.mainloop()

def getsearchedParagraph():
    global searchedParagraph
    write_import_batch()
    write_run_batch()
    return searchedParagraph

def identifiers():
    #start of canvas2 buttons abd input.
    root = tk.Tk()

    canvas2 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas2.pack()

    label1 = tk.Label(root, text='1. Enter a keyword and click import.')
    label1.config(font=('helvetica', 14))
    canvas2.create_window(200, 25, window=label1)

    label4 = tk.Label(root, text='2. Click Run.')
    label4.config(font=('helvetica', 14))
    canvas2.create_window(200, 65, window=label4)

    label5 = tk.Label(root, text='Optional: Click csv import to upload a csv file.')
    label5.config(font=('helvetica', 14))
    canvas2.create_window(200, 105, window=label5)

    button3 = tk.Button(root, text='QUIT', command=quit, bg='brown', fg='white',
                            font=('helvetica', 9, 'bold'))
    canvas2.create_window(120, 220, window=button3)
    #
    button4 = tk.Button(root, text='Run', command=write_run, bg='blue', fg='white',
                          font=('helvetica', 9, 'bold'))
    canvas2.create_window(280, 220, window=button4)
    #
    button5 = tk.Button(root, text='Import From Wiki', command=write_import, bg='green', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas2.create_window(200, 220, window=button5)

    button7 = tk.Button(root, text='Upload CSV', command=read_input, bg='orange', fg='white',
                            font=('helvetica', 9, 'bold'))
    canvas2.create_window(200, 260, window=button7)

    button20 = tk.Button(root, text='Socket', command=Client, bg='purple', fg='white',
                         font=('helvetica', 9, 'bold'))
    canvas2.create_window(200, 280, window=button20)

    #user input
    global entry3
    entry3 = tk.Entry(root)
    canvas2.create_window(200, 160, window=entry3)


    #end of canvas2 buttons and input.


    root.mainloop()

def main():
    identifiers()

if __name__ == "__main__":
    main()

