# using file
# "amazon_co-ecommerce_sample.csv"
# under license
# https://creativecommons.org/licenses/by-sa/4.0/
import tkinter as tk
import tkinter.ttk as ttk

import random
import sys
import life_generator_client as lgc
import life_generator_csv as c

CLIENT_PORT = 5432
DB_FILE = "amazon_co-ecommerce_sample.csv"
WINDOW_TITLE = "Life Generator"

dataset = None
outputGridVals = []


def main():
    lgg = LifeGeneratorGUI()
    lgg.create_gui()




class LifeGeneratorGUI:
    entry_gui = None
    type_val = None
    quantity_variable = None
    prod_types = None

    def __init__(self):
        # read the dataset
        global dataset
        dataset = c.DatabaseData(DB_FILE)
        if dataset is None:
            print("you have a bad db csv file")

        self.prod_types = dataset.get_all_types()

        # run from input csv file and end program
        if len(sys.argv) > 1:
            self.run_batch()
            return


    def create_gui(self):
        # setup the window
        root1 = tk.Tk()

        root1.title(WINDOW_TITLE)
        root1.geometry("700x500")

        mainframe = tk.Frame(root1)
        mainframe.grid(column=0, row=0)

        vcmd = (root1.register(validate), '%P')

        # row 1 - output quantity
        quantity_text = tk.StringVar()
        quantity_text.set("Enter results desired")
        quantity_dir = tk.Label(mainframe, textvariable=quantity_text, height=4)
        quantity_dir.grid(column=1, row=1)

        self.quantity_variable = tk.IntVar()

        input_entry = tk.Entry(mainframe, textvariable=self.quantity_variable, validate='key', validatecommand=vcmd)
        input_entry.grid(column=2, row=1)

        # row 2
        type_text = tk.StringVar()
        type_text.set("Choose toy category")
        type_dir = tk.Label(mainframe, textvariable=type_text, height=4)
        type_dir.grid(column=1, row=2)

        self.type_val = tk.StringVar(mainframe)
        self.type_val.set(self.prod_types[0])

        type_options = ttk.Combobox(mainframe, textvariable=self.type_val, values=self.prod_types)
        type_options.grid(column=2, row=2)

        # row 3 - generate
        generate_button = tk.Button(mainframe, text="Generate", command=self.generate_click)
        generate_button.grid(column=2, row=3)

        # row 4
        self.entry_gui = tk.Entry(mainframe)
        self.entry_gui.grid(column=1, columnspan=2, row=4)

        root1.mainloop()

    def __create_entry(self, name, col, row=0):
        header = tk.Entry(self.entry_gui, width=20)
        header.grid(row=row, column=col)
        header.insert(tk.END, name)
        outputGridVals.append(header)

    def generate_click(self):
        input_row = c.InputRowData("toy", self.type_val.get(), self.quantity_variable.get())

        result_array = get_top(input_row.inputCat, input_row.inputNumToGen)

        # clear out all old values
        for x in outputGridVals:
            x.destroy()

        # create headers
        self.__create_entry(c.PROD_NAME, 4)
        self.__create_entry(c.AVER_REV, 5)
        self.__create_entry(c.NUM_REV, 6)
        self.__create_entry(c.SELLER_STATE, 7)

        # receive column 7 data from content generator
        lg_client = lgc.LifeGenClient(CLIENT_PORT)
        wiki_desc = lg_client.receive_info()

        # populate the contents of table
        for i, row in enumerate(result_array):
            self.__create_entry(row.PROD_NAME, 4, i + 1)
            self.__create_entry(row.AVER_REV, 5, i + 1)
            self.__create_entry(row.NUM_REV, 6, i + 1)
            self.__create_entry(wiki_desc, 7, i + 1)

        csv_results = []
        for row in result_array:
            csv_results.append(row.create_csv_line(input_row))

        c.create_csv(csv_results)

    def run_batch(self):
        input1 = sys.argv[1]
        input_data = c.InputData(input1)
        csv_output = []
        for inputDataRow in input_data.data:
            print(str(inputDataRow))
            result_array = get_top(inputDataRow.inputCat, int(inputDataRow.inputNumToGen))
            print(str(result_array))
            results = []
            for resultRow in result_array:
                results.append(resultRow.create_csv_line(inputDataRow))
            csv_output.extend(results)
        c.create_csv(csv_output)


def validate(value_if_allowed):
    """
    filter the quantity to return by only float values
    :param value_if_allowed:
    :return:
    """
    try:
        int(value_if_allowed)
        return True
    except ValueError:
        return False


def get_top(cat, quantity):
    """
    algorithm to get the top 'quantity' num of products of certain type.
    Steps:
    1. get all of category desired
    2. sort by unique id
    3. sort by number of reviews
    4. take top (quantity * 10)
    5. sort by average review
    6. take top (quantity)
    :param cat:
    :param quantity:
    :return:
    """
    p = [s for s in dataset.data if s.CAT_SUB == cat]

    p = sorted(p, key=lambda x: x.ID)

    p = sorted(p, key=lambda x: x.NUM_REV, reverse=True)

    p = p[:(quantity * 10)]

    p = sorted(p, key=lambda x: x.AVER_REV, reverse=True)

    p = p[:quantity]
    return p


def get_top_random_toy():
    """

    :return:
    """
    # read the dataset
    global dataset
    dataset = c.DatabaseData(DB_FILE)
    if dataset is None:
        print("you have a bad db csv file")

    types = dataset.get_all_types()
    rand_type = random.choice(types)
    res = get_top(rand_type, 1)[0]

    return [res.PROD_NAME, res.CAT_SUB]


if __name__ == "__main__":
    main()
