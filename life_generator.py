# using file
# "amazon_co-ecommerce_sample.csv"
# under license
# https://creativecommons.org/licenses/by-sa/4.0/
import tkinter as tk
import tkinter.ttk as ttk

import random
import sys
import life_generator_client as lgc
import life_generator_utils as c


DB_FILE = "amazon_co-ecommerce_sample.csv"
dataset = None
outputGridValues = []


class LifeGeneratorGUI:
    __GUI_TABLE_HEADERS = [c.PROD_NAME, c.AVER_REV, c.NUM_REV, c.DOG_DATA]
    __WINDOW_TITLE = "Life Generator"
    __CLIENT_PORT = 5432

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
            self.__run_batch()

    def create_gui(self):
        """
        sets up the GUI window
        :return: None
        """
        root1 = tk.Tk()

        root1.title(self.WINDOW_TITLE)
        root1.geometry("700x500")

        mainframe = tk.Frame(root1)
        mainframe.grid(column=0, row=0)

        validate_command = (root1.register(self.validate), '%P')

        # row 1 - output quantity
        quantity_text = tk.StringVar()
        quantity_text.set("Enter results desired")
        quantity_dir = tk.Label(mainframe, textvariable=quantity_text, height=4)
        quantity_dir.grid(column=1, row=1)

        self.quantity_variable = tk.IntVar()

        input_entry = tk.Entry(mainframe,
                               textvariable=self.quantity_variable,
                               validate='key',
                               validatecommand=validate_command)
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
        outputGridValues.append(header)

    def __generate_click(self):
        """
        Creates an output csv given the info in the GUI
        :return: None
        """
        # capture the GUI info
        input_row = c.InputRowData("toy", self.type_val.get(), self.quantity_variable.get())

        result_array = get_top(input_row.input_cat, input_row.input_num_to_generate)

        # clear out all old values
        for x in outputGridValues:
            x.destroy()

        # create headers
        for index, header in enumerate(self.__GUI_TABLE_HEADERS):
            self.__create_entry(header, index + 4)

        # receive column 7 data from content generator
        lg_client = lgc.LifeGenClient(self.CLIENT_PORT)
        wiki_desc = lg_client.receive_info()

        # populate the contents of table
        for i, row in enumerate(result_array):
            self.__create_entry(row.product_name, 4, i + 1)
            self.__create_entry(row.average_review, 5, i + 1)
            self.__create_entry(row.number_reviews, 6, i + 1)
            self.__create_entry(wiki_desc, 7, i + 1)

        csv_results = []
        for row in result_array:
            csv_results.append(row.create_csv_line(input_row))

        c.create_csv(csv_results)

    @staticmethod
    def __run_batch():
        """
        Creates the output csv file from an input csv file
        :return: None
        """
        input1 = sys.argv[1]
        input_data = c.InputData(input1)
        csv_output = []

        # for each row of the input file find the values requested
        for inputDataRow in input_data.data:
            result_array = get_top(inputDataRow.input_cat, int(inputDataRow.input_num_to_generate))
            results = []
            for resultRow in result_array:
                results.append(resultRow.create_csv_line(inputDataRow))
            csv_output.extend(results)

        c.create_csv(csv_output)

    @staticmethod
    def __validate(value_if_allowed):
        """
        filter the quantity to return by only int values
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
    :param cat: Category to sort
    :param quantity: quantity to return
    :return: items that fulfill the sort
    """
    p = [s for s in dataset.data if s.category_subcategory == cat]

    p = sorted(p, key=lambda x: x.id)

    p = sorted(p, key=lambda x: x.number_reviews, reverse=True)

    p = p[:(quantity * 10)]

    p = sorted(p, key=lambda x: x.average_review, reverse=True)

    p = p[:quantity]
    return p


def get_top_random_toy():
    """
    Function to interact with Person Generator client.
    Get's the top toy from a random category
    :return: array of the product name and the product category
    """
    # read the dataset
    global dataset
    dataset = c.DatabaseData(DB_FILE)
    if dataset is None:
        print("you have a bad db csv file")

    types = dataset.get_all_types()
    rand_type = random.choice(types)
    res = get_top(rand_type, 1)[0]

    return [res.product_name, res.category_subcategory]


def main():
    lgg = LifeGeneratorGUI()
    if len(sys.argv) > 1:
        return

    lgg.create_gui()


if __name__ == "__main__":
    main()
