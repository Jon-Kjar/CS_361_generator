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

CLIENT_PORT = 8546
DB_FILE = "amazon_co-ecommerce_sample.csv"
WINDOW_TITLE = "Life Generator"

dataset = None
outputGridVals = []


def main():
    lgg = LifeGeneratorGUI()


class LifeGeneratorGUI:
    entry_gui = None
    type_val = None
    quantity_variable = None

    def __init__(self):
        # read the dataset
        global dataset
        dataset = c.DatabaseData(DB_FILE)
        if dataset is None:
            print("you have a bad db csv file")

        prod_types = dataset.get_all_types()

        # read the input file if exists
        if len(sys.argv) > 1:
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

            # break so GUI does not open
            return

        # setup the window
        root1 = tk.Tk()

        root1.title(WINDOW_TITLE)
        root1.geometry("700x500")

        mainframe = tk.Frame(root1)
        mainframe.grid(column=0, row=0)

        vcmd = (root1.register(validate),
                '%P')

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
        self.type_val.set(prod_types[0])

        type_options = ttk.Combobox(mainframe, textvariable=self.type_val, values=prod_types)

        type_options.grid(column=2, row=2)

        # row 3 - generate
        generate_button = tk.Button(mainframe, text="Generate", command=self.generate_click)
        generate_button.grid(column=2, row=3)

        # row 4
        self.entry_gui = tk.Entry(mainframe)
        self.entry_gui.grid(column=1, columnspan=2, row=4)

        root1.mainloop()

    def generate_click(self):
        input_row = c.InputRowData("toy", self.type_val.get(), self.quantity_variable.get())

        result_array = get_top(input_row.inputCat, input_row.inputNumToGen)

        for x in outputGridVals:
            x.destroy()

        tp = tk.Entry(self.entry_gui, width=20)

        header4 = tk.Entry(self.entry_gui, width=20)
        header4.grid(row=0, column=4)
        header4.insert(tk.END, c.PROD_NAME)
        outputGridVals.append(header4)

        header5 = tk.Entry(self.entry_gui, width=20)
        header5.grid(row=0, column=5)
        header5.insert(tk.END, c.AVER_REV)
        outputGridVals.append(header5)

        header6 = tk.Entry(self.entry_gui, width=20)
        header6.grid(row=0, column=6)
        header6.insert(tk.END, c.NUM_REV)
        outputGridVals.append(header6)

        header7 = tk.Entry(self.entry_gui, width=20)
        header7.grid(row=0, column=7)
        header7.insert(tk.END, c.SELLER_STATE)
        outputGridVals.append(header7)

        dic = {}
        for i, row in enumerate(result_array):
            dic[row.PROD_NAME] = i
        # receive column 7 data from content generator
        print(str(dic))
        # lg_client = lgc.LifeGenClient(CLIENT_PORT)
        # lg_client.send_initial_info(dic)
        # wiki_desc = lg_client.receive_info()
        wiki_desc = ["HEY"] * len(result_array)
        # del lg_client

        # populate the contents of table
        for i, row in enumerate(result_array):
            tp4 = tk.Entry(self.entry_gui, width=20)
            tp4.grid(row=i + 1, column=4)
            tp4.insert(tk.END, row.PROD_NAME)
            outputGridVals.append(tp4)

            tp5 = tk.Entry(self.entry_gui, width=20)
            tp5.grid(row=i + 1, column=5)
            tp5.insert(tk.END, row.AVER_REV)
            outputGridVals.append(tp5)

            tp6 = tk.Entry(self.entry_gui, width=20)
            tp6.grid(row=i + 1, column=6)
            tp6.insert(tk.END, row.NUM_REV)
            outputGridVals.append(tp6)

            tp7 = tk.Entry(self.entry_gui, width=20)
            tp7.grid(row=i + 1, column=7)
            # tp7.insert(tk.END, wiki_desc[row.PROD_NAME])
            tp7.insert(tk.END, wiki_desc[i])
            outputGridVals.append(tp7)

        csv_results = []
        for row in result_array:
            csv_results.append(row.create_csv_line(input_row))

        c.create_csv(csv_results)


def validate(value_if_allowed):
    """
    filter the quantity to return by only float values
    :param value_if_allowed:
    :return:
    """
    if value_if_allowed:
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False


def get_top(cat, quantity):
    """
    algorithm to get the top 'quantity' num of products of certain type
    :param cat:
    :param quantity:
    :return:
    """
    # get all of category desired
    p = [s for s in dataset.data if s.CAT_SUB == cat]

    # sort by unique id
    p = sorted(p, key=lambda x: x.ID)

    # sort by number of reviews
    p = sorted(p, key=lambda x: x.NUM_REV, reverse=True)

    # take top (quantity * 10)
    p = p[:(quantity * 10)]

    # sort by average review
    p = sorted(p, key=lambda x: x.AVER_REV, reverse=True)

    # take top (quantity)
    p = p[:quantity]

    # for row in p:
    #     print('1ID:' + row.ID +
    #           '\tNum Revs: ' + str(row.NUM_REV) +
    #           '\tAvg Rev: ' + str(row.AVER_REV) +
    #           '\tCat: ' + str(row.CAT_SUB))
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
