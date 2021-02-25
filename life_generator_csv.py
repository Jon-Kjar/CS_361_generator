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

CSV_HEADER = [INPUT_TYPE,INPUT_CATEGORY,INPUT_NUM_TO_GEN,"output_item_name","output_item_rating","output_item_num_reviews"]


# writes the rows with the header into a output.csv file
def createCSV(rows):
  with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADER)        
    for row in rows:
      writer.writerow(row)
      

def createCSVLines(results, inputDataRow):
  p = []
  for row in results:
    rowVal = [inputDataRow.inputType, inputDataRow.inputCat, str(inputDataRow.inputNumToGen), row.PROD_NAME, row.AVER_REV, row.NUM_REV]
    p.append(rowVal)
  return p


def readCSV(filePath):
  p = []
  with open(filePath) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      p.append(row)
    return p
      
# 
def getCols(colName, header):
  if colName not in header:
    print("you are missing %s from your csv" % colName)
  else:
    return header.index(colName)


def getTypes(colName):
  getCols(colName)
  typeArray = []
  if colName in cols.keys():
    for i,item in enumerate(dataset):
      if i is not 0:
         typeArray.append(item[cols[colName]].split(' >')[0])
    return list(sorted(set(typeArray)))
    



class DatabaseData:
  def __init__(self, filePath):
    self.cols = {}
    self.allTypes = []
    self.data = []
    
    self.__readDatabaseCSV(filePath)
    
  def getAllTypes(self):
    self.allTypes = []
    for item in self.data:
      if item.CAT_SUB not in self.allTypes and item.CAT_SUB is not "":
         self.allTypes.append(item.CAT_SUB)
    
    self.allTypes = sorted(self.allTypes)
    return self.allTypes
    #return list(sorted(set(typeArray)))
  
  def __populateHeaderVars(self, header):
    self.cols[ID] = getCols(ID, header)
    self.cols[PROD_NAME] = getCols(PROD_NAME, header)
    self.cols[CAT_SUB] = getCols(CAT_SUB, header)
    self.cols[NUM_REV] = getCols(NUM_REV, header)
    self.cols[AVER_REV] = getCols(AVER_REV, header)
    
  def __readDatabaseCSV(self, filePath):
    p = readCSV(filePath)
    self.__populateHeaderVars(p[0])
    p = p[1:]
    self.data = []
    for row in p:
      self.data.append(DatabaseRowData(row[self.cols[ID]], row[self.cols[PROD_NAME]], row[self.cols[CAT_SUB]], row[self.cols[NUM_REV]], row[self.cols[AVER_REV]]))
    
  
class DatabaseRowData:
  def __init__(self, _id, prod_name, cat_sub, num_rev, aver_rev): 
    self.ID = _id
    
    self.PROD_NAME = prod_name
    
    self.CAT_SUB = cat_sub.split(' >')[0]
    
    if num_rev == "":
      num_rev = "0"
    self.NUM_REV = int(num_rev.replace(',', ''))
    
    if aver_rev == "":
      aver_rev = "0"
    self.AVER_REV = float(aver_rev.split(' out')[0])


class InputData:
  def __init__(self, filePath):
    self.data = []
    self.cols = {}
    
    if filePath is not None:
      self.__readInputCSV(filePath)
      self.filePath = filePath
    
  def __readInputCSV(self, filePath):
    p = readCSV(filePath)
    self.__populateHeaderVars(p[0])
    p = p[1:]
    for row in p:
      self.data.append(InputRowData(row[self.cols[INPUT_TYPE]], row[self.cols[INPUT_CATEGORY]], row[self.cols[INPUT_NUM_TO_GEN]]))
 
  def __populateHeaderVars(self, header):
    self.cols[INPUT_TYPE] = getCols(INPUT_TYPE, header)
    self.cols[INPUT_CATEGORY] = getCols(INPUT_CATEGORY, header)
    self.cols[INPUT_NUM_TO_GEN] = getCols(INPUT_NUM_TO_GEN, header)

  
class InputRowData:
  def __init__(self, inputType, inputCat, inputNumToGen): 
    self.inputType = inputType
    self.inputCat = inputCat
    self.inputNumToGen = inputNumToGen
 
