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

# Global pandas dataframe storage for generated output to later export via GUI to output.csv
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


#calls validation functions
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
    data = pd._read_csv(fileName, dtype=dtype)
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


# fns to confirm input is int and qty does not exceed available data
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
    if fileName == "./datafiles_persongen/wy.csv":
        cleanData = data.dropna(subset=['NUMBER', 'STREET'])
    else:
        cleanData = data.dropna(subset=['NUMBER', 'CITY', 'STREET', 'POSTCODE'])
    return cleanData


# fn to randomly pick addresses from data w/ no duplicates
def parse_data(csvData, qty):
    rndIdx = random.sample(range(len(csvData)), qty)
    parsedData = csvData.iloc[rndIdx]
    return parsedData


#########################################################################################
#                    functions for cross-app comms
#########################################################################################
# code based on following source for socket tutorials for next 3 functions:
# https://www.youtube.com/watch?v=Lbfe3-v7yE0&t=511s
# https://www.youtube.com/watch?v=8A4dqoGL62E
# https://www.youtube.com/watch?v=WM1z8soch0Q


def feeder_socket():
    HEADERSIZE = 10 #corresponds to msg size of 10000 characters

    #start listener on localhost and socket 5425
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 5425))
    s.listen(5)

    #send message when client connection detected
    while True:
        clientsocket, address = s.accept()
        print(f"connection from {address} established")

        output_msg = output_for_content_generator()
        msg = pickle.dumps(output_msg)
        msg = bytes(f'{len(msg):{HEADERSIZE}}', "utf-8") + msg  #append header to msg

        clientsocket.send(msg)


def consumer_socket():
    HEADERSIZE = 10 #corresponds to max msg size of 10000 characters

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5423)) #connect to other microservice on port 5423

    full_msg = b''
    new_msg = True
    process_consumer_socket_msg(HEADERSIZE, full_msg, new_msg, s)


def process_consumer_socket_msg(HEADERSIZE, full_msg, new_msg, s):
    while True:
        msg = s.recv(10) #recv msg in chuncks of 10 bytes

        #upon msg receipt, get msglen from headersize
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        #use HEADERSIZE to determine when msg recipt is finished
        if len(full_msg) - HEADERSIZE == msglen:
            lifeGen = pickle.loads(full_msg[HEADERSIZE:]) #convert data from bytes to python obj
            process_lifegen_data(lifeGen)
            break


def process_lifegen_data(lifeGen):
    toy = lifeGen[0]
    category = lifeGen[1]
    generate_lifegen_gui_output(toy, category)
    return


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


#determine which GUI objects to manipulate and return to requesting function
def target_selection(target):
    if target == "lifeGen":
        frame = outputFrameToy
        label = outputLabelToy
        tree = pandasTreeToy

    else:
        frame = outputFrame
        label = outputLabel
        tree = pandasTree
    return frame, label, tree


def gui_input_validation(rawNumber, target):
    targets = target_selection(target)
    frame = targets[0]
    label = targets[1]
    while True:
        try:
            intOutput = int(rawNumber)
            return True
        except ValueError:
            if rawNumber == "":
                frame.config(bg="#ff9999")
                label.config(text="You must specify number to output", bg="#ff9999")
                return
            else:
                frame.config(bg="#ff9999")
                label.config(text="Number to output must be Integer", bg="#ff9999")
                return


#confirm there are enough data to fulfill request
def gui_output_qty_validation(intOutput, csvData, target):
    targets = target_selection(target)
    frame = targets[0]
    label = targets[1]

    if intOutput > len(csvData):
        frame.config(bg="#ff9999")
        label.config(text="Input is larger than number of valid addresses. There are: " + str(
            len(csvData)) + " valid addresses", bg="#ff9999")
        return False
    else:
        return True


def generate_persongen_gui_output():
    state = stateVar.get()
    rawInput = outputNum.get()
    state = state.lower()
    target = "personGen"
    generate_gui_output(state, rawInput, target)
    return


# for the "Toy Promotion" tab
def generate_lifegen_gui_output(toy, category):
    state = stateVarToy.get()
    rawInput = outputNumToy.get()
    state = state.lower()
    target = "lifeGen"
    if generate_gui_output(state, rawInput, target):
        generate_gui_prize(toy, category)
    return


def generate_gui_output(state, rawInput, target):
    # get correct datafile
    csvData = find_data_file(state)

    # validate input qty, print results to gui if true
    if gui_input_validation(rawInput, target):
        intOutput = int(rawInput)
        if gui_output_qty_validation(intOutput, csvData, target):
            parsedData = parse_data(csvData, intOutput)
            global df
            df = parsedData
            update_pandas_table(parsedData, target)
            return True
    return False


# place consumed data onto GUI
def generate_gui_prize(toy, category):
    prizeLabel.config(text=toy)
    prizeCategory.config(text=category)
    return


def update_pandas_table(parsedData, target):
    targets = target_selection(target)
    frame = targets[0]
    label = targets[1]
    tree = targets[2]

    # https: // tkdocs.com / tutorial / tree.html
    tree.delete(*tree.get_children())
    for index, row in parsedData.iterrows():
        tree.insert("", 'end', values=list(row))
    frame.config(bg="#b3ffb3")
    label.config(text="Complete!", bg="#b3ffb3")


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
tabMenu.pack(expand=2, fill="both", padx=5, pady=5)


# frames persongen
topFrame = Frame(personGenTab)
topFrame.pack()
bottomFrame = Frame(personGenTab)
bottomFrame.pack()
outputFrame = Frame(personGenTab)
outputFrame.pack(fill="x")
tableFrame = Frame(personGenTab, width=100)
tableFrame.pack(side=BOTTOM)


# frames lifegen Tab
topFrameToy = Frame(toyPromoteTab)
topFrameToy.pack()
bottomFrameToy = Frame(toyPromoteTab)
bottomFrameToy.pack()
outputFrameToy = Frame(toyPromoteTab)
outputFrameToy.pack(fill="x")
prizeFrame = Frame(toyPromoteTab)
prizeFrame.pack()
tableFrameToy = Frame(toyPromoteTab, width=100)
tableFrameToy.pack(side=BOTTOM)


# lables personGen
titleLabel = Label(topFrame, text="Person Generator - Prototype", font=25)
titleLabel.pack(padx=20, pady=20)
outputLabel = Label(outputFrame, text="")
outputLabel.pack(pady=5)


#labels lifeGen
titleLabelToy = Label(topFrameToy, text="Toy Promotion Tab", font=25)
titleLabelToy.pack(padx=20, pady=20)
outputLabelToy = Label(outputFrameToy, text="")
outputLabelToy.pack(pady=5)
prize = Label(prizeFrame, text="Prize & Prize Category: ", font=12)
prize.pack(side=TOP)
prizeLabel = Label(prizeFrame, text="")
prizeLabel.pack()
prizeCategory = Label(prizeFrame, text="")
prizeCategory.pack()


# treeview scrollbar personGen
#https://stackoverflow.com/questions/33375489/how-can-i-attach-a-vertical-scrollbar-to-a-treeview-using-tkinter
pandasTreeScroll = Scrollbar(tableFrame)
pandasTreeScroll.pack(side=RIGHT, fill=Y)


# treeview scrollbar lifeGen
pandasTreeScrollToy = Scrollbar(tableFrameToy)
pandasTreeScrollToy.pack(side=RIGHT, fill=Y)


# personGen display pandas dataframe w/ tkinter treeview widget
pandasTree = ttk.Treeview(tableFrame, yscrollcommand=pandasTreeScroll.set)
pandasTree.pack()
cols = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE']
pandasTree["columns"] = cols
pandasTree["show"] = 'headings'
for i in cols:
    pandasTree.column(i, anchor="center", minwidth=100, width=125, stretch=True)
    pandasTree.heading(i, text=i, anchor="center")
pandasTreeScroll.config(command=pandasTree.yview)


#lifeGen display pandas dataframe w/ tkinter treeview widget
pandasTreeToy = ttk.Treeview(tableFrameToy, yscrollcommand=pandasTreeScrollToy.set)
pandasTreeToy.pack()
cols = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE']
pandasTreeToy["columns"] = cols
pandasTreeToy["show"] = 'headings'
for i in cols:
    pandasTreeToy.column(i, anchor="center", minwidth=100, width=125, stretch=True)
    pandasTreeToy.heading(i, text=i, anchor="center")
pandasTreeScrollToy.config(command=pandasTreeToy.yview)


# person Gen Dropdown state menu
stateLabel = Label(topFrame, text="Select State: ")
stateLabel.pack(side=LEFT)
states = ['AK', 'AZ', 'CO', 'HI', 'ID', 'MT', 'NV', 'OR', 'UT', 'WA', 'WY']
stateVar = StringVar(root)
stateVar.set(states[0])
stateSelect = OptionMenu(topFrame, stateVar, *states)
stateSelect.pack(side=LEFT, padx=(5, 20))


#lifeGen drowdown state menu
stateLabelToy = Label(topFrameToy, text="Select State: ")
stateLabelToy.pack(side=LEFT)
statesToy = ['AK', 'AZ', 'CO', 'HI', 'ID', 'MT', 'NV', 'OR', 'UT', 'WA', 'WY']
stateVarToy = StringVar(root)
stateVarToy.set(statesToy[0])
stateSelectToy = OptionMenu(topFrameToy, stateVarToy, *statesToy)
stateSelectToy.pack(side=LEFT, padx=(5, 20))


# Persongen Number to generate (input box)
outputNumLabel = Label(topFrame, text="Number to Generate (int): ")
outputNumLabel.pack(side=LEFT, padx=(20, 5))
outputNum = Entry(topFrame)
outputNum.pack(side=LEFT)


# LifeGen Number to generate (input box)
outputNumLabelToy = Label(topFrameToy, text="Number to Generate (int): ")
outputNumLabelToy.pack(side=LEFT, padx=(20, 5))
outputNumToy = Entry(topFrameToy)
outputNumToy.pack(side=LEFT)


# Buttons w/ function calls personGen
genButton = Button(bottomFrame, text="Generate", bg="#cce6ff", height=4, width=30, command=generate_persongen_gui_output)
genButton.pack(side=LEFT, padx=10, pady=20)
csvButton = Button(bottomFrame, text="Export Result to CSV", bg="#cce6ff", height=4, width=30, command=tkinter_generate_csv)
csvButton.pack(side=LEFT, padx=10, pady=20)


# Lifegen buttons w/ fn calls
genButtonToy = Button(bottomFrameToy, text="Generate Prize and Winners!", bg="#cce6ff", height=4, width=30, command=consumer_socket)
genButtonToy.pack(side=LEFT, padx=10, pady=20)


#########################################################################################
#                    sys.argv processing and Mainloop
#########################################################################################


#if statement logic to determine if input.csv functions should be called
if len(sys.argv) > 1:
    print("Generating file...")
    output_csv_from_file()

else:
    if __name__ == '__main__':
        # multiprocessing, run socket server and tkinter simultaneously
        p1 = Process(name="ptkinter", target=tkinter_loop)
        p2 = Process(name="psocket", target=feeder_socket)
        p2.start()
        p1.start()

        # determine if tkinter window is closed, kill socket server if tkinter is closed
        while True:
            if not p1.is_alive():
                p2.terminate()
                break
