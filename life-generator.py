# using file
# "amazon_co-ecommerce_sample.csv"
# under license
# https://creativecommons.org/licenses/by-sa/4.0/

import Tkinter as tk
import ttk as ttk

import sys
import tkMessageBox
#import csvUtils
import csv

DB_FILE = "amazon_co-ecommerce_sample.csv"
CAT_SUB = "amazon_category_and_sub_category"
PROD_NAME = "product_name" 
NUM_REV = "number_of_reviews" 
ID = "uniq_id" 
AVER_REV = "average_review_rating" 

dataset = None
inputData = None

INPUT_TYPE = "input_item_type"
INPUT_CATEGORY = "input_item_category"
INPUT_NUM_TO_GEN = "input_number_to_generate"
inputCat = None
inputType = "toys"
inputNumToGen = 0

WINDOW_TITLE = "Life Generator"

cols = {}

outputGridVals = []


def createCSV(rows):
  with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["input_item_type","input_item_category","input_number_to_generate","output_item_name","output_item_rating","output_item_num_reviews"])        
    for row in rows:
      writer.writerow(row)
        
def createCSVLines(results, inputType, inputCat, inputCount, outputNameCol, outputRatingCol, outputNumReviewsCol):
  p = []
  for row in results:
    rowVal = [inputType, inputCat, str(inputCount), row[outputNameCol], row[outputRatingCol], row[outputNumReviewsCol]]
    p.append(rowVal)
  return p
        

def readCSV(filePath):
  p = []
  with open(filePath) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      p.append(row)
    return p
 

def main():
  def generateClick():
    global inputCat
    inputCat = typeVal.get()
    global inputNumToGen
    inputNumToGen = quant_var.get()
    #print("quant:" + str(inputNumToGen))
    #print("type:" + inputCat)
    resultArray = getTop(inputCat, inputNumToGen)
    
    for x in outputGridVals:
      x.destroy()
       
    tp = tk.Entry(t, width=20) 
 #    tp.grid(row=i, column=1) 
 #    tp.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp)
 # 
 #    tp2 = tk.Entry(t, width=20) 
 #    tp2.grid(row=i, column=2) 
 #    tp2.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp2)
 # 
 #    tp3 = tk.Entry(t, width=20) 
 #    tp3.grid(row=i, column=2) 
 #    tp3.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp3)
      
    header4 = tk.Entry(t, width=20) 
    header4.grid(row=0, column=4) 
    header4.insert(tk.END, PROD_NAME) 
    outputGridVals.append(header4)
    
    header5 = tk.Entry(t, width=20) 
    header5.grid(row=0, column=5) 
    header5.insert(tk.END, AVER_REV) 
    outputGridVals.append(header5)
    
    header6 = tk.Entry(t, width=20) 
    header6.grid(row=0, column=6) 
    header6.insert(tk.END, NUM_REV) 
    outputGridVals.append(header6)
       
    for i, row in enumerate(resultArray):
 #    tp = tk.Entry(t, width=20) 
 #    tp.grid(row=i+1, column=1) 
 #    tp.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp)
 # 
 #    tp2 = tk.Entry(t, width=20) 
 #    tp2.grid(row=i+1, column=2) 
 #    tp2.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp2)
 # 
 #    tp3 = tk.Entry(t, width=20) 
 #    tp3.grid(row=i+1, column=2) 
 #    tp3.insert(tk.END, resultArray[i][]) 
 #    outputGridVals.append(tp3)
      
      tp4 = tk.Entry(t, width=20) 
      tp4.grid(row=i+1, column=4) 
      tp4.insert(tk.END, resultArray[i][cols[PROD_NAME]]) 
      outputGridVals.append(tp4)
      
      tp5 = tk.Entry(t, width=20) 
      tp5.grid(row=i+1, column=5) 
      tp5.insert(tk.END, resultArray[i][cols[AVER_REV]]) 
      outputGridVals.append(tp5)
      
      tp6 = tk.Entry(t, width=20) 
      tp6.grid(row=i+1, column=6) 
      tp6.insert(tk.END, resultArray[i][cols[NUM_REV]]) 
      outputGridVals.append(tp6)
    results = createCSVLines(resultArray, inputType, inputCat, int(inputNumToGen), cols[PROD_NAME], cols[AVER_REV], cols[NUM_REV])
    createCSV(results)

  def generateBatch():
    createCSV(resultArray, cols[CAT_SUB], cols[CAT_SUB], int(inputNumToGen), cols[PROD_NAME], cols[AVER_REV], cols[NUM_REV])
    
  
  # read the dataset
  global dataset 
  dataset = readCSV(DB_FILE)
  if dataset is None:
    print("you have a bad db csv file")
  
  #get category names

  prodTypes = getTypes(CAT_SUB)
  getCols(PROD_NAME) 
  getCols(NUM_REV) 
  getCols(ID) 
  getCols(AVER_REV) 
  
  # read the input file if exists
  if len(sys.argv) > 1:
    input1 = sys.argv[1]
    global inputData 
    inputData = readCSV(input1)
    if inputData is None or INPUT_TYPE not in inputData[0] or INPUT_CATEGORY not in inputData[0] or INPUT_NUM_TO_GEN not in inputData[0]:
      print("you have a bad input csv file")
    else:
      rows = []
      for i,row in enumerate(inputData):
        if i == 0:
          continue
        global inputCat
        inputCat = row[1]
        global inputNumToGen
        inputNumToGen = row[2]
        global inputType
        inputType = row[0]
        resultArray = getTop(inputCat, int(inputNumToGen))
        results = createCSVLines(resultArray, inputType, inputCat, int(inputNumToGen), cols[PROD_NAME], cols[AVER_REV], cols[NUM_REV])
        rows.extend(results)
      createCSV(rows)
        
  # setup the window
  root1 = tk.Tk()
  
  root1.title(WINDOW_TITLE)
  root1.geometry("700x500")
  
  mainframe = tk.Frame(root1)
  mainframe.grid(column=0, row=0)
  
  vcmd = (root1.register(validate),
          '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
  
  #row 1 - output quantity
  quantityText=tk.StringVar()
  quantityText.set("Enter results desired")
  quantityDir=tk.Label(mainframe, textvariable=quantityText, height=4)
  quantityDir.grid(column=1, row=1)
  
  quant_var=tk.IntVar()

  inputentry = tk.Entry(mainframe, textvariable=quant_var, validate='key', validatecommand=vcmd)
  inputentry.grid(column=2, row=1)
  
  #row 2
  typeText=tk.StringVar()
  typeText.set("Choose toy type")
  typeDir=tk.Label(mainframe, textvariable=typeText, height=4)
  typeDir.grid(column=1, row=2)
  
  typeVal = tk.StringVar(mainframe)
  #for prodtype in prodTypes:
  #  print(prodtype)
  typeVal.set(prodTypes[0])

  #catText=tk.StringVar()
  #catText.set(prodTypes[0]) # default value
  typeOptions = ttk.Combobox(mainframe, textvariable=typeVal, values=prodTypes)
 
  #scrollbar = tk.Scrollbar(typeOptions)
  #scrollbar.pack(side= tk.RIGHT, fill = tk.BOTH)
  typeOptions.grid(column=2, row=2)      
  #scrollbar.config(command = typeOptions.yview)
  

    
  #row 3 - generate
  generateButton = tk.Button(mainframe, text="Generate", command=generateClick)
  generateButton.grid(column=2, row=3)
        
  #row 4  
  t = tk.Entry(mainframe) 
          
  #outputtext = tk.Text(mainframe)
  #outputtext.insert(tk.INSERT, output)
  t.grid(column=1, columnspan=2, row=4)        
  
  #my_canvas = tk.Canvas(t)
  #my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
  
  #my_scrollbar = tk.Scrollbar(t, orient=tk.VERTICAL, command=my_canvas.yview)
  root1.mainloop()
  
  
def validate(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
  if value_if_allowed:
      try:
          float(value_if_allowed)
          return True
      except ValueError:
          return False
  else:
      return False


def getTypes(colName):
  getCols(colName)
  typeArray = []
  if colName in cols.keys():
    for i,item in enumerate(dataset):
      if i is not 0:
         typeArray.append(item[cols[colName]].split(' >')[0])
    return list(sorted(set(typeArray)))
    
def getCols(colName):
  if colName not in dataset[0]:
    print("you are missing %s from your db csv" % colName)
  else:
    cols[colName] = dataset[0].index(colName)

    
def getTop(cat, quant):
  p = []
  #print(len(dataset))
  # get all of category desired
  rowNum = 0
  for row in dataset:
    if rowNum != 0 and cat == row[cols[CAT_SUB]].split(' >')[0]:
      p.append(row)
    rowNum = rowNum+ 1
  
  # remove anything without reviews
  p = [s for s in p if s[cols[NUM_REV]] is not ""]
  
  # sort by unique id
  p = sorted(p, key=lambda x: x[cols[ID]])
  
  # sort by number of reviews, remove ','s for example 1,999
  p = sorted(p, key=lambda x: int(x[cols[NUM_REV]].replace(',', '')), reverse=True)
  
  # take top (quantity * 10)
  p = p[:(quant*10)]
  
  # sort by average review
  p = sorted(p, key=lambda x: float(x[cols[AVER_REV]].split(' out')[0]), reverse=True)
  
  # take top (quantity)
  p = p[:quant]
  
  #print('cat: ' + cat + ' len: ' + str(len(p)))
  #for row in p:
   # print('ID:' + row[IDCol] + '\tNum Revs: ' + row[NumRevCol] + '\tAvg Rev: ' + row[AverageRevCol])   
  return p



if __name__ == "__main__":
  main()

