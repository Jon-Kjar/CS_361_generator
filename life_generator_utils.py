from csv import writer, reader
from pathlib import Path

# DB columns
CAT_SUB = "amazon_category_and_sub_category"
PROD_NAME = "product_name" 
NUM_REV = "number_of_reviews" 
ID = "uniq_id" 
AVER_REV = "average_review_rating"

# pulled data
DOG_DATA = "Dog Data"

# Input columns
INPUT_TYPE = "input_item_type"
INPUT_CATEGORY = "input_item_category"
INPUT_NUM_TO_GEN = "input_number_to_generate"

CSV_HEADER = [INPUT_TYPE,
              INPUT_CATEGORY,
              INPUT_NUM_TO_GEN,
              "output_item_name",
              "output_item_rating",
              "output_item_num_reviews"]


def create_csv(rows):
    """
    Writes the rows with the header into a output.csv file.
    :param rows: rows to use in the csv file
    :return: None
    """
    with open('output.csv', 'w') as f:
        output_writer = writer(f)
        output_writer.writerow(CSV_HEADER)
        for row in rows:
            output_writer.writerow(row)

      
class Data:
    data = []
    cols = {}

    @staticmethod
    def _read_csv(file_path):
        """
        Reads a csv file into an array object
        :param file_path: path of the file to read
        :return: Is an array or rows. Each row is an array.
        """
        p = []
        if Path(file_path).exists():
            with open(file_path, encoding="utf8") as f:
                csv_reader = reader(f, delimiter=',')
                for row in csv_reader:
                    p.append(row)
        else:
            print("you are missing your csv file: %s" % file_path)
        return p

    @staticmethod
    def _get_column_index(col_name, header):
        """
        Gets the column index of a specific name.
        :param col_name: column that we want the index of
        :param header: array of values. Should contain desired name
        :return: the index of the column name.
        """
        if col_name not in header:
            print("you are missing %s from your csv" % col_name)
        else:
            return header.index(col_name)


class DatabaseData(Data):
    def __init__(self, database_file_path):
        """
        Reads the database file and creates data for each row in class member.
        :param database_file_path: path to the database file
        """
        self.allTypes = []
        self.database_file_path = database_file_path

        self.__read_database_csv()

    def get_all_types(self):
        """
        Gets all unique categories from the database data, this does not include the empty categories.
        """
        self.allTypes = []
        for item in self.data:
            if item.category_subcategory not in self.allTypes and item.category_subcategory != "":
                self.allTypes.append(item.category_subcategory)

        self.allTypes = sorted(self.allTypes)
        return self.allTypes

    def __populate_header_variables(self, header):
        self.cols[ID] = self._get_column_index(ID, header)
        self.cols[PROD_NAME] = self._get_column_index(PROD_NAME, header)
        self.cols[CAT_SUB] = self._get_column_index(CAT_SUB, header)
        self.cols[NUM_REV] = self._get_column_index(NUM_REV, header)
        self.cols[AVER_REV] = self._get_column_index(AVER_REV, header)

    def __read_database_csv(self):
        p = self._read_csv(self.database_file_path)
        self.__populate_header_variables(p[0])
        p = p[1:]
        self.data = []
        for row in p:
            self.data.append(DatabaseRowData(row[self.cols[ID]],
                                             row[self.cols[PROD_NAME]],
                                             row[self.cols[CAT_SUB]],
                                             row[self.cols[NUM_REV]],
                                             row[self.cols[AVER_REV]]))

  
class DatabaseRowData:
    def __init__(self, _id, prod_name, cat_sub, num_rev, aver_rev):
        """
        Gathers the data from a row of the database file.
        Cleans the data by splitting or checking for empties
        """
        self.id = _id

        self.product_name = prod_name

        self.category_subcategory = cat_sub.split(' >')[0]

        if num_rev == "":
            num_rev = "0"
        self.number_reviews = int(num_rev.replace(',', ''))

        if aver_rev == "":
            aver_rev = "0"
        self.average_review = float(aver_rev.split(' out')[0])

    def create_csv_line(self, input_data_row):
        """
        Returns what information is needed for the creation of the output CSV file
        """
        result_row = [input_data_row.input_type,
                      input_data_row.input_cat,
                      str(input_data_row.input_num_to_generate),
                      self.product_name,
                      self.average_review,
                      self.number_reviews]

        return result_row


class InputData(Data):
    def __init__(self, input_file_path):
        """
        Reads the input file and creates data for each row in class member.
        """
        self.input_file_path = input_file_path

        if input_file_path is not None and Path(input_file_path).exists():
            self.__read_input_csv()

    def __read_input_csv(self):
        p = self._read_csv(self.input_file_path)
        self.__populate_header_variables(p[0])
        p = p[1:]
        for row in p:
            self.data.append(InputRowData(row[self.cols[INPUT_TYPE]],
                                          row[self.cols[INPUT_CATEGORY]],
                                          row[self.cols[INPUT_NUM_TO_GEN]]))

    def __populate_header_variables(self, header):
        self.cols[INPUT_TYPE] = self._get_column_index(INPUT_TYPE, header)
        self.cols[INPUT_CATEGORY] = self._get_column_index(INPUT_CATEGORY, header)
        self.cols[INPUT_NUM_TO_GEN] = self._get_column_index(INPUT_NUM_TO_GEN, header)

  
class InputRowData:
    def __init__(self, input_type, input_cat, input_num_to_generate):
        """
        Gathers information from the input file or user input
        """
        self.input_type = input_type
        self.input_cat = input_cat
        self.input_num_to_generate = input_num_to_generate
