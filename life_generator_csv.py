import csv

# DB columns
CAT_SUB = "amazon_category_and_sub_category"
PROD_NAME = "product_name" 
NUM_REV = "number_of_reviews" 
ID = "uniq_id" 
AVER_REV = "average_review_rating" 

# pulled data
SELLER_STATE = "seller_state"

# Input columns
INPUT_TYPE = "input_item_type"
INPUT_CATEGORY = "input_item_category"
INPUT_NUM_TO_GEN = "input_number_to_generate"

CSV_HEADER = [INPUT_TYPE, INPUT_CATEGORY, INPUT_NUM_TO_GEN,
              "output_item_name", "output_item_rating", "output_item_num_reviews"]


# writes the rows with the header into a output.csv file
def create_csv(rows):
    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        for row in rows:
            writer.writerow(row)
      
      
class Data:
    def read_csv(self, file_path):
        p = []
        with open(file_path, encoding="utf8") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                p.append(row)
            return p

    def get_cols(self, col_name, header):
        if col_name not in header:
            print("you are missing %s from your csv" % col_name)
        else:
            return header.index(col_name)


class DatabaseData(Data):
    def __init__(self, file_path):
        """
        Reads the database file and creates data for each row in class member.
        """
        self.cols = {}
        self.allTypes = []
        self.data = []

        self.__read_database_csv(file_path)

    def get_all_types(self):
        """
        Gets all unique categories from the database data, this does not include the empty categories.
        """
        self.allTypes = []
        for item in self.data:
            if item.CAT_SUB not in self.allTypes and item.CAT_SUB != "":
                self.allTypes.append(item.CAT_SUB)

        self.allTypes = sorted(self.allTypes)
        return self.allTypes

    def __populate_header_variables(self, header):
        self.cols[ID] = self.get_cols(ID, header)
        self.cols[PROD_NAME] = self.get_cols(PROD_NAME, header)
        self.cols[CAT_SUB] = self.get_cols(CAT_SUB, header)
        self.cols[NUM_REV] = self.get_cols(NUM_REV, header)
        self.cols[AVER_REV] = self.get_cols(AVER_REV, header)

    def __read_database_csv(self, file_path):
        p = self.read_csv(file_path)
        self.__populate_header_variables(p[0])
        p = p[1:]
        self.data = []
        for row in p:
            self.data.append(DatabaseRowData(row[self.cols[ID]], row[self.cols[PROD_NAME]], row[self.cols[CAT_SUB]], row[self.cols[NUM_REV]], row[self.cols[AVER_REV]]))

  
class DatabaseRowData:
    def __init__(self, _id, prod_name, cat_sub, num_rev, aver_rev):
        """
        Gathers the data from a row of the database file. Cleans the data by splitting or checking for empties
        """
        self.ID = _id

        self.PROD_NAME = prod_name

        self.CAT_SUB = cat_sub.split(' >')[0]

        if num_rev == "":
            num_rev = "0"
        self.NUM_REV = int(num_rev.replace(',', ''))

        if aver_rev == "":
            aver_rev = "0"
        self.AVER_REV = float(aver_rev.split(' out')[0])

    def create_csv_line(self, input_data_row):
        """
        Returns what information is needed for the creation of the output CSV file
        """
        result_row = [input_data_row.inputType, input_data_row.inputCat, str(input_data_row.inputNumToGen), self.PROD_NAME, self.AVER_REV, self.NUM_REV]
        return result_row

class InputData(Data):
    def __init__(self, filePath):
      """
      Reads the input file and creates data for each row in class member.
      """
      self.data = []
      self.cols = {}

      if filePath is not None:
          self.__read_input_csv(filePath)
          self.filePath = filePath

    def __read_input_csv(self, filePath):
        p = self.read_csv(filePath)
        self.__populate_header_variables(p[0])
        p = p[1:]
        for row in p:
            self.data.append(InputRowData(row[self.cols[INPUT_TYPE]], row[self.cols[INPUT_CATEGORY]], row[self.cols[INPUT_NUM_TO_GEN]]))

    def __populate_header_variables(self, header):
        self.cols[INPUT_TYPE] = self.get_cols(INPUT_TYPE, header)
        self.cols[INPUT_CATEGORY] = self.get_cols(INPUT_CATEGORY, header)
        self.cols[INPUT_NUM_TO_GEN] = self.get_cols(INPUT_NUM_TO_GEN, header)

  
class InputRowData:
    def __init__(self, inputType, inputCat, inputNumToGen):
        """
        Gathers information from the input file or user input
        """
        self.inputType = inputType
        self.inputCat = inputCat
        self.inputNumToGen = inputNumToGen
 
