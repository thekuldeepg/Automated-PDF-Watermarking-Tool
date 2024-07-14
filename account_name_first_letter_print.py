##importing required modules
import os
import datetime
import slate3k as slate
import glob
import math
import sys
import tk
import PyPDF2
from openpyxl import workbook , load_workbook
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader , PdfFileWriter ,PdfFileMerger
from tkinter import Tk , filedialog

root = Tk()
root.withdraw()
root.attributes('-topmost', True)
label_file = filedialog.askopenfilenames(filetypes = [('pdf file', '*.pdf')])
if not label_file :
    print ("nor lable_file selected")
    sys.exit(0)
label_file = ''.join(label_file)
filepath = os.path.dirname(label_file)

#timestamp 
current_time = datetime.datetime.now()
second = str(current_time.second)
minute = str(current_time.minute)
hour = str(current_time.hour)
day = str(current_time.day)
month = str(current_time.month)
year = str(current_time.year)

timestamp = day+"_"+month+"_"+year+"_"+hour+"_"+minute+"_"+second+"_"

print ("Process Starting....")

#creating a pdf file object
pdFileObj = open(label_file, 'rb')
allContent = slate.PDF(pdFileObj)

#creating a pdf reader object
pdfReader =PyPDF2.PdfFileReader(pdFileObj)

#creating a pdf write object
pdfWriter = PyPDF2.PdfFileWriter()

#printing number of pages in pdf file
pageCount = pdfReader.numPages

#creating a page object
pageObj = pdfReader.getPage(0)

#extracting text from page
pageContent = allContent[0]

#print (pageContent)

isMessho =pageContent.find ('Fold Here')
isFlipkart = pageContent.find ('E-Kart')

mark = "0"

if isMessho > 0 :
    portal = "Messho"
    account = "Blank"

    if pageContent.find('CYGOD') > 0:
        account = "CYGOD"
        mark = "C"
    if pageContent.find('AYUSH') > 0:
        account = "AYUSH"
        mark = "A"
    #creating the watermark from an image
    c = canvas.Canvas('watermark.pdf')

    #Add some custom text for good measure
    c.setFont("Helvetica-Bold" , size = 60)

    if account == "CYGOD":
        c.setFont("Helvetica-Bold" , size = 40)
        c.setFont ("Helvetica-Bold" , size = 50)
    c.drawString (265 , 615 , mark)
    c.save()


if isFlipkart > 0 :
    portal = "Flipkart"
    account = "Blank"

    if pageContent.find('CYGOD') > 0:
        account = "CYGOD"
        mark = "C"
    if pageContent.find('AYUSH') > 0:
        account = "AYUSH"
        mark = "A"
    #creating the water mark from an image
    c = canvas.Canvas('watermark.pdf')

    #Add some custom text for good measure
    c.setFont("Helvetica-Bold" , size = 30)

    if account == "CYGOD":
        c.setFont("Helvetica-Bold" , size = 15)
        c.setFont ("Helvetica-Bold" , size = 25)
    c.drawString (250 , 690 , mark)
    c.save()

# Get the watermark file you just created
watermark = PdfFileReader(open("watermark.pdf" , "rb"))
i = 0
while i < pageCount :
    currentPage = pdfReader.getPage(i)
    currentPage.mergePage(watermark.getPage(0))
    pdfWriter.addPage(currentPage)

    if (i%10 == 0) :
        print(str(math.trunc(i/pageCount*100)) + "% of Lables Processed...")
        i = i+1

newFile = open(filepath + '\\' + account + '_watermarked_' + timestamp + '.pdf' , 'wb')
pdfWriter.write(newFile)
print("100% Done")
newFile.close()
pdFileObj.close()
#root.mainloop()