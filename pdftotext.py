import PyPDF2 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
def ptot(file):
    filename =  file
    #open allows you to read the file
    pdfFileObj = open(filename,'rb')
    #The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    #This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
    else:
        text = textract.process(file, method='tesseract', language='eng')

    #pattern = re.compile(r'(\w{3}\d{2}\w{2}\d{3})(\w+\(\w+[+]?\))((,\s\w+\(\w+[+]?\))*)')
    #matches = pattern.finditer(text)
    #return matches
    return text

    # Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
    # Now, we will clean our text variable, and return it as a list of keywords.
