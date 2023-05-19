import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import os
import csv
import fitz

class App(tk.Tk):
  def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
    super().__init__(screenName, baseName, className, useTk, sync, use)

    self.pdfFilePath =""
    self.codesFilePath=""
        
        
    tk.Button(self, text="Select PDF template file", command=lambda: self.selectPDFFile()).pack()
    tk.Button(self, text="Select codes file", command=lambda: self.selectCodesFile()).pack()

    self.pdfLabel = tk.Label(self, text="PDF template: ")
    self.pdfLabel.pack()
    self.codesLabel = tk.Label(self, text="Codes file")
    self.codesLabel.pack()

    tk.Label(self, text="String to replace (spaces before and after will be counted)")
    self.replaceEntry = tk.Entry(self)
    self.replaceEntry.pack()

    tk.Button(self, text="RUN", command=lambda: self.generateFiles()).pack()

    self.progressLabel = tk.Label(self, text="Progress: 0/?")
    self.progressLabel.pack()
    self.progressBar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=280)
    self.progressBar.pack()

  def selectPDFFile(self):
    self.pdfFilePath = fd.askopenfilename(filetypes=[("PDF files", "*.pdf" )])
    self.pdfLabel.config(text=f"PDF template: {self.pdfFilePath}")

  def selectCodesFile(self):
    self.codesFilePath = fd.askopenfilename(filetypes=[("CSC files", "*.csv" )])
    self.codesLabel.config(text=f"Codes file: {self.codesFilePath}")
  
  def progress(self, total, current):
    if total == 0 :
      self.progressBar['value'] = 0
      return
    self.progressBar['value'] = current / total * 100
    self.progressLabel['text'] = f"Progress: {current}/{total}"
    


  def generateFiles(self):
    if(self.replaceEntry.get() == "" or self.codesFilePath == "" or self.pdfFilePath == "" ):
      tk.messagebox.showerror("Error", "Please provide all details")
      return
    codes = []
    total = 0
    completed = 0
    self.progress(total, completed)
    #load csv
    try: 
      with open(self.codesFilePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
          # list of codes in csv format (one code per line)
          
          code = row[0]
          codes.append(code)
          line_count += 1
        print(f"processed {line_count} lines.")
    except: 
      tk.messageBox.showError(f"could not read file {self.codesFilePath} file not found or unable to be read")
      return
    
    total = len(codes)
    #load pdf

    for code in codes:
      template = fitz.Document(self.pdfFilePath)
      doc = template

      for page in doc: 
        print(page.get_fonts())
        for xref in page.get_contents():
          print(code, self.replaceEntry.get())
          print(self.replaceEntry.get().encode('UTF-8'))
          stream = doc.xref_stream(xref).replace(self.replaceEntry.get().encode('UTF-8'), 'blah'.encode('cp1252'))
          doc.update_stream(xref, stream)
      
      doc.save(f"{code}.pdf")
      completed += 1
      self.progress(total, completed)
    
    tk.messagebox.showinfo(message="Completed!!")


    
if __name__ == "__main__":
    app = App()
    app.mainloop()
