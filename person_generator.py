# Import packages
from tkinter import *
from tkinter import ttk
from multiprocessing import *

import sys
import pandas as pd
import random
import socket
import pickle


# Seed random module
random.seed(a=None)

#state reference dict
STATE_KEY = {"ak": "Arkansas", "az": "Arizona", "co": "Colorado", "hi": "Hawaii", "id": "Idaho",
             "mt": "Montana", "nv": "Nevada", "or": "Oregon", "ut": "Utah", "wa": "Washington", "wy": "Wyoming"}

# Global storage for generated output to later export via GUI to output.csv
df = pd.DataFrame()


#########################################################################################
#                functions for input.csv processing
#########################################################################################


def output_csv_from_file():
    validatedInput = input_csv_validate()
    csvData = validatedInput[0]
    qty = validatedInput[1]
    outputData = parse_data(csvData, qty)
    outputData.to_csv('output.csv', index=False, header=True)
    print("Data successfully written to output.csv!")
    return


def input_csv_validate():
    inputData = input_csv_read("input.csv")
    inputState = inputData[0]
    inputNum = inputData[1]

    state = input_csv_state_validate(inputState)
    qty = input_csv_num_validate(inputNum)
    csvData = find_data_file(state)
    qty = input_csv_qty_validate(csvData, qty, state)
    return csvData, qty


# Function used to read input.csv and send variables to file input if-statement.
def input_csv_read(fileName):
    dtype = {'input_state': "string", 'input_number_to_generate': int}
    data = pd.read_csv(fileName, dtype=dtype)
    parsedInput = data.values[0]
    return parsedInput


# validation for input.csv state
def input_csv_state_validate(state):
    state = state.lower()
    for key in STATE_KEY:
        if STATE_KEY[key].lower() == state:
            state = key
            return state
        elif key == state:
            return state
    print("State not found. Some states were excluded by instructor, see Piazza post or check for typos in input.csv...")
    sys.exit()


# validation for input.csv qty
def input_csv_num_validate(qty):
    while True:
        try:
            qty = int(qty)
            return qty
        except ValueError:
            print("number_to_generate in input.csv not valid integer...")
            sys.exit()


def input_csv_qty_validate(csvData, qty, state):
    if qty > len(csvData):
        print("Input is larger than number of valid addresses. There are: " + str(
            len(csvData)) + " valid addresses for state: " + state.upper())
        sys.exit()
    else:
        return qty


#########################################################################################
#                   functions for reading from csv data sources
#########################################################################################


def find_data_file(state):
    csvName = "./datafiles_persongen/" + str(state) + ".csv"
    csvData = data_read(csvName)
    return csvData


# Function used to pull and clean data from CSV datasources using pandas
def data_read(fileName):
    dtype = {'NUMBER': "string", 'STREET': "string", 'UNIT': "string", 'CITY': "string", 'DISTRICT': "string",
             'REGION': "string", 'POSTCODE': "string"}
    data = pd.read_csv(fileName, dtype=dtype)

    # if statement for wyoming exception (no post codes in wyoming data).
    # pandas dropna command to remove data that are missing the required fields (Number, city, street, postcode)
    if fileName == "wy.csv":
        cleanData = data.dropna(subset=['NUMBER', 'STREET'])
    else:
        cleanData = data.dropna(subset=['NUMBER', 'CITY', 'STREET', 'POSTCODE'])
    return cleanData


def parse_data(csvData, qty):
    rndIdx = random.sample(range(len(csvData)), qty)
    parsedData = csvData.iloc[rndIdx]
    return parsedData


#########################################################################################
#                    functions for cross-app comms
#########################################################################################


# code based on following source for socket tutorials for next 2 functions:
# https://www.youtube.com/watch?v=Lbfe3-v7yE0&t=511s,
# https://www.youtube.com/watch?v=WM1z8soch0Q
def feeder_socket():
    HEADERSIZE = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 5425))
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        print(f"connection from {address} established")

        output_msg = output_for_content_generator()
        msg = pickle.dumps(output_msg)
        msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

        clientsocket.send(msg)


def consumer_socket():
    HEADERSIZE = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5423))

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

            d = pickle.loads(full_msg[HEADERSIZE:])
            pandasTree.delete(*pandasTree.get_children())
            for index, row in d.iterrows():
                pandasTree.insert("", 'end', values=list(row))
            outputFrame.config(bg="#b3ffb3")
            outputLabel.config(text="Complete!", bg="#b3ffb3")
            break


def output_for_content_generator():
    randState = ""

    while randState == "" or randState == "wy":   # excluding wy as data has no cities
        randState = random.choice(list(STATE_KEY.keys()))

    randAddr = parse_data(find_data_file(randState), 1)
    randCity = randAddr.values[0][3]
    stateProperName = STATE_KEY[randState]
    output = [randCity, stateProperName]
    return output


#########################################################################################
#                    functions for tkinter GUI
#########################################################################################


def tkinter_loop():
    root.mainloop()


# Function used to generate CSV file from GUI w/ pandas
def tkinter_generate_csv():
    df.to_csv('output.csv', index=False, header=True)
    outputFrame.config(bg="#b3ffb3")
    outputLabel.config(text="Success! Exported to output.csv", bg="#b3ffb3")
    return


# function to generate randomly generated addresses to GUI
def generateOutput():
    # get data from tkinter GUI
    state = stateVar.get()
    raw_number = outputNum.get()
    int_output = 0

    # try-except loop for GUI input validation
    while True:
        try:
            int_output = int(raw_number)
            break
        except ValueError:
            if raw_number == "":
                outputFrame.config(bg="#ff9999")
                outputLabel.config(text="You must specify number to output", bg="#ff9999")
                return
            else:
                outputFrame.config(bg="#ff9999")
                outputLabel.config(text="Number to output must be Integer", bg="#ff9999")
                return

    state = state.lower()
    csvData = find_data_file(state)

    # validate input qty
    if int_output > len(csvData):
        outputFrame.config(bg="#ff9999")
        outputLabel.config(text="Input is larger than number of valid addresses. There are: " + str(
            len(csvData)) + " valid addresses", bg="#ff9999")

    else:
        parsedData = parse_data(csvData, int_output)
        global df
        df = parsedData
        update_pandas_table(parsedData)
    return


def update_pandas_table(parsedData):
    # https: // tkdocs.com / tutorial / tree.html
    pandasTree.delete(*pandasTree.get_children())
    for index, row in parsedData.iterrows():
        pandasTree.insert("", 'end', values=list(row))
    outputFrame.config(bg="#b3ffb3")
    outputLabel.config(text="Complete!", bg="#b3ffb3")

#########################################################################################
#                    initialize tkinter GUI
#########################################################################################

# root
root = Tk()
root.title("Person Generator - Prototype")
root.geometry('900x600')

# tabs
tabMenu = ttk.Notebook(root)
personGenTab = ttk.Frame(tabMenu)
tabMenu.add(personGenTab, text='Person Generator - Prototype')
toyPromoteTab = ttk.Frame(tabMenu)
tabMenu.add(toyPromoteTab, text="Toy Give-away Promotion")
tabMenu.pack(expand=1, fill="both")

# frames
topFrame = Frame(personGenTab)
topFrame.pack()
bottomFrame = Frame(personGenTab)
bottomFrame.pack()
outputFrame = Frame(personGenTab)
outputFrame.pack(fill="x")
tableFrame = Frame(personGenTab, width=100)
tableFrame.pack(side=BOTTOM)


# lables
titleLabel = Label(topFrame, text="Person Generator - Prototype", font=25)
titleLabel.pack(padx=20, pady=20)
outputLabel = Label(outputFrame, text="")
outputLabel.pack(pady=5)


# treeview scrollbar
pandasTreeScroll = Scrollbar(tableFrame)
pandasTreeScroll.pack(side=RIGHT, fill=Y)


# display pandas dataframe w/ tkinter treeview widget
pandasTree = ttk.Treeview(tableFrame, yscrollcommand=pandasTreeScroll.set)
pandasTree.pack()
cols = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE']
pandasTree["columns"] = cols
pandasTree["show"] = 'headings'
for i in cols:
    pandasTree.column(i, anchor="center", minwidth=100, width=125, stretch=True)
    pandasTree.heading(i, text=i, anchor="center")
pandasTreeScroll.config(command=pandasTree.yview)


# Dropdown state menu
stateLabel = Label(topFrame, text="Select State: ")
stateLabel.pack(side=LEFT)
states = ['AK', 'AZ', 'CO', 'HI', 'ID', 'MT', 'NV', 'OR', 'UT', 'WA', 'WY']
stateVar = StringVar(root)
stateVar.set(states[0])
stateSelect = OptionMenu(topFrame, stateVar, *states)
stateSelect.pack(side=LEFT, padx=(5, 20))


# Number to generate (input box)
outputNumLabel = Label(topFrame, text="Number to Generate (int): ")
outputNumLabel.pack(side=LEFT, padx=(20, 5))
outputNum = Entry(topFrame)
outputNum.pack(side=LEFT)


# Buttons w/ function calls
genButton = Button(bottomFrame, text="Generate", bg="#cce6ff", height=4, width=30, command=generateOutput)
genButton.pack(side=LEFT, padx=10, pady=20)
csvButton = Button(bottomFrame, text="Get Data From SocketApp2", bg="#cce6ff", height=4, width=30, command=consumer_socket)
csvButton.pack(side=LEFT, padx=10, pady=20)



if len(sys.argv) > 1:
    print("Generating file...")
    output_csv_from_file()




else:
    if __name__ == '__main__':

        p1 = Process(name="ptkinter", target=tkinter_loop)
        p2 = Process(name="psocket", target=feeder_socket)
        p2.start()
        p1.start()

        print("Running")

        while True:
            if not p1.is_alive():
                p2.terminate()
                break