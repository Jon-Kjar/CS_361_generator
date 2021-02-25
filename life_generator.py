# using file
# "amazon_co-ecommerce_sample.csv"
# under license
# https://creativecommons.org/licenses/by-sa/4.0/
import Tkinter as tk
import ttk as ttk

import sys
import tkMessageBox
import life_generator_client as lgc
import life_generator_csv as c

CLIENT_PORT = 8546 # will call my server method      

DB_FILE = "amazon_co-ecommerce_sample.csv"

dataset = None

WINDOW_TITLE = "Life Generator"

outputGridVals = []


def main():
  def generateClick():
    inputRow = c.InputRowData("toy", typeVal.get(), quant_var.get())
    
    resultArray = getTop(inputRow.inputCat, inputRow.inputNumToGen)
    
    for x in outputGridVals:
      x.destroy()
       
    tp = tk.Entry(t, width=20) 

    header4 = tk.Entry(t, width=20) 
    header4.grid(row=0, column=4) 
    header4.insert(tk.END, c.PROD_NAME) 
    outputGridVals.append(header4)
    
    header5 = tk.Entry(t, width=20) 
    header5.grid(row=0, column=5) 
    header5.insert(tk.END, c.AVER_REV) 
    outputGridVals.append(header5)
    
    header6 = tk.Entry(t, width=20) 
    header6.grid(row=0, column=6) 
    header6.insert(tk.END, c.NUM_REV) 
    outputGridVals.append(header6)
       
    
    header7 = tk.Entry(t, width=20) 
    header7.grid(row=0, column=7) 
    header7.insert(tk.END, c.SELLER_STATE) 
    outputGridVals.append(header7)
    
    dic = {}
    for i, row in enumerate(resultArray):    
      dic[row.PROD_NAME] = i
    # recieve column 7 data from content generator
    print(str(dic))
    lgClient = lgc.Life_Gen_Client(CLIENT_PORT)
    lgClient.sendInitialInfo(dic)
    wikiDesc = lgClient.recieveInfo()
    
    del lgClient
    
    #populate the contents of table
    for i, row in enumerate(resultArray):      
      tp4 = tk.Entry(t, width=20) 
      tp4.grid(row=i+1, column=4) 
      tp4.insert(tk.END, row.PROD_NAME) 
      outputGridVals.append(tp4)
      
      tp5 = tk.Entry(t, width=20) 
      tp5.grid(row=i+1, column=5) 
      tp5.insert(tk.END, row.AVER_REV) 
      outputGridVals.append(tp5)
      
      tp6 = tk.Entry(t, width=20) 
      tp6.grid(row=i+1, column=6) 
      tp6.insert(tk.END, row.NUM_REV) 
      outputGridVals.append(tp6)
    
      tp7 = tk.Entry(t, width=20) 
      tp7.grid(row=i+1, column=7) 
      tp7.insert(tk.END, wikiDesc[row.PROD_NAME]) 
      outputGridVals.append(tp7)
      
      
    results = []
    for row in resultArray:
      results.append(row.createCSVLine(inputRow))
    
      
    c.createCSV(results)
  
  # read the dataset
  global dataset 
  dataset = c.DatabaseData(DB_FILE)
  if dataset is None:
    print("you have a bad db csv file")
  
  #get category names

  prodTypes = dataset.getAllTypes()
  
  # read the input file if exists
  if len(sys.argv) > 1:
    input1 = sys.argv[1]
    inputData = c.InputData(input1)
    csvOutput = []
    for inputDataRow in inputData.data:
      print(str(inputDataRow))
      resultArray = getTop(inputDataRow.inputCat, int(inputDataRow.inputNumToGen))
      print(str(resultArray))
      results = []
      for resultRow in resultArray:
        results.append(resultRow.createCSVLine(inputDataRow))
      csvOutput.extend(results)
    c.createCSV(csvOutput)
    return 0
    
  # setup the window
  root1 = tk.Tk()
  
  root1.title(WINDOW_TITLE)
  root1.geometry("700x500")
  
  mainframe = tk.Frame(root1)
  mainframe.grid(column=0, row=0)
  
  vcmd = (root1.register(validate),
          '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
  
  #fdsa
  
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
  

# filter the quantity to return by only float values
def validate(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
  if value_if_allowed:
      try:
        int(value_if_allowed)
        return True
      except ValueError:
        return False
  else:
      return False


# algorithm to get the top 'quant' num of products of certain type
def getTop(cat, quant):
  # get all of category desired
  p = [s for s in dataset.data if s.CAT_SUB == cat]
 
  # sort by unique id
  p = sorted(p, key=lambda x: x.ID)
  
  # sort by number of reviews
  p = sorted(p, key=lambda x: x.NUM_REV, reverse=True)
  
  # take top (quantity * 10)
  p = p[:(quant*10)]
  
  # sort by average review
  p = sorted(p, key=lambda x: x.AVER_REV, reverse=True)
  
  # take top (quantity)
  p = p[:quant]
  
  #print('cat: ' + cat + ' len: ' + str(len(p)))
  for row in p:
    print('1ID:' + row.ID + '\tNum Revs: ' + str(row.NUM_REV) + '\tAvg Rev: ' + str(row.AVER_REV)+ '\tCat: ' + str(row.CAT_SUB))   
  return p


if __name__ == "__main__":
  main()

